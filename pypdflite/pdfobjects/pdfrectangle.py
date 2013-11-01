

class PDFRectangle(object):

    def __init__(self, session, page, color_scheme, cursor_start, cursor_end, size=1, style='S'):
        self.session = session
        self.page = page
        self.color_scheme = color_scheme

        # S is plain, B is filled with border, F is filled no border.
        self.style_list = ['S', 'B', 'F']

        self._set_dimensions(cursor_start, cursor_end)
        self._set_style(style)
        self.set_size(size)
        self.set_color()

    def _set_dimensions(self, cursor_start, cursor_end):
        self.corner = cursor_start
        difference = cursor_end.subtract(cursor_start)

        self.width = difference.x
        self.height = difference.y

    def _set_style(self, style='S'):
        style = style.upper()
        if style in self.style_list:
            self.style = style
        else:
            self.style = 'S'

    def set_size(self, line_size=1):
        self.line_size = line_size
        self.session._out('%.2f w' % self.line_size)

    def set_color(self, color_scheme=None):
        if color_scheme is None:
            self.session._out(self.color_scheme._get_draw_color_string(), self.page)
            self.session._out(self.color_scheme._get_fill_color_string(), self.page)
            print "Did color_scheme in rect", self.color_scheme._get_fill_color_string()
        else:
            self.color_scheme = color_scheme
            self.set_color(None)

    def draw(self):
        s = '%.2f %.2f %.2f %.2f re %s' % (
            self.corner.x, self.corner.y_prime, self.width, self.height, self.style)
        self.session._out(s, self.page)
