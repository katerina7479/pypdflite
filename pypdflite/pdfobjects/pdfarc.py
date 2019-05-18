import math
from .pdfdraw import PDFDraw
from .pdfcursor import PDFCursor


class PDFArc(PDFDraw):
    """
    Draw an arc using the Bezier Cubic Splines
    present in the PDF primitives.
    """

    def __init__(self, session, page, cursor_center, radius, start_angle, arc_angle, inverted, end_angle=None, border_color=None, fill_color=None, style=None, stroke=None, size=1):
        super(PDFArc, self).__init__(session, page, border_color, style, stroke, size)
        """Draws an arc counter-clockwise from start. Accepts angles in degrees, converts to radians """
        self.center = cursor_center
        self.radius = radius
        self.inverted = inverted
        self.get_angles(start_angle, arc_angle, end_angle)

        self.fill_color = fill_color
        self.createArc()

    def get_angles(self, start_angle, arc_angle, end_angle):
        if end_angle is not None:
            self.start_angle = math.radians(start_angle)
            self.end_angle = math.radians(end_angle)
            if self.inverted:
                self.start_angle = math.radians(start_angle)
                self.end_angle = math.radians(end_angle)
        else:
            if self.inverted:
                self.start_angle = math.radians(start_angle + arc_angle)
                self.end_angle = math.radians(start_angle)
            else:
                self.start_angle = math.radians(start_angle)
                self.end_angle = math.radians(start_angle + arc_angle)
        if self.end_angle == math.pi * 2:
            self.end_angle = math.pi * 2 - 0.001

    def createArc(self):
        TWO_PI = math.pi * 2
        PI_OVER_TWO = math.pi / 2.0

        self._start_angle = self.start_angle % TWO_PI
        self._end_angle = self.end_angle % TWO_PI

        self.curves = []

        a1 = self._start_angle
        if self.inverted:
            totalAngle = min(TWO_PI, TWO_PI - abs(self._end_angle - self._start_angle))
        else:
            totalAngle = min(TWO_PI, abs(self._end_angle - self._start_angle))
        while totalAngle > 0.01:
            a2 = a1 + min(totalAngle, PI_OVER_TWO)
            self.curves.append(self.createSmallArc(self.radius, a1, a2))
            totalAngle -= abs(a2-a1)
            a1 = a2

    def createSmallArc(self, radius, a1, a2):
        a = (a2 - a1) / 2.0
        x4 = radius * math.cos(a)
        y4 = radius * math.sin(a)
        x1 = x4
        y1 = -y4

        q1 = x1**2 + y1**2
        q2 = q1 + x1*x4 + y1*y4
        k2 = (4.0/3.0) * (math.sqrt(2 * q1 * q2) - q2) / (x1 * y4 - y1 * x4)

        x2 = x1 - k2 * y1
        y2 = y1 + k2 * x1
        x3 = x2
        y3 = -y2

        ar = a + a1
        cos_ar = math.cos(ar)
        sin_ar = math.sin(ar)

        return {
            "p0": PDFCursor(self.center.x + (radius * math.cos(a1)), self.center.y - radius * math.sin(a1)),
            "p1": PDFCursor(self.center.x + (x2 * cos_ar - y2 * sin_ar), self.center.y - (x2 * sin_ar + y2 * cos_ar)),

            "p2": PDFCursor(self.center.x + (x3 * cos_ar - y3 * sin_ar), self.center.y - (x3 * sin_ar + y3 * cos_ar)),
            "p3": PDFCursor(self.center.x + (radius * math.cos(a2)), self.center.y - (radius * math.sin(a2)))
        }

    def _draw(self):
        self._draw_colors()
        self._draw_line_size()

        # Starting point
        s = '%.2f %.2f m' % (self.center.x, self.center.y_prime)
        self.session._out(s, self.page)
        s = '%.2f %.2f l' % (self.curves[0]["p0"].x, self.curves[0]["p0"].y_prime)
        self.session._out(s, self.page)

        for curve in self.curves:
            s = '%.2f %.2f %.2f %.2f %.2f %.2f c' % (curve["p1"].x, curve["p1"].y_prime, curve["p2"].x, curve["p2"].y_prime, curve["p3"].x, curve["p3"].y_prime)
            self.session._out(s, self.page)

        self.session._out(" h", self.page)

        s = '%s' % self._style
        self.session._out(s, self.page)