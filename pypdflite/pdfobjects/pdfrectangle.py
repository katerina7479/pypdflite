from pdfcolor import PDFColor


class PDFRectangle(object):

    def __init__(self, session, page, cursor_start, cursor_end, border_color=None, fill_color=None,
                 style='S', size=1):
        self.session = session
        self.page = page
        self.border_color = border_color
        self.fill_color = fill_color

        # S is plain, B is filled with border, F is filled no border.
        self.style_list = ['S', 'B', 'F']

        self._set_dimensions(cursor_start, cursor_end)
        self._set_style(style)
        self._set_size(size)

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

    def _set_size(self, line_size=1):
        self.line_size = line_size
        self.session._out('%.2f w' % self.line_size, self.page)

    def _set_colors(self):
        if isinstance(self.border_color, PDFColor):
            self.border_color._set_type('d')
            if not self.session._compare_color(self.border_color):
                self.session._out(self.border_color._get_color_string(), self.page)
                self.session._save_color(self.border_color.copy())

        if isinstance(self.fill_color, PDFColor):
            self.fill_color._set_type('f')
            if not self.session._compare_color(self.fill_color):
                self.session._out(self.fill_color._get_color_string(), self.page)
                self.session._save_color(self.fill_color.copy())

    def _draw(self):
        self._set_colors()
        s = '%.2f %.2f %.2f %.2f re %s' % (
            self.corner.x, self.corner.y_prime,
            self.width, -self.height, self.style)
        self.session._out(s, self.page)
