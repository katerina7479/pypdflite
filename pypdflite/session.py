from pdfobjects.pdfobject import PDFObject


class Session(object):
    def __init__(self, parent):
        self.parent = parent
        self.buffer = ''
        self.offset = 0
        self.objects = []
        self._createplaceholders()
        self.compression = False

    def setCompression(self, value):
        if type(value) is bool:
            self.compression = value
        else:
            raise Exception(TypeError, "%s is not a valid option for compression" % value)

    def _createplaceholders(self):
        self.objects.append("Zeroth")
        self.objects.append("Catalog")
        self.objects.append("Pages")

    def out(self, s, page=None):
        if page is not None:
            page.buffer += str(s) + "\n"
        else:
            self.buffer += str(s) + "\n"

    def putstream(self, s):
        self.out('stream')
        self.out(s)
        self.out('endstream')

    def newobj(self, flag=None):
        self.offset = self.offset + len(self.buffer)
        if flag is None:
            objnum = len(self.objects)
            obj = PDFObject(objnum, self.offset)
            self.objects.append(obj)
        else:
            objnum = flag
            obj = PDFObject(objnum, self.offset)
            self.objects[flag] = obj
        self.out(str(objnum) + ' 0 obj')
        return obj

    def addPage(self, text):
        self.parent.D.addPage()
        self.parent.D.addText(text)
