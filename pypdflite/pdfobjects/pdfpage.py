from pdfmargin import PDFMargin
from pdfcursor import PDFCursor
from zlib import compress


class PDFPage(object):
    def __init__(self, session, orientation="P", format="letter"):
        self.SS = session

        self.formatdict = {'a3': (841.89, 1190.55), 'a4': (595.28, 841.89), 'a5': (420.94, 595.28), 'letter': (612, 792), 'legal': (612, 1008), "11x17": (792, 1224)}
        self.orientation = orientation
        self.format = format

        self.cursor = PDFCursor()

        self.margin = None
        self.setPageSize(format)
        self.setOrientation(orientation)
        self.setMargins()

        self.orientation_change = False
        self.buffer = ""

    def compress(self):
        self.buffer = compress(self.buffer)

    def setIndex(self, value):
        self.number = value

    def setPageSize(self, format):
        self.format = format.lower()
        if self.format in self.formatdict:
            self.pagesize = self.formatdict[self.format]
        else:
            raise Exception('Unknown page format: ', self.format)

    def _setWidthHeight(self):
        if self.margin is None:
            self.w = self.size[0]
            self.h = self.size[1]
        else:
            self.w = self.size[0] - self.margin.l - self.margin.r
            self.h = self.size[1] - self.margin.t - self.margin.b

    def setOrientation(self, orientation):
        self.orientation = orientation.lower()
        if(self.orientation == 'p' or self.orientation == 'portrait'):
            self.size = self.pagesize
        elif(self.orientation == 'l' or self.orientation == 'landscape'):
            self.size = (self.pagesize[1], self.pagesize[0])
        else:
            raise Exception('Incorrect orientation: ', self.orientation)
        self._setWidthHeight()
        self._setBounds()

    def changeOrientation(self):
        if self.orientation_change is False:
            self.size = (self.size[1], self.size[0])
            self.orientation_change = True
            self._setWidthHeight()
            self._setBounds()
        else:
            pass

    def setMargins(self, margin=None):
        if margin is None:
            self.margin = PDFMargin()
        elif isinstance(margin, PDFMargin):
            self.margin = margin
        else:
            raise Exception("Invalid Margin object")
        self._setWidthHeight()
        self._setBounds()

    def _setBounds(self):
        if self.margin is None:
            xmin = 0
            xmax = self.size[0]
            ymin = self.size[1]
            ymax = 0
        else:
            xmin = 0 + self.margin.l
            xmax = self.size[0] - self.margin.r
            ymin = self.size[1] - self.margin.t
            ymax = 0 + self.margin.b
        self.cursor.setBounds(xmin, ymin, xmax, ymax)
