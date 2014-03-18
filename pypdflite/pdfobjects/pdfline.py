
from pdfdraw import PDFDraw

class PDFLine(PDFDraw):

    def __init__(self, session, page, cursor_start, cursor_end, color=None, style=None, size=1):
        super(PDFLine, self).__init__(session, page, color, style, size=size)
        self.start = cursor_start
        self.end = cursor_end


    def _draw(self):
        self._draw_color()
        if self.style is not None:
            self._draw_style()
        self._draw_line_size()
        s = '%.2f %.2f m %.2f %.2f l %s' % (
            self.start.x, self.start.y_prime, self.end.x, self.end.y_prime, self.stroke)
        self.session._out(s, self.page)
