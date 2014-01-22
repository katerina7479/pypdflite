from fontref import pdf_character_widths


CORE_FONTS = {
    'courier': 'Courier',
    'courier_bold': 'Courier-Bold',
    'courier_italic': 'Courier-Oblique',
    'courier_bold_italic': 'Courier-BoldOblique',
    'helvetica': 'Helvetica',
    'helvetica_bold': 'Helvetica-Bold',
    'helvetica_italic': 'Helvetica-Oblique',
    'helvetica_bold_italic': 'Helvetica-BoldOblique',
    'times': 'Times-Roman',
    'times_bold': 'Times-Bold',
    'times_italic': 'Times-Italic',
    'times_bold_italic': 'Times-BoldItalic',
    'symbol': 'Symbol', 'zapfdingbats': 'ZapfDingbats'}


class PDFFont(object):

    def __init__(self, session, family='helvetica', style='', size=20):
        self.session = session

        self.is_set = False
        self.font_size = None
        self._set_font(family, style, size)
        self.type = 'Core'

    def __repr__(self):
        return self.family

    def _set_family(self, family):
        if family is not None:
            family = family.lower()
            if family not in CORE_FONTS:
                raise Exception("%s is not a valid core font" % family)
            self.family = family
        else:
            self.family = "helvetica"

    def _set_style(self, style=None):
        """ Style should be a string, containing the letters 'B' for bold,
        'U' for underline, or 'I' for italic, or should be '', for no style.
        Symbol will not be underlined. The underline style can further be
        modified by specifying the underline thickness and position.

        """
        if style is None:
            self.style = ''
            self.underline = False
        # No syling for symbol
        elif self.family == ('symbol' or 'zapfdingbats'):
            self.style = ''
            self.underline = False

        self.style = style.upper()
            # SetUnderline

        if 'U' in self.style or self.style == 'U':
            self.underline = True
        else:
            self.underline = False

    def _set_underline_params(self):
        # Does a pretty good job visually representing an underline
        if 'B' in self.style:
                multiplier = 1.5
        multiplier = 1

        self.underline_thickness = int(multiplier * self.font_size / 12.0)
        if self.underline_thickness < 1:
            self.underline_thickness = 1
        self.underline_position = int(multiplier * self.font_size / 7.0)

    def _set_size(self, size=None):
        if size is not None:
            if self.font_size != size:
                self.font_size = float(size)
                self.line_size = self.font_size * 1.2
                self._set_underline_params()
                self.is_set = False

    def _set_font_key(self):
        self.font_key = self.family
        if 'B' in self.style:
            self.font_key += '_bold'
        if 'I' in self.style:
            self.font_key += '_italic'

    def _set_name(self):
        self.name = CORE_FONTS[self.font_key]

    def _set_character_widths(self):
        self.character_widths = pdf_character_widths[self.font_key]

    def _set_font(self, family=None, style=None, size=None):
        "Select a font; size given in points"
        self._set_family(family)
        self._set_style(style)
        self._set_size(size)
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

    def _string_width(self, s):
        "Get width of a string in the current font"
        s = str(s)
        w = 0
        for i in s:
            w += self.character_widths[i]
        return w * self.font_size / 1000.0

    def _output(self):
            self.session._out('<</Type /Font')
            self.session._out('/BaseFont /' + self.name)
            self.session._out('/Subtype /Type1')
            if(self.name != 'Symbol' and self.name != 'ZapfDingbats'):
                self.session._out('/Encoding /WinAnsiEncoding')
            self.session._out('>>')
            self.session._out('endobj')
