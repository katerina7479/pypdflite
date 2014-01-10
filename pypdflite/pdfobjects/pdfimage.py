from os.path import splitext
import struct, StringIO
import urllib
import zlib, re


class PDFImage(object):

    def __init__(self, session, path, name, cursor):

        self.session = session
        self.path = path
        self.name = name
        self.cursor = cursor
        self.width = -1
        self.height = -1
        self.size = None  # in bits

        self.number = None  # Object number

        self.bits_per_component = None
        self.palette = None
        self.colorspace = None  # 'Indexed', 'DeviceCMYK',
        self.transparent = None

        self.soft_mask_data = None
        self.soft_mask = None
        self.filter = None
        self.decode = None

        self.run()

    def _set_number(self, number):
        """ Object number

        """
        self.number = number

    def _set_index(self, index=1):
        """ Image number

        """
        self.index = index

    def draw(self, page):
        self.session._out('q %s 0 0 %s %s %s cm /I%d Do Q' %
                          (self.width, self.height, self.cursor.x,
                          (self.cursor.y_prime - self.height),
                          self.index), page)
        self.cursor.x_plus(self.width)
        self.cursor.y_plus(self.height)

    def run(self):
        self._open_file()
        initial_data = ''
        initial_data = str(self.file.read())
        self.file.close()

        if not initial_data:
            raise Exception("Can't open image file: ", self.path)

        self.content_type = ''

        # handle GIFs
        if initial_data[:6] in ('GIF87a', 'GIF89a'):
            # Check to see if content_type is correct
            self.content_type = 'image/gif'
            w, h = struct.unpack("<HH", initial_data[6:10])
            self.width = int(w)
            self.height = int(h)

        elif (initial_data.startswith('\211PNG\r\n\032\n') and initial_data[12:16] == 'IHDR'):
            self.content_type = 'image/png'
            self._read_png()

        # handle JPEGs
        elif initial_data.startswith('\377\330'):
            self.content_type = 'image/jpeg'
            jpeg = StringIO.StringIO(initial_data)
            jpeg.read(2)
            b = jpeg.read(1)
            try:
                while (b and ord(b) != 0xDA):
                    while (ord(b) != 0xFF):
                        b = jpeg.read(1)
                    while (ord(b) == 0xFF):
                        b = jpeg.read(1)
                    if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                        jpeg.read(3)
                        h, w = struct.unpack(">HH", jpeg.read(4))
                        break
                    else:
                        jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0]) - 2)
                    b = jpeg.read(1)
                self.width = int(w)
                self.height = int(h)
            except struct.error:
                pass
            except ValueError:
                pass
        else:
            raise Exception("Unknown file type")

    def _read_png(self):

        def substr(s, start, length=-1):
            if length < 0:
                length = len(s) - start
            return s[start:start + length]

        self.transparent = None
        self.palette = None
        image_data = ''

        self.file = None
        self._open_file()
        f = self.file

        if(f.read(8) != '\x89PNG\r\n\x1a\n'):
            raise Exception('Not a PNG file: ')
        f.read(4)
        if(f.read(4) != 'IHDR'):
            self.error('Incorrect PNG file: ')
        w = struct.unpack('>HH', f.read(4))[1]
        h = struct.unpack('>HH', f.read(4))[1]
        self.width = int(w)
        self.height = int(h)
        # Find bits per component
        self.bits_per_component = ord(f.read(1))
        if self.bits_per_component > 8:
            raise Exception('16 bit not supported')

        # Find ct
        self.ct = ord(f.read(1))
        if(self.ct == 0 or self.ct == 4):
            self.colorspace = 'DeviceGray'
            coord = 1
        elif(self.ct == 2 or self.ct == 6):
            self.colorspace = 'DeviceRGB'
            coord = 3
        elif(self.ct == 3):
            self.colorspace = 'Indexed'
            coord = 1
        else:
            raise Exception('Unknown color type: %s' % self.ct)
        f.read(4)

        self.decode = '/Predictor 15 /Colors %s /BitsPerComponent %s /Columns %s' \
                      % (coord, self.bits_per_component, self.width)

        n = 1
        test_n = 1
        # f.seek(12)
        # passes = 0
        while True:
            # passes += 1
            last_pos = f.tell()
            header = f.read(4)
            if header in ('PLTE', 'tRNS', 'IDAT', 'IEND'):
                f.seek(last_pos - 4)
                test_n = struct.unpack('>HH', f.read(4))[1]
                f.read(4)
            if header == 'IHDR':
                #print "IHDR found"
                pass
            elif header == 'PLTE':
                #print "PLTE found"
                self.pallet = f.read(test_n)
                f.read(4)
            elif header == 'tRNS':
                #print "tRNS found"
                # Simple transparancy
                t = f.read(test_n)
                if self.ct == 0:
                    self.transparent = [ord(substr(t, 1, 1)), ]
                elif self.ct == 2:
                    self.transparent = [ord(substr(t, 1, 1)), ord(substr(t, 3, 1)), ord(substr(t, 5, 1))]
                else:
                    pos = t.find('\x00')
                    if pos != -1:
                        self.transparent = [pos, ]
                f.read(4)
            elif header == 'IDAT':
                #print "IDAT found"
                image_data += f.read(test_n)
                #print "Should equal size", test_n
                f.read(4)
            elif header == 'IEND':
                #print "End found"
                break
            else:
                f.seek(last_pos + 1)
                pass

        if self.colorspace == 'Indexed' and not self.palette:
            raise Exception('Missing Palette')
        f.close()

        if self.ct >= 4:
            #print "Color Test >= 4, splitting"
            image_data = zlib.decompress(image_data)
            color = ''
            alpha = ''
            if self.ct == 4:
                # Grey
                length = 2 * self.width
                for i in range(self.height):
                    pos = (1 + length) * i
                    color += image_data[pos]
                    alpha += image_data[pos]
                    line = substr(image_data, pos + 1, length)
                    color += re.sub('(.).', lambda m: m.group(1), line, flags=re.DOTALL)
                    alpha += re.sub('.(.)', lambda m: m.group(1), line, flags=re.DOTALL)
            else:
                # RGB image
                length = 4 * self.width
                for i in range(self.height):
                    pos = (1 + length) * i
                    color += image_data[pos]
                    alpha += image_data[pos]
                    line = substr(image_data, pos + 1, length)
                    color += re.sub('(.{3}).', lambda m: m.group(1), line, flags=re.DOTALL)
                    alpha += re.sub('.{3}(.)', lambda m: m.group(1), line, flags=re.DOTALL)

            image_data = zlib.compress(color)
            #self.soft_mask_data = zlib.compress(alpha)

        self.image_data = image_data
        self.size = len(self.image_data)
        self.filter = 'FlateDecode'
        """
        #if self.soft_mask_data is not None:
        #    self.soft_mask = PDFSoftMask(self.width, self.height, self.filter, self.soft_mask_data)

        if self.transparent is not None:
            self.transparent_string = ''
            for i in xrange(0, len(self.transparent)):
                self.transparent_string += '%s %s ' % (self.transparent[i], self.transparent[i])
        """
    def _open_file(self):
        if self.path.startswith("http://") or self.path.startswith("https://"):
            self.file = urllib.urlopen(self.path)
        else:
            self.file = open(self.path, 'rb')


class PDFSoftMask(object):
    def __init__(self, width, height, filtercode, data):
        self.width = width
        self.height = height
        self.filter = filtercode
        self.image_data = data
        self.size = len(self.image_data)
        self.bits_per_component = 8
        self.colorspace = 'DeviceRGB'
        self.decode = '/Predictor 15 /Colors 1 /BitsPerComponent 8 /Columns %s' % self.width
        self.transparent = None
        self.soft_mask = None

    def _set_number(self, number):
        """ Object number

        """
        self.number = number
