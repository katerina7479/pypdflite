

class PDFLine(object):

    def __init__(self, session, page, cursor_start, cursor_end, color=None, style=None, size=1):
        self.session = session
        self.start = cursor_start
        self.end = cursor_end

        self.page = page

        self.color = color
        self._set_size(size)
        self._set_style(style)

    def _set_size(self, line_size=1):
        self.line_size = line_size

    def _set_style(self, style=None):
        if style == "dashed" or style == 1:
            self.style = "dashed"
        else:
            self.style = "solid"

    def _draw_color(self):
        if self.color is not None:
            self.color._set_type('d')
            if not self.session._compare_color(self.color):
                self.session._out(self.color._get_color_string(), self.page)
                self.session._save_color(self.color.copy())

    def _draw_style(self):
        if self.style == "dashed":
            self.session._out('[%s] %s d' % (3, 0), self.page)
        elif (self.style == "solid"):
            self.session._out('[] 0 d', self.page)

    def _draw_line_size(self):
        self.session._out('%.2f w' % self.line_size, self.page)

    def _draw(self):
        self._draw_color()

        if self.style is not None:
            self._draw_style()
        self._draw_line_size()
        s = '%.2f %.2f m %.2f %.2f l S' % (
            self.start.x, self.start.y_prime, self.end.x, self.end.y_prime)
        self.session._out(s, self.page)
