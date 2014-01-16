from fontref import pdf_character_widths


CORE_FONTS = {
    'courier': 'Courier', 'courierB': 'Courier-Bold',
    'courierI': 'Courier-Oblique', 'courierBI': 'Courier-BoldOblique',
    'helvetica': 'Helvetica', 'helveticaB': 'Helvetica-Bold',
    'helveticaI': 'Helvetica-Oblique',
    'helveticaBI': 'Helvetica-BoldOblique',
    'times': 'Times-Roman', 'timesB': 'Times-Bold',
    'timesI': 'Times-Italic', 'timesBI': 'Times-BoldItalic',
    'symbol': 'Symbol', 'zapfdingbats': 'ZapfDingbats'}


class PDFFont(object):

    def __init__(self, session, family='helvetica', style=None, size=20):
        self.session = session
        self.families = ['courier', 'helvetica', 'arial', 'times', 'symbol', 'zapfdingbats']

        self.is_set = False
        self.font_size = None
        self.set_font(family, style, size)
        self.type = 'Core'


    def __repr__(self):
        return self.family

    def _set_family(self, family):
        if family is not None:
            family = family.lower()
            assert family in self.families, "%s not a valid font name" % family
            if(family == 'arial'):
                family = 'helvetica'
            else:
                self.family = family
        else:
            self.family = "helvetica"

    def _set_style(self, style=None):
        """ Style should be a string, containing the letters 'B' for bold,
        'U' for underline, or 'I' for italic, or should be None, for no style.
        Symbol will not be underlined. The underline style can further be
        modified by specifying the underline thickness and position.

        """
        if style is None:
            self.style = None
            self.underline = False
        # No syling for symbol
        elif self.family == ('symbol' or 'zapfdingbats'):
            self.style = None
            self.underline = False
        else:
            self.style = style.upper()
            # SetUnderline
            if('U' in self.style):
                self.underline = True

                # Remove U from style string, in case there is a bold / italic
                self.style = self.style.replace("U", "")
                self._set_underline_params()

            else:
                self.underline = False

            # Correct order of bold-italic
            if(self.style == 'IB'):
                self.style = 'BI'

    def _set_underline_params(self):
        # Does a good job visually representing an underline
        self.underline_thickness = int(1 * self.font_size / 8)
        if self.underline_thickness < 1:
            self.underline_thickness = 1
        self.underline_position = int(3 * self.font_size / 8)

    def _set_size(self, size=None):
        if size is not None:
            if self.font_size != size:
                self.font_size = float(size)
                self.line_size = self.font_size * 1.2
                self.is_set = False


    def _set_font_key(self):
        if self.style is None:
            self.font_key = self.family
        else:
            self.font_key = self.family + self.style

    def _set_name(self):
        self.name = CORE_FONTS[self.font_key]

    def _set_character_widths(self):
        self.character_widths = pdf_character_widths[self.font_key]

    def set_font(self, family=None, style=None, size=None):
        "Select a font; size given in points"
        self._set_family(family)
        self._set_size(size)
        self._set_style(style)
        self._set_font_key()
        self._set_name()
        self._set_character_widths()

    def _set_index(self, index=1):
        """ Index is the number of the font, not the same as
            object number, both are used and set in document.

        """
        self.index = index

    def _set_number(self, value):
        "This is the font pdf object number."
        self.number = value

    def _equals(self, font):
        if (font.family == self.family) and\
           (font.font_size == self.font_size) and\
           (font.style == self.style):
            ans = True
        else:
            ans = False
        return ans

    def dict(self):
        return {'i': self.index, 'type': 'core', 'name': self.name, 'up': 100,
                'ut': 50, 'character_width': self.character_width}

    def string_width(self, s):
        "Get width of a string in the current font"
        w = 0
        for i in s:
            w += self.character_widths[i]
        return w * self.font_size / 1000.0

    def set_line_size(self, value):
        "Set line_size"
        self.line_size = value

    def output(self):
            self.session._out('<</Type /Font')
            self.session._out('/BaseFont /' + self.name)
            self.session._out('/Subtype /Type1')
            if(self.name != 'Symbol' and self.name != 'ZapfDingbats'):
                self.session._out('/Encoding /WinAnsiEncoding')
            self.session._out('>>')
            self.session._out('endobj')
