

class PDFLine(object):

    def __init__(self, session, page, color_scheme, cursor_start, cursor_end, size=1):
        self.session = session
        self.start = cursor_start
        self.end = cursor_end

        self.page = page

        self.color_scheme = color_scheme
        self.set_size(size)
        self.set_color()

    def set_size(self, line_size=1):
        self.line_size = line_size
        self.session._out('%.2f w' % self.line_size)

    def set_color(self, color_scheme=None):
        if color_scheme is None:
            self.session._out(
                self.color_scheme._get_draw_color_string(), self.page)
        else:
            self.color_scheme = color_scheme
            self.set_color(None)

    def draw(self):
        s = '%.2f %.2f m %.2f %.2f l S' % (
            self.start.x, self.start.y, self.end.x, self.end.y)
        self.session._out(s, self.page)
