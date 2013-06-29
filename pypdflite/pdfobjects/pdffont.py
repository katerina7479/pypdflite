from fontref import fpdf_charwidths


class PDFFont(object):
    def __init__(self, family='helvetica', style=None, size=20):
        self.core_fonts = {'courier': 'Courier', 'courierB': 'Courier-Bold', 'courierI': 'Courier-Oblique', 'courierBI': 'Courier-BoldOblique',
                           'helvetica': 'Helvetica', 'helveticaB': 'Helvetica-Bold', 'helveticaI': 'Helvetica-Oblique', 'helveticaBI': 'Helvetica-BoldOblique',
                           'times': 'Times-Roman', 'timesB': 'Times-Bold', 'timesI': 'Times-Italic', 'timesBI': 'Times-BoldItalic',
                           'symbol': 'Symbol', 'zapfdingbats': 'ZapfDingbats'}

        self.families = ['courier', 'helvetica', 'arial', 'times', 'symbol', 'zapfdingbats']
        self.setFont(family, style, size)

    def _setfamily(self, family=None):
        if family is None:
            pass
        else:
            family = family.lower()
            assert family in self.families, "%s is not a valid font name" % family
            if(family == 'arial'):
                family = 'helvetica'
            else:
                self.font_family = family

    def _setStyle(self, style):
        if style is None:
            self.style = None
            self.underline = False
        # No syling for symbol
        elif self.font_family == ('symbol' or 'zapfdingbats'):
            self.style = None
            self.underline = False
        else:
            self.style = style.upper()
            # SetUnderline
            if('U' in self.style):
                self.underline = True
                self.style = self.style.replace("U", "")
                self.underlinethickness = int(1*self.fontsize/8)
                if self.underlinethickness < 1:
                    self.underlinethickness = 1
                self.underlineposition = int(3*self.fontsize/8)
            else:
                self.underline = False
            # Correct order of bold-italic
            if(self.style == 'IB'):
                self.style = 'BI'

    def _setSize(self, size):
        if size is None:
            pass
        else:
            self.fontsize = float(size)
            self.linesize = self.fontsize * 1.2

    def _setFontKey(self):
        if self.style is None:
            self.fontkey = self.font_family
        else:
            self.fontkey = self.font_family + self.style

    def _setName(self):
        self.name = self.core_fonts[self.fontkey]

    def _setCharacterWidths(self):
        self.cw = fpdf_charwidths[self.fontkey]

    def setFont(self, family=None, style=None, size=None):
        "Select a font; size given in points"
        self._setfamily(family)
        self._setSize(size)
        self._setStyle(style)
        self._setFontKey()
        self._setName()
        self._setCharacterWidths()

    def setIndex(self, index=1):
        self.index = index

    def dict(self):
        return {'i': self.index, 'type': 'core', 'name': self.name, 'up': 100, 'ut': 50, 'cw': self.cw}

    def inCoreFonts(self, key):
        test = key.lower()
        if test in self.core_fonts:
            return True
        else:
            return False

    def equals(self, font):
        if (font.font_family == self.font_family) and\
           (font.fontsize == self.fontsize) and\
           (font.style == self.style):
            ans = True
        else:
            ans = False
        return ans

    def StringWidth(self, s):
        "Get width of a string in the current font"
        w = 0
        for i in s:
            w += self.cw[i]
        return w * self.fontsize/1000.0

    def setNumber(self, value):
        self.number = value

    def set_linesize(self, width):
        "Set line size"
        self.linesize = width
