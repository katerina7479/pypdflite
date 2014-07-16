"""
Created on Mar 15, 2014

@author: tjoneslo
"""
from pdfdraw import PDFDraw


class PDFEllipse(PDFDraw):
    """
    Draw an ellipse or circle using the Bezier Cubic Splines
    present in the PDF primitives.
    See: http://www.tinaja.com/glib/ellipse4.pdf
    """

    def __init__(self, session, page, cursor_center, cursor_radius, border_color=None, fill_color=None, style=None, stroke=None, size=1):
        super(PDFEllipse, self).__init__(session, page, border_color, style, stroke, size)
        self.center = cursor_center
        self.radius = cursor_radius
        self.magic = 0.551787
        self.fill_color = fill_color

    def _draw(self):
        self._draw_colors()
        self._draw_line_size()
        xmagic = self.radius.x * self.magic
        ymagic = self.radius.y * self.magic
        xradius = self.radius.x
        yradius = self.radius.y
        x = self.center.x
        y = self.center.y_prime
        
        s = '%.2f %.2f m' % (self.center.x - xradius, self.center.y_prime)
        self.session._out(s, self.page)

        s = '%.2f %.2f %.2f %.2f %.2f %.2f c' % (x-xradius, y+ymagic, x-xmagic, y+yradius, x, y+yradius)
        self.session._out(s, self.page)
        s = '%.2f %.2f %.2f %.2f %.2f %.2f c' % (x+xmagic, y+yradius, x+xradius, y+ymagic, x+xradius, y)
        self.session._out(s, self.page)
        s = '%.2f %.2f %.2f %.2f %.2f %.2f c' % (x+xradius, y-ymagic, x+xmagic, y-yradius, x, y-yradius)
        self.session._out(s, self.page)
        s = '%.2f %.2f %.2f %.2f %.2f %.2f c' % (x-xmagic, y-yradius, x-xradius, y-ymagic, x-xradius, y)
        self.session._out(s, self.page)
        s = '%s' % self._style
        self.session._out(s, self.page)