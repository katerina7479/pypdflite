

class PDFText(object):
    def __init__(self, session, page, font, color, text):
        self.SS = session
        self.page = page
        self.font = font
        self.color = color
        self.c = page.cursor
        self.text = text

        if self._testLength() is True:
            self._text()
        else:
            self._write()

    def _normalize_text(self):
        self.text = self.text.encode('latin1')

    def _testLength(self, value=None):
        if value is None:
            test = self.c.xfit(self.font.StringWidth(self.text))
        else:
            test = self.c.xfit(self.font.StringWidth(value))
        return test

    def _splitIntoLines(self, text):
        tc = self.c.Copy()  # Test cursor
        textarray = text.split()
        myline = ''
        linearray = []
        for word in textarray:
            segment = myline + ' ' + word
            if tc.xfit(self.font.StringWidth(segment)) is False:
                linearray.append(myline)
                myline = word
                tc.xreset()
            else:
                if myline == '':
                    myline = word
                else:
                    myline += ' %s' % word
        linearray.append(myline)
        return linearray

    def _text(self, value=None):
        if value is not None:
            self.text = value
        self._normalize_text()
        textstring = self._textstring(self.text)
        if self.text != '':
            s = 'BT %.2f %.2f Td %s Tj ET' % (self.c.x, self.c.y, textstring)
            if(self.font.underline):
                s = '%s %s' % (s, self._dounderline())
            if(self.color.color_flag):
                s = 'q %s %s Q' % (self.color.text_color, s)
            #Set Font for text
            fs = 'BT /F%d %.2f Tf ET' % (self.font.index, self.font.fontsize)
            self.SS.out(fs, self.page)
            self.SS.out(s, self.page)
            try:
                self.c.xplus(self.font.StringWidth(self.text))
            except ValueError:
                self._newline()
        else:
            pass

    def _write(self):
        linearray = self._splitIntoLines(self.text)
        test = self.c.yfit(self.font.linesize * len(linearray))
        if test is False:
            self.SS.addPage(self.text)
        else:
            for line in linearray:
                self._text(line)
                self._newline()

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

    def _newline(self):
        self.c.yplus(self.font.linesize)
        self.c.xreset()