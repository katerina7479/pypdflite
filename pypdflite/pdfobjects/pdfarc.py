from pdfdraw import PDFDraw
from pdfcursor import PDFCursor
import math

class PDFArc(PDFDraw):
    """
    Draw an arc using the Bezier Cubic Splines
    present in the PDF primitives.
    See: http://www.tinaja.com/glib/ellipse4.pdf
    """

    def __init__(self, session, page, cursor_center, radius, start_angle, arc_angle, inverted, border_color=None, fill_color=None, style=None, stroke=None, size=1):
        super(PDFArc, self).__init__(session, page, border_color, style, stroke, size)
        """Draws an arc counter-clockwise from start. Accepts angles in degrees, converts to radians """
        self.center = cursor_center
        self.radius = radius
        self.start_angle = math.radians(start_angle)
        self.end_angle = math.radians(arc_angle + start_angle)
        self.magic = 0.55
        self.l = self.magic * self.radius
        self.fill_color = fill_color
        self._get_points()

    def get_coord_from_theta(self, theta):
        x = self.center.x + self.radius * math.cos(theta)
        y = self.center.y - self.radius * math.sin(theta)
        return PDFCursor(x, y)

    def get_coord_from_beta(self, beta):
        hyp = math.sqrt(self.radius ** 2 + self.l ** 2)
        x = self.center.x - hyp * math.sin(beta)
        y = self.center.y + hyp * math.cos(beta)
        return PDFCursor(x, y)

    def _get_points(self):
        self.start = self.get_coord_from_theta(self.start_angle)
        self.end = self.get_coord_from_theta(self.end_angle)
        theta2 = math.asin(self.magic)

        self.p1 = self.get_coord_from_theta(theta2 + self.start_angle)
        self.p2 = self.get_coord_from_beta(180 - self.end_angle + theta2)

    def _draw(self):
        self._draw_colors()
        self._draw_line_size()

        # Starting point
        s = '%.2f %.2f m' % (self.center.x, self.center.y_prime)
        self.session._out(s, self.page)
        s = '%.2f %.2f l' % (self.start.x, self.start.y_prime)
        self.session._out(s, self.page)

        print self.p1.x, self.p1.y, self.p2.x, self.p2.y

        s = '%.2f %.2f %.2f %.2f %.2f %.2f c' % (self.p1.x, self.p1.y, self.p2.x, self.p2.y, self.end.x, self.end.y_prime)
        self.session._out(s, self.page)
        #s = '%.2f %.2f %.2f %.2f %.2f %.2f c' % (x+xmagic, y+yradius, x+xradius, y+ymagic, x+xradius, y)
        #self.session._out(s, self.page)
        #s = '%.2f %.2f %.2f %.2f %.2f %.2f c' % (x+xradius, y-ymagic, x+xmagic, y-yradius, x, y-yradius)
        #self.session._out(s, self.page)
        #s = '%.2f %.2f %.2f %.2f %.2f %.2f c' % (x-xmagic, y-yradius, x-xradius, y-ymagic, x-xradius, y)
        #self.session._out(s, self.page)

        self.session._out(" h", self.page)

        s = '%s' % self.stroke
        self.session._out(s, self.page)