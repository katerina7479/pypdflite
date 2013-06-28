

class PDFText(object):
    def __init__(self, session, page, font, color, text):
        self.SS = session
        self.page = page
        self.font = font
        self.color = color
        self.c = page.cursor
        self.text = text
        self._text()

    def _normalize_text(self):
        "Check that text input is in the correct format/encoding"
        self.text = self.text.encode('latin1')

    def _text(self):
        "Output a string"
        self._normalize_text()
        textstring = self._textstring(self.text)
        if self.text != '':
            s = 'BT %.2f %.2f Td %s Tj ET' % (self.c.x, self.c.y, textstring)
            if(self.font.underline):
                s = '%s %s' % (s, self._dounderline())
            if(self.color.color_flag):
                s = 'q %s %s Q' % (self.color.text_color, s)
        #Set Font for text
        fs = 'BT /F%d %.2f Tf ET' % (self.font.index, self.font.font_size)
        self.SS.out(fs, self.page)
        self.SS.out(s, self.page)
        self.c.xplus(self.font.StringWidth(self.text))

    def _textstring(self, txt):
        txt = self._escapetext(txt)
        txt = "(%s)" % txt
        return str(txt)

    def _escapetext(self, text):
        for i, j in {"\\": "\\\\", ")": "\\)", "(": "\\("}.iteritems():
            text = text.replace(i, j)
        return text

    def _dounderline(self):
        #Underline text
        up = self.font.underlineposition
        ut = self.font.underlinethickness
        w = self.font.StringWidth(self.text)
        s = '%.2f %.2f %.2f %.2f re f' % (self.c.x, self.c.y-up, w, ut)
        return s
