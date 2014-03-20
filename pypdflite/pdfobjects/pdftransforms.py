'''
Created on Mar 16, 2014

@author: tjoneslo
'''

from math import cos, tan, sin, pi

class PDFTransform(object):
    '''
    classdocs
    '''


    def __init__(self, session, page):
        '''
        Constructor
        '''
        self.session = session
        self.page = page

        self._currentMatrix = (1., 0., 0., 1., 0., 0.)
        self._textMatrix = (1., 0., 0., 1., 0., 0.)

    def saveState(self):
        """Save the current graphics state to be restored later by restoreState.
        This saves/restores only the current graphics state on the PDF Page, 
        not in the internal state of the PyPDFLite.
        
        For example:
            canvas.setFont("Helvetica", 20)
            canvas.saveState()
            ...
            canvas.setFont("Courier", 9)
            ...
            canvas.restoreState()
            # if the save/restore pairs match then font is Helvetica 20 again.
        
        
        """
        self.session._out('q', self.page)

    def restoreState(self):
        """restore the graphics state to the matching saved state (see saveState)."""
        self.session._out('Q', self.page)

        
    def transform(self, a, b, c, d, e, f):
        """ Adjust the current transformation state of the current graphics state
        matrix. Not recommended for the faint of heart. 
        """
        a0, b0, c0, d0, e0, f0 = self._currentMatrix
        self._currentMatrix = (a0 * a + c0 * b, b0 * a + d0 * b,
                               a0 * c + c0 * d, b0 * c + d0 * d,
                               a0 * e+ c0 * f + e0, b0 * e + d0 * f + f0)
        a1, b1, c1, d1, e1, f1 = self._currentMatrix
        self.session._out('%.2f %.2f %.2f %.2f %.2f %.2f cm' % (a1, b1, c1, d1, e1, f1), self.page)

    def absolutePosition(self, x, y):
        """return the absolute position of x,y in user space w.r.t. default user space"""
        (a, b, c, d, e, f) = self._currentMatrix
        xp = a * x + c * y + e
        yp = b * x + d * y + f
        return (xp, yp)

    def translate(self, dx, dy):
        """move the origin from the current (0,0) point to the (dx,dy) point
           (with respect to the current graphics state)."""
        self.transform(1, 0, 0, 1, dx, dy)

    def scale(self, x, y):
        """Scale the horizontal dimension by x and the vertical by y
           (with respect to the current graphics state).
           For example canvas.scale(2.0, 0.5) will make everything short and fat."""
        self.transform(x, 0, 0, y, 0, 0)

    def rotate(self, theta):
        """Rotate current graphic state by the angle theta (in degrees)."""
        c = cos(theta * pi / 180)
        s = sin(theta * pi / 180)
        self.transform(c, s, -s, c, 0, 0)

    def skew(self, alpha, beta):
        tanAlpha = tan(alpha * pi / 180)
        tanBeta  = tan(beta  * pi / 180)
        self.transform(1, tanAlpha, tanBeta, 1, 0, 0)
