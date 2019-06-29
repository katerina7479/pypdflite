from .pdfimage import PDFImage
import struct
import io


class PDFJPG(PDFImage):

    def __init__(self, *args, **kwargs):
        super(PDFJPG, self).__init__(*args, **kwargs)

    def _read(self):
        # handle JPEGs
        if self.initial_data.startswith(bytes([0xFF, 0xD8, 0xFF])):
            self.content_type = 'image/jpeg'
            jpeg = io.BytesIO(self.initial_data)
            jpeg.read(2)
            b = jpeg.read(1)
            try:
                w, h = 0, 0
                while b and b != b'\xDA':
                    while b != b'\xFF':
                        b = jpeg.read(1)
                    while b == b'\xFF':
                        b = jpeg.read(1)
                    if b'\xC0' <= b <= b'\xC3':
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
