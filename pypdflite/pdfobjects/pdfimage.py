import os
import struct, StringIO
import urllib
import zlib, re


class PDFImage(object):

    def __init__(self, session, path, name):

        self.session = session
        self.path = path
        self.name = name
        self.cursor = None
        self.width = -1
        self.height = -1
        self.size = None  # in bits

        self.number = None  # Object number

        self.bits_per_component = None
        self.palette = None
        self.colorspace = None  # 'Indexed', 'DeviceCMYK',
        self.transparent = None

        self.soft_mask = None
        self.filter = None
        self.decode = None

        self._get_metrics()

    def _set_number(self, number):
        """ Object number

        """
        self.number = number

    def _set_index(self, index=1):
        """ Image number

        """
        self.index = index

    def _set_cursor(self, cursor):
        self.cursor = cursor

    def _set_size(self, width=None, height=None):
        if width is not None and height is None:
            self.scale = width / float(self.width)
            self._set_scale()
        elif height is not None and width is None:
            self.scale = height / float(self.height)
            self._set_scale()
        elif width is None and height is None:
            self.scale = 1
            self._set_scale()
        else:
            self.scale_width = int(width)
            self.scale_height = int(height)

    def _set_scale(self):
        self.scale_width = int(self.width * self.scale)
        self.scale_height = int(self.height * self.scale)

    def _open_file(self):
        if self.path.startswith("http://") or self.path.startswith("https://"):
            self.file = urllib.urlopen(self.path)
        else:
            try:
                self.file = open(self.path, 'rb')
            except IOError:
                try:
                    path = os.path.join(self.session.project_dir, 'bin', self.path)
                    self.file = open(path, 'rb')
                    self.path = path
                except:
                    raise Exception("Use absolute paths for images")

    def _initialize(self):
        self._open_file()

        self.initial_data = str(self.file.read())
        self.file.close()
        if not self.initial_data:
            raise Exception("Can't openimage file: ", self.path)

    def _read(self):
        pass

    def _get_metrics(self):
        self._initialize()
        self._read()
        #self._set_scale()

    def _parse_image(self):
        self.transparent = None
        self.palette = None
        image_data = ''

        self.file = None
        self._open_file()
        f = self.file

        f.read(12)
        if(f.read(4) != 'IHDR'):
            raise Exception('Image is broken')
        w = struct.unpack('>HH', f.read(4))[1]
        h = struct.unpack('>HH', f.read(4))[1]
        self.width = int(w)
        self.height = int(h)
        #self._set_scale()
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
        while True:
            last_pos = f.tell()
            header = f.read(4)
            if header in ('PLTE', 'tRNS', 'IDAT', 'IEND'):
                f.seek(last_pos - 4)
                test_n = struct.unpack('>HH', f.read(4))[1]
                f.read(4)
            if header == 'IHDR':
                pass
            elif header == 'PLTE':
                self.pallet = f.read(test_n)
                f.read(4)
            elif header == 'tRNS':
                # Simple transparancy
                t = f.read(test_n)
                if self.ct == 0:
                    self.transparent = [ord(t[1:2]), ]
                elif self.ct == 2:
                    self.transparent = [ord(t[1:2]), ord(t[3:4]), ord(t[5:6])]
                else:
                    pos = t.find('\x00')
                    if pos != -1:
                        self.transparent = [pos, ]
                f.read(4)
            elif header == 'IDAT':
                image_data += f.read(test_n)
                f.read(4)
            elif header == 'IEND':
                break
            else:
                f.seek(last_pos + 1)
                pass

        if self.colorspace == 'Indexed' and not self.palette:
            raise Exception('Missing Palette')
        self.file.close()

        if self.ct >= 4:
            #print "Color Type >= 4, splitting"
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
                    line = image_data[pos + 1: pos + 1 + length]
                    color += re.sub('(.).', lambda m: m.group(1), line, flags=re.DOTALL)
                    alpha += re.sub('.(.)', lambda m: m.group(1), line, flags=re.DOTALL)
            else:
                # RGB image
                length = 4 * self.width
                for i in range(self.height):
                    pos = (1 + length) * i
                    color += image_data[pos]
                    alpha += image_data[pos]
                    line = image_data[pos + 1: pos + 1 + length]
                    color += re.sub('(.{3}).', lambda m: m.group(1), line, flags=re.DOTALL)
                    alpha += re.sub('.{3}(.)', lambda m: m.group(1), line, flags=re.DOTALL)

            image_data = zlib.compress(color)
            smdata = zlib.compress(alpha)
        else:
            smdata = None

        self.image_data = image_data
        self.size = len(self.image_data)
        self.filter = 'FlateDecode'

        if self.transparent is not None:
            self.transparent_string = ''
            for i in xrange(0, len(self.transparent)):
                self.transparent_string += '%s %s ' % (self.transparent[i], self.transparent[i])

        if smdata is not None:
            self.soft_mask = PDFSoftMask(self.session, self.width, self.height, smdata, self.filter)

    def _draw(self, page):
        self.session._out('q %s 0 0 %s %s %s cm /I%d Do Q' %
                          (self.scale_width, self.scale_height,
                           self.cursor.x, (self.cursor.y_prime - self.scale_height),
                          self.index), page)
        self.cursor.x_plus(self.scale_width)
        self.cursor.y_plus(self.scale_height)

    def _output(self):
        """ Prompts the creating of image objects.

        """
        self.session._out('<</Type /XObject')
        self.session._out('/Subtype /Image')
        self.session._out('/Width %s' % self.width)
        self.session._out('/Height %s' % self.height)

        if self.colorspace is 'Indexed':
            self.session._out('/ColorSpace [/Indexed /DeviceRGB %s %s 0 R' %
                              (self.pal, self.number + 1))
        else:
            self.session._out('/ColorSpace /%s' % self.colorspace)
            if self.colorspace is 'DeviceCMYK':
                self.session._out('/Decode [1 0 1 0 1 0 1 0]')

        self.session._out('/BitsPerComponent %s' % self.bits_per_component)

        if self.filter:
            self.session._out('/Filter /%s' % self.filter)
        if self.decode:
            self.session._out('/DecodeParms << %s >>' % self.decode)
        if self.transparent:
            self.session._out('/Mask [%s]' % self.transparent_string)
        if self.soft_mask:
            self.session._out('/SMask %s 0 R' % (self.number + 1))
        self.session._out('/Length %s >>' % self.size)
        self.session._put_stream(self.image_data)
        self.session._out('endobj')

        if self.colorspace is 'Indexed':
            self.session._out('<<%s /Length %s >>' % (self.palette_filter, self.palette_length))
            self.session._put_stream(self.palette)
            self.session._out('endobj')

        if isinstance(self.soft_mask, PDFImage):
            obj = self.session._add_object()
            self.soft_mask._set_number(obj.id)
            self.soft_mask._output()


class PDFSoftMask(PDFImage):
    def __init__(self, session, width, height, data, imfilter):
        self.session = session
        self.width = width
        self.height = height
        self.image_data = data
        self.bits_per_component = 8
        self.colorspace = 'DeviceGray'
        self.filter = imfilter
        self.decode = '/Predictor 15 /Colors 1 /BitsPerComponent 8 /Columns %s' % self.width
        self.path = None
        self.size = len(self.image_data)

    def draw(self):
        pass

    def parse_image(self):
        pass

    def _initialize(self):
        pass

    def _output(self):
        self.session._out('<</Type /XObject')
        self.session._out('/Subtype /Image')
        self.session._out('/Width %s' % self.width)
        self.session._out('/Height %s' % self.height)
        self.session._out('/ColorSpace /%s' % self.colorspace)
        self.session._out('/BitsPerComponent %s' % self.bits_per_component)

        if self.filter:
            self.session._out('/Filter /%s' % self.filter)

        self.session._out('/DecodeParms << %s >>' % self.decode)
        self.session._out('/Length %s >>' % self.size)
        self.session._put_stream(self.image_data)
        self.session._out('endobj')
