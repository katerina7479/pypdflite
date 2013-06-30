

class PDFLine(object):
    def __init__(self, session, page, colorscheme, cursor1, cursor2, size=1):
        self.SS = session
        self.start = cursor1
        self.end = cursor2

        self.page = page

        self.colorscheme = colorscheme
        self.setSize(size)
        self.setColor()


    def setSize(self, linesize=1):
        self.linesize = linesize
        self.SS._out('%.2f w' % self.linesize)

    def setColor(self, colorscheme=None):
        if colorscheme is None:
            self.SS._out(self.colorscheme._getDrawColorString(), self.page)
        else:
            self.colorscheme = colorscheme
            self.setColor(None)

    def draw(self):
        s = '%.2f %.2f m %.2f %.2f l S' % (self.start.x, self.start.y, self.end.x, self.end.y)
        self.SS._out(s, self.page)