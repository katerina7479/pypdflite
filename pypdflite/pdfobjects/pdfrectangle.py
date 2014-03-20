from pdfdraw import PDFDraw


class PDFRectangle(PDFDraw):

    def __init__(self, session, page, cursor_start, cursor_end, border_color=None, fill_color=None,
                 style=None, stroke=None, size=1):
        super(PDFRectangle, self).__init__(session, page, border_color, style, stroke, size)

        self.fill_color = fill_color
        self._set_dimensions(cursor_start, cursor_end)

    def _set_dimensions(self, cursor_start, cursor_end):
        self.corner = cursor_start
        difference = cursor_end - cursor_start

        self.width = difference.x
        self.height = difference.y

    def _draw(self):
        self._draw_colors()
        self._draw_line_size()
        s = '%.2f %.2f %.2f %.2f re %s' % (
            self.corner.x, self.corner.y_prime,
            self.width, -self.height, self.stroke)
        self.session._out(s, self.page)
