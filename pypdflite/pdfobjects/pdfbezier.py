from pdfcursor import PDFCursor
from pdfcolor import PDFColor


class PDFBezier(object):
    def __init__(self, session, page, points, draw_color=None, style="S", stroke="solid"):
        self.session = session
        self.page = page
        self.points = points
        self.style = style
        self.stroke = stroke
        if draw_color is None:
            self.draw_color = PDFColor()
        else:
            self.draw_color = draw_color

        self.stroke = stroke

        for point in points:
            if not isinstance(point, PDFCursor):
                raise Exception("Must be a PDFCursor object", point)


    def draw(self):
        self._set_color()

        s = '%.2f %.2f m' % (self.points[0].x, self.points[0].y_prime)
        self.session._out(s, self.page)

        for point in self.points[1:]:
            self.session._out('%.2f %.2f l' % (point.x, point.y_prime), self.page)
        self.session._out('%s ' % self.style, self.page)

    def _set_color(self):
        self.draw_color._set_type('d')
        if not self.session._compare_color(self.draw_color):
            self.session._out(self.draw_color._get_color_string(), self.page)
            self.session._save_color(self.draw_color.copy())