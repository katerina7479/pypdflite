from .pdfimage import PDFImage


class PDFPNG(PDFImage):

    def __init__(self, *args, **kwargs):
        super(PDFPNG, self).__init__(*args, **kwargs)

    def _read(self):
        if self.initial_data.startswith(b'\211PNG\r\n\032\n') and self.initial_data[12:16] == b'IHDR':
            self.content_type = 'image/png'
            self._parse_image()
        else:
            raise Exception("Unknown file type")
