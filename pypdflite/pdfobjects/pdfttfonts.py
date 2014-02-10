from pdffont import PDFFont
from ttfonts import TTFontFile
import re, zlib
import os
from ..font_loader import Font_Loader


class PDFTTFont(PDFFont):
    def __init__(self, session, family='arial', style=None, size=20):
        self.session = session

        self.FAMILIES = Font_Loader.families
        self.TTFONTS = Font_Loader.font_dict

        self.is_set = False
        self.font_size = None
        self.subset = []

        self.path = None
        self.diffs = None
        self.diff_number = None
        self.encoded = None
        self.descriptors = {}

        self._set_font(family, style, size)
        self._cache_text("""abcdefghijklmnopqrstuvwxyz
                        ABCDEFGHIJKLMNOPQRSTUVWXYZ
                        1234567890-,.<>/?;:\'\"\\[]{}
                        =+_!@#$%^&*()~`""")

    def _set_family(self, family):
        if family is not None:
            family = family.lower()
            if family not in self.TTFONTS:
                raise Exception("%s not a valid font name" % family)
            self.family = family
        else:
            self.family = 'arial'

    def _set_name(self):
        self.name = self.font_key + self.style

    def _set_character_widths(self):
        pass

    def _set_font(self, family=None, style=None, size=None):
        "Select a font; size given in points"
        if style is not None:
            if 'B' in style:
                family += '_bold'
            if 'I' in style:
                family += '_italic'

        self._set_family(family)
        self._get_diffs()
        self._set_style(style)
        self._set_metrics()
        self._set_size(size)
        self._set_font_key()

    def _set_metrics(self):
        self.path = self.TTFONTS[self.family]

        self.info_object = TTFontFile()
        ttf = self.info_object
        ttf.getMetrics(self.path)
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
        self.character_widths = ttf.charWidths

    def _get_diffs(self):
        pass

    def _string_width(self, s):
        "Get width of a string in the current font"
        s = str(s)
        w = 0
        for char in s:
            char = ord(char)
            w += self.character_widths[char]
        return w * self.font_size / 1000.0

    def _output(self):
        self.session._out('<</Type /Font')
        self.session._out('/BaseFont /' + self.name)
        self.session._out('/Subtype /TrueType')
        self.session._out('/FirstChar 32 /LastChar 255')
        self.session._out('/Widths %s 0 R' % (self.number + 1))
        self.session._out('/FontDescriptor %s 0 R' % (self.number + 2))

        if self.diff_number is not None:
            self.session._out('/Encoding %s 0 R' % (self.diff_number + self.session.get_saved_number))
        else:
            self.session._out('/Encoding /WinAnsiEncoding')
        self.session._out('>>')
        self.session._out('endobj')

        self._output_character_widths()
        self._output_descriptors()
        self._output_file()

    def _output_character_widths(self):
        #Widths
        self.session._add_object()
        cw = self.character_widths
        s = '['
        for i in xrange(32, 256):
            try:
                s += str(cw[i]) + ' '
            except:
                s += '0 '
        self.session._out(s + ']')
        self.session._out('endobj')

    def _output_descriptors(self):
        #Descriptor
        obj = self.session._add_object()
        self.session._out('<</Type /FontDescriptor /FontName /%s' % self.name)
        s = ''
        for k in self.descriptors:
            s += ' /%s %s' % (k, self.descriptors[k])

        s += ' /FontFile2 %s 0 R' % (obj.id + 1)
        self.session._out(s + '>>')
        self.session._out('endobj')

    def _output_file(self):
        self.file = self.info_object.makeSubset(self.path, self.subset)
        self.length1 = len(self.file)
        self.file = zlib.compress(self.file)
        self.length = len(self.file)

        obj = self.session._add_object()
        self.session._out('<</Length ' + str(self.length))
        self.session._out('/Filter /FlateDecode')
        self.session._out('/Length1 ' + str(self.length1))
        self.session._out('>>')
        self.session._put_stream(self.file)
        self.session._out('endobj')

    def _cache_text(self, text):
        txt_unicode = [ord(c) for c in text]
        for uni in txt_unicode:
            if uni not in self.subset:
                self.subset.append(uni)
