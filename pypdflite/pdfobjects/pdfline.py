

class PDFLine(object):

    def __init__(self, session, page, cursor_start, cursor_end, color=None, style=None, size=1):
        self.session = session
        self.start = cursor_start
        self.end = cursor_end

        self.page = page

        self.color = color
        self.set_size(size)
        self.set_style(style)

    def set_size(self, line_size=1):
        self.line_size = line_size

    def draw_color(self):
        if self.color is not None:
            self.color.set_type('d')
            self.session._out(self.color._get_color_string(), self.page)

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
        self.draw_color()

        if self.style is not None:
            self.draw_style()
        self.draw_line_size()
        s = '%.2f %.2f m %.2f %.2f l S' % (
            self.start.x, self.start.y_prime, self.end.x, self.end.y_prime)
        self.session._out(s, self.page)
