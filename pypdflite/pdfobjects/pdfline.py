from .pdfdraw import PDFDraw


class PDFLine(PDFDraw):

    def __init__(self, session, page, cursor_start, cursor_end, color=None, stroke=None, size=1):
        super(PDFLine, self).__init__(session, page, color, None, stroke, size=size)
        self.start = cursor_start
        self.end = cursor_end

    def _draw(self):
        self._draw_color()
        if self._stroke is not None:
            self._draw_stroke()
        self._draw_line_size()
        s = '%.2f %.2f m %.2f %.2f l %s' % (
            self.start.x, self.start.y_prime, self.end.x, self.end.y_prime, self._style)
        self.session._out(s, self.page)
