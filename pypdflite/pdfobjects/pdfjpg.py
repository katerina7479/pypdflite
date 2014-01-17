from os.path import splitext
from pdfimage import PDFImage
import struct, StringIO
import urllib
import zlib, re


class PDFJPG(PDFImage):

    def __init__(self, *args, **kwargs):
        super(PDFJPG, self).__init__(*args, **kwargs)

    def _read(self):
        # handle JPEGs
        if self.initial_data.startswith('\377\330'):
            self.content_type = 'image/jpeg'
            jpeg = StringIO.StringIO(self.initial_data)
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
        self._parse_image()

    def _parse_image(self):
        self._open_file()
        self.colorspace = 'DeviceRGB'
        self.bits_per_component = 8
        self.filter = 'DCTDecode'
        self.image_data = self.file.read()
        self.size = len(self.image_data)
        self.file.close()
