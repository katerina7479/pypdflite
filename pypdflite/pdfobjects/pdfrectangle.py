

class PDFRectangle(object):
    def __init__(self, session, page, colorscheme, cursor1, cursor2, size=1, style='S'):
        self.SS = session
        self.page = page
        self.colorscheme = colorscheme

        self.stylelist = ['S', 'B', 'F']  # S is plain, B is filled with border, F is filled no border.

        self._setDimensions(cursor1, cursor2)
        self._setStyle(style)
        self.setSize(size)
        self.setColor()

    def _setDimensions(self, cursor1, cursor2):
        self.corner = cursor1
        difference = cursor2.subtract(cursor1)

        self.width = difference.x
        self.height = difference.y

    def _setStyle(self, style='S'):
        style = style.upper()
        if style in self.stylelist:
            self.style = style
        else:
            self.style = 'S'

    def setSize(self, linesize=1):
        self.linesize = linesize
        self.SS._out('%.2f w' % self.linesize)

    def setColor(self, colorscheme=None):
        if colorscheme is None:
            self.SS._out(self.colorscheme._getDrawColorString(), self.page)
            self.SS._out(self.colorscheme._getFillColorString(), self.page)
            print "Did colorscheme in rect", self.colorscheme._getFillColorString()
        else:
            self.colorscheme = colorscheme
            self.setColor(None)

    def draw(self):
        s = '%.2f %.2f %.2f %.2f re %s' % (self.corner.x, self.corner.y, self.width, self.height, self.style)
        self.SS._out(s, self.page)