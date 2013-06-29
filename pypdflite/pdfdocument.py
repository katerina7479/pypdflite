from pdfobjects.pdffont import PDFFont
from pdfobjects.pdfpage import PDFPage
from pdfobjects.pdfcolors import PDFColors
from pdfobjects.pdftext import PDFText


class PDFDocument(object):
    def __init__(self, session):
        self.SS = session
        self.pages = []
        self.fonts = []               # array of used fonts
        self._setDefaults()

    def _setDefaults(self):
        self._setColor()
        self._setFont()
        self.addPage()

    def _setColor(self):
        self.color = PDFColors()

    def _setFont(self):
        self.font = PDFFont()
        self.font.setIndex()
        self.fonts.append(self.font)

    def addPage(self):
        self.page = PDFPage(self.SS)
        self.page.setIndex(len(self.pages))
        self.pages.append(self.page)

    def setFont(self, family, style=None, size=None):
        "Select a font; size given in points"
        if size is None:
            size = self.font.fontsize
        newfont = PDFFont(family, style, size)

        #Test if font is already selected
        if not newfont.equals(self.font):
            #Test if used for the first time
            if newfont.fontkey not in self.fonts:
                i = len(self.fonts) + 1
                newfont.setIndex(i)
                self.fonts[newfont.fontkey] = newfont

        #Select it
        self.font = self.fonts[newfont.fontkey]
        print self.fonts
        if(self.page.number > 0):
            self.SS.out('BT /F%d %.2f Tf ET' % (self.font.index, self.font.fontsize), self.page)
        else:
            del newfont

    def setFontSize(self, size):
        "Set font size in points"
        if(self.font.fontsize == size):
            return
        else:
            self.setFont(self.font.family, self.font.style, size)

    def _getOrientationChanges(self):
        self.orientation_changes = []
        for page in self.pages:
            if page.orientation_change is True:
                self.orientation_changes.append(page.number)
            else:
                pass
        return self.orientation_changes

    def outputPages(self):
        if self.orientation_changes is None:
            self.getOrientationChanges()
        else:
            #Page
            for page in self.pages:
                self.SS.newobj()
                self.SS.out('<</Type /Page')
                self.SS.out('/Parent 1 0 R')
                if page in self.orientation_changes:
                    self.SS.out('/MediaBox [0 0 %.2f %.2f]' % (page.h, page.w))
                self.SS.out('/Resources 2 0 R')
                self.SS.out('/Contents %s 0 R>>' % len(self.SS.objects))
                self.SS.out('endobj')
                #Page content
                self.SS.newobj()
                if self.SS.compression is True:
                    textfilter = '/Filter /FlateDecode'
                    page.compress()
                else:
                    textfilter = ''
                self.SS.out('<< %s /Length %s >>' % (textfilter, len(page.buffer)))
                self.SS.putstream(page.buffer)
                self.SS.out('endobj')

    def outputFonts(self):
        for font in self.fonts:
            obj = self.SS.newobj()
            font.setNumber(obj.id)
            self.SS.out('<</Type /Font')
            self.SS.out('/BaseFont /' + font.name)
            self.SS.out('/Subtype /Type1')
            if(font.name != 'Symbol' and font.name != 'ZapfDingbats'):
                self.SS.out('/Encoding /WinAnsiEncoding')
            self.SS.out('>>')
            self.SS.out('endobj')

    def addText(self, text):
        text = PDFText(self.SS, self.page, self.font, self.color, text)

    def newline(self, number=1):
        self.page.newline(self.font, number)