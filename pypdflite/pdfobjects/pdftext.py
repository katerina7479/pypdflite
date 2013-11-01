        # Note (not written, if color flag is True, then the string must be wrapped for output as follows:
        # s = 'q ' + s (from here) + ' ' + text s + ' Q'


class PDFText(object):

    def __init__(self, session, page, font, color_scheme, text):
        self.session = session
        self.page = page
        self.font = font
        self.color_scheme = color_scheme
        self.cursor = page.cursor
        self.text = text

        if self._test_x_fit() is True:
            self._text()
        else:
            self._write()

    def _normalize_text(self):
        self.text = self.text.encode('latin1')

    def _test_x_fit(self, value=None):
        if value is None:
            test = self.cursor.x_fit(self.font.string_width(self.text))
        else:
            test = self.cursor.x_fit(self.font.string_width(value))
        return test

    def _split_into_lines(self, text):
        test_cursor = self.cursor.copy()  # Test cursor
        text_array = text.split()
        myline = ''
        line_array = []
        for word in text_array:
            segment = myline + ' ' + word
            if test_cursor.x_fit(self.font.string_width(segment)) is False:
                line_array.append(myline)
                myline = word
                test_cursor.x_reset()
            else:
                if myline == '':
                    myline = word
                else:
                    myline += ' %s' % word
        line_array.append(myline)
        return line_array

    def _text(self, value=None):
        if value is not None:
            self.text = value
        self._normalize_text()
        text_string = self._text_to_string(self.text)
        if self.text != '':
            s = 'BT %.2f %.2f Td %s Tj ET' % (self.cursor.x, self.cursor.y, text_string)
            if(self.font.underline):
                s = '%s %s' % (s, self._underline())
            # Only called if text != fill colors in current scheme
            if(self.color_scheme._get_color_flag()):
                s = 'q %s %s Q' % (self.color._get_text_color_string(), s)
            # Set Font for text
            fs = 'BT /F%d %.2f Tf ET' % (self.font.index, self.font.font_size)
            self.session._out(fs, self.page)
            self.session._out(s, self.page)
            try:
                self.cursor.x_plus(self.font.string_width(self.text))
            except ValueError:
                self._newline()
        else:
            pass

    def _write(self):
        line_array = self._split_into_lines(self.text)
        test = self.cursor.y_fit(self.font.line_size * len(line_array))
        if test is False:
            self.session._add_page(self.text)
        else:
            for line in line_array:
                self._text(line)
                self._newline()

    def _text_to_string(self, txt):
        txt = self._escape(txt)
        txt = "(%s)" % txt
        return str(txt)

    def _escape(self, text):
        for i, j in {"\\": "\\\\", ")": "\\)", "(": "\\("}.iteritems():
            text = text.replace(i, j)
        return text

    def _underline(self):
        # Underline text
        up = self.font.underline_position
        ut = self.font.underline_thickness
        w = self.font.string_width(self.text)
        s = '%.2f %.2f %.2f %.2f re f' % (self.cursor.x, self.cursor.y - up, w, ut)
        return s

    def _newline(self):
        self.cursor.y_plus(self.font.line_size)
        self.cursor.x_reset()
