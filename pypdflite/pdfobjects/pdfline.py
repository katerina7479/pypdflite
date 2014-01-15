

class PDFLine(object):

    def __init__(self, session, page, cursor_start, cursor_end, color_scheme=None, style=None, size=1):
        self.session = session
        self.start = cursor_start
        self.end = cursor_end

        self.page = page

        if color_scheme is None:
            self.color_scheme = self.session.parent.document.color_scheme
        else:
            self.color_scheme = color_scheme
        self.set_size(size)
        self.set_color()
        self.set_style(style)

    def set_size(self, line_size=1):
        self.line_size = line_size

    def set_color(self, color_scheme=None):
        if color_scheme is None:
            self.session._out(
                self.color_scheme._get_draw_color_string(), self.page)
        else:
            self.color_scheme = color_scheme
            self.set_color(None)

    def set_style(self, style=None):
        if style == "dashed" or style == 1:
            self.style = "dashed"
        else:
            self.style = "solid"

    def draw_style(self):
        if self.style == "dashed":
            self.session._out('[%s] %s d' % (3, 0), self.page)
        elif (self.style == "solid"):
            self.session._out('[] 0 d', self.page)

    def draw_line_size(self):
        self.session._out('%.2f w' % self.line_size, self.page)

    def draw(self):
        if self.style is not None:
            self.draw_style()
        self.draw_line_size()
        s = '%.2f %.2f m %.2f %.2f l S' % (
            self.start.x, self.start.y_prime, self.end.x, self.end.y_prime)
        self.session._out(s, self.page)
