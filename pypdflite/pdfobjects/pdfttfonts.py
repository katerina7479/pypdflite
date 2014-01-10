from truetype.ttfonts import TTFontFile
import re, zlib


FONT_DIR = 'pypdflite/pdfobjects/truetype/'
Families = ['arial', 'dejavusans']
Filedict = {'arial': FONT_DIR + 'arial.ttf',
            'dejavusans': FONT_DIR + 'DejaVuSans.ttf'
            }


class PDFTTFont(object):
    def __init__(self, session, family='arial', style=None, size=20):
        self.session = session

        self.path = None
        self.file = None
        self.raw_file = None
        self.encoded = None
        self.descriptors = {}

        self.set_font(family, style, size)

    def _set_family(self, family):
        if family is not None:
            family = family.lower()
            assert family in Families, "%s not a valid font name" % family
            self.family = family
        else:
            self.family = 'arial'

        self.path = Filedict[self.family]

        self.file = TTFontFile()
        ttf = self.file
        self.file.getMetrics(self.path)
        self.descriptors['Ascent'] = int(round(ttf.ascent))
        self.descriptors['Descent'] = int(round(ttf.descent))
        self.descriptors['CapHeight'] = int(round(ttf.capHeight))
        self.descriptors['Flags'] = ttf.flags
        self.descriptors['FontBBox'] = '[%s %s %s %s]' % (
                                       int(round(ttf.bbox[0])),
                                       int(round(ttf.bbox[1])),
                                       int(round(ttf.bbox[2])),
                                       int(round(ttf.bbox[3])))
        self.descriptors['ItalicAngle'] = int(ttf.italicAngle)
        self.descriptors['StemV'] = int(round(ttf.stemV))
        self.descriptors['MissingWidth'] = int(round(ttf.defaultWidth))
        self.name = re.sub('[ ()]', '', ttf.fullName)
        self.type = 'TTF'
        self.character_width = ttf.charWidths

        self.subset = None
        f = open(self.path, 'rb')
        ttfontstream = f.read()
        self.ttfontsize = len(ttfontstream)
        self.fontstream = zlib.compress(ttfontstream)

    def _set_style(self, style=None):
        """ Style should be a string, containing the letters 'B' for bold,
        'U' for underline, or 'I' for italic, or should be None, for no style.
        Symbol will not be underlined. The underline style can further be
        modified by specifying the underline thickness and position.

        """
        if style is None:
            self.style = None
            self.underline = False
        else:
            self.style = style.upper()
            # SetUnderline
            if('U' in self.style):
                self.underline = True

                # Remove U from style string, in case there is a bold / italic
                self.style = self.style.replace("U", "")

                # Does a good job visually representing an underline
                self.Underline_position = round(self.file.underlinePosition)
                self.underline_thickness = round(self.file.underlineThickness)
            else:
                self.underline = False

            # Correct order of bold-italic
            if(self.style == 'IB'):
                self.style = 'BI'

    def _set_size(self, size=None):
        if size is not None:
            self.font_size = float(size)
            self.line_size = self.font_size * 1.2

    def _set_font_key(self):
        if self.style is None:
            self.font_key = self.family
            print "TT font ", self.font_key
        else:
            self.font_key = self.family + self.style

    def _set_character_widths(self):
        pass

    def set_name(self):
        pass

    def set_font(self, family=None, style=None, size=None):
        "Select a font; size given in points"
        self._set_family(family)
        self._set_size(size)
        self._set_style(style)
        self._set_font_key()

    def _set_index(self, index=1):
        """ Index is the number of the font, not the same as
            object number, both are used and set in document.

        """
        self.index = index

    def output(self):
        self.session._out('<</Type /Font')
        self.session._out('/BaseFont /' + self.name)
        self.session._out('/Subtype /TrueType')
        self.session._out('/FirstChar 32 /LastChar 255')
        self.session._out('/Widths %s 0 R' % (self.number + 1))
        self.session._out('/FontDescriptor %s 0 R' % (self.number + 2))

        # if self.encoded is not None:
        #    if self.diff is not None:
        #        self._out('/Encoding '+ str(nf + self.diff) +' 0 R')
        #    else:
        self.session._out('/Encoding /WinAnsiEncoding')
        self.session._out('>>')
        self.session._out('endobj')

        #Widths
        self.session._add_object()
        cw = self.character_width

        s = '['
        for i in xrange(32, 256):
            s += str(cw[ord(chr(i))] or 0) + ' '
        self.session._out(s + ']')
        self.session._out('endobj')

        #Descriptor
        obj = self.session._add_object()
        s = '<</Type /FontDescriptor /FontName /' + self.name
        for k in ('Ascent', 'Descent', 'CapHeight', 'Flags', 'FontBBox', 'ItalicAngle', 'StemV', 'MissingWidth'):
            s += ' /%s %s' % (k, self.descriptors[k])

        s += ' /FontFile2 %s 0 R' % (obj.id + 1)
        self.session._out(s + '>>')
        self.session._out('endobj')

        obj = self.session._add_object()
        #Font file
        self.session._out('<</Length ' + str(len(self.fontstream)))
        self.session._out('/Filter /FlateDecode')
        self.session._out('/Length1 ' + str(self.ttfontsize))
        self.session._out('>>')
        self.session._out(self.fontstream)
        self.session._out('endobj')

    def dict(self):
        return {'i': self.index, 'type': 'core', 'name': self.name, 'up': 100,
                'ut': 50, 'character_width': self.character_width}

    def _equals(self, font):
        if (font.family == self.family) and\
           (font.font_size == self.font_size) and\
           (font.style == self.style):
            ans = True
        else:
            ans = False
        return ans

    def string_width(self, s):
        "Get width of a string in the current font"
        w = 0
        for char in s:
            char = ord(char)
            w += self.character_width[char]
        return w * self.font_size / 1000.0

    def _set_number(self, value):
        "This is the font pdf object number."
        self.number = value

    def set_line_size(self, value):
        "Set line_size"
        self.line_size = value
