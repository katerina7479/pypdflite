from math import cos, tan, sin, pi
import re

class PDFText(object):

    def __init__(self, session, page, text, font=None, color=None, cursor=None, justify='left'):
        self.session = session
        self.page = page
        self.text = text
        self.justify = justify
        self.stale_page = False
        if font is None:
            self.font = self.session.parent.document.font
        else:
            self.font = font
        self.color = color
        if cursor is None:
            self.cursor = page.cursor
        else:
            self.cursor = cursor
        if self._test_x_fit() is True:
            self._set_justification(self.text)
            self._text()
        else:
            self._write()

        if self.font.type == 'TTF':
            self.font._cache_text(self.text)

    def _set_justification(self, text):
        width = self.font._string_width(text)
        if width > 0:
            if self.justify == 'right':
                self.cursor.x = (self.cursor.xmax - width)
            elif self.justify == 'center':
                self.cursor.x = (self.cursor.xmax + self.cursor.xmin - width) / 2.0
            else:
                pass

    def _text(self, value=None):
        if value is not None:
            self.text = value

        # Check to make sure it's not a blank string
        if self.text != '' and self.text is not None:
            # Check to make sure it is not in the top margin.
            if (self.cursor.y - self.font.line_size) < self.cursor.ymin:
                self.cursor.y_plus(self.font.line_size)

            # Check to make sure it will fit before the bottom margin
            if not self.cursor.y_fit(self.font.line_size):
                if hasattr(self, 'line_array'):
                    if self.line_index < len(self.line_array):
                        self.text = ''.join(self.line_array[self.line_index:])
                        self.stale_page = True
                self.session._add_page(self.text)
            else:
                # Escape and put in ()
                text_string = self._text_to_string(self.text)
                
                if getattr(self, '_textMatrix', False):
                    self.text_position(self.cursor.x, self.cursor.y_prime)
                
                s = 'BT '
                s += getattr(self, '_textMatrix', '%.2f %.2f Td ' % (self.cursor.x, self.cursor.y_prime))
                s += ' %s Tj ' % text_string
                s += ' ET'

                # Underline Flag
                if self.font.underline:
                    s = '%s %s' % (s, self._underline())

                # See if the text color is the same as the written
                if self.color is not None:
                    self.color._set_type('t')
                    if not self.session._compare_color(self.color):
                        self.session._out(self.color._get_color_string(), self.page)
                    self.session._save_color(self.color.copy())

                # Set Font for text
                if self.font.is_set is False:
                    fs = 'BT /F%d %.2f Tf ET' % (self.font.index, self.font.font_size)
                    self.font.is_set = True
                    self.session._out(fs, self.page)

                self.session._out(s, self.page)
                try:
                    self.cursor.x_plus(self.font._string_width(self.text))
                except ValueError:
                    self._newline()
        else:
            pass

    def _write(self):
        # Move the y cursor down if it will run into the top margin
        if (self.cursor.y - self.font.line_size) <= self.cursor.ymin:
                self.cursor.y_plus(self.font.line_size)
        # Split array into lines that will fit in the x direction
        self.line_array = self._split_into_lines(self.text)

        # Test length for whole paragraph
        test_length = self.font.line_size * len(self.line_array)
        if self.cursor.y_fit(test_length) is False and (test_length < (self.cursor.ymax - self.cursor.ymin - self.font.line_size)):
            # If the unit won't fit on this page as a whole, but will fit on a new page,
            # then push whole paragraph onto next page
            self.session._add_page(self.text)
        else:
            # Split up the unit into lines, and write them one by one
            self.line_index = 0
            for line in self.line_array[:-1]:
                if self.stale_page:
                    # _text has added a new page, and forwarded remaining lines.
                    break
                self._set_justification(line)
                self._text(line)
                self.line_index += 1
                self._newline()
            if not self.stale_page:
                line = self.line_array[-1]
                self._set_justification(line)
                self._text(line)

    def _test_x_fit(self, value=None):
        if value is None:
            if self.text != '' and self.text is not None:
                test = self.cursor.x_fit(self.font._string_width(self.text))
            else:
                test = True
        else:
            test = self.cursor.x_fit(self.font._string_width(value))
        return test

    def _split_into_lines(self, text):
        test_cursor = self.cursor.copy()  # Test cursor
        text_array = re.split('(\s+)', text)
        myline = ''
        line_array = []
        for word in text_array:
            segment = myline + ' ' + word
            if test_cursor.x_fit(self.font._string_width(segment)) is False:
                line_array.append(myline)
                myline = word
                test_cursor.x_reset()
            else:
                if myline == '':
                    myline = word
                else:
                    myline += '%s' % word
        line_array.append(myline)
        return line_array

    def _text_to_string(self, txt):
        txt = self._escape(txt)
        txt = "(%s)" % txt
        return str(txt)

    @staticmethod
    def _escape(text):
        for i,j in [("\\","\\\\"),(")","\\)"),("(", "\\(")]:
            text = text.replace(i, j)
        return text

    def _underline(self):
        # Underline text
        up = self.font.underline_position
        ut = self.font.underline_thickness
        w = self.font._string_width(self.text)
        s = '%.2f %.2f %.2f %.2f re f' % (self.cursor.x,
            self.cursor.y_prime - up, w, ut)
        return s

    def _newline(self):
        self.cursor.y_plus(self.font.line_size)
        self.cursor.x_reset()

    def _text_transform(self, a, b, c, d, e, f):
        i, j, k, l, m, n = getattr(self, '_currentMatrix', (1., 0., 0., 1., 0., 0.))
        # i j 0    a b 0    i*a + j*c    i*b + j*d    i*0+j*0
        # k l 0 X  c d 0  = k*a + l*c    k*b + l*d    k*0+l*0
        # m n 1    e f 1    m*a + n*c+e  m*b + n*d+f  
        
        a1, b1, c1, d1, e1, f1 = (i * a + j * c, i * b + j * d,
                                  k * a + l * c, k * b + l * d,
                                  m * a + n * c + e, m * b + n * d + f)
        self._textMatrix = '%.2f %.2f %.2f %.2f %.2f %.2f Tm' % (a1, b1, c1, d1, e1, f1)
        #print self._textMatrix
        self._currentMatrix = (a1, b1, c1, d1, e1, f1)

    def text_rotate(self, theta):
        c = cos(theta * pi / 180)
        s = sin(theta * pi / 180)
        self._text_transform(c, s, -s, c, 0., 0.)

    def text_scale(self, x, y):
        self._text_transform(x, 0, 0, y, 0, 0)

    def text_position(self, x, y):
        self._text_transform(1., 0., 0., 1., x, y)

    def text_skew(self, alpha, beta):
        tan_alpha = tan(alpha * pi / 180)
        tan_beta = tan(beta * pi / 180)
        self._text_transform(1, tan_alpha, tan_beta, 1, 0, 0)