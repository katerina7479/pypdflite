from pdfcolor import PDFColor


class PDFLine(object):
    def __init__(self, session, page, cursor1, cursor2, size=1, color=None):
        self.SS = session
        self.start = cursor1
        self.end = cursor2

        self.page = page

        self.setColor(color)
        self.setSize(size)
        self.draw()

    def setColor(self, color):
        if color is None:
            pass
        elif isinstance(color, PDFColor):
            self.color = color
            self.color.setDrawColor()
        else:
            raise ValueError('%s is not a valid PDFColor object')

    def setSize(self, linesize=1):
        self.linesize = linesize
        self.SS._out('%.2f w' % self.linesize)

    def draw(self):
        self.SS._out()