"""
Created on Mar 15, 2014

@author: tjoneslo
"""
from pdfcolor import PDFColor


class PDFDraw(object):
    """
    Base class for the drawing classes: PDFLine, PDFRectangle, PDFEllipse
    """
    def __init__(self, session, page, color=None, style=None, stroke=None, size=1):
        # S is plain, B is filled with border, F is filled no border.
        self.style_list = ['S', 'B', 'F']
        self.stroke_list = ['solid', 'dashed', 'dots']

        self.session = session
        self.page = page
        self.color = color
        self._set_size(size)
        self._set_style(style)
        self._set_stroke(stroke)
        self.fill_color = None

    def _set_size(self, line_size=1):
        self.line_size = line_size

    def _set_style(self, style=None):
        if style in self.stroke_list:
            raise Exception("Style in stroke list : %s" % style)
        style = style.upper() if style is not None else 'S'
        self._style = style if style in self.style_list else 'S'

    def _set_stroke(self, stroke='solid'):
        if stroke in self.style_list:
            raise Exception("Stroke in style list : %s" % stroke)
        if stroke == "dashed" or stroke == 1:
            self._stroke = "dashed"
        elif stroke == 'dots' or stroke == 2:
            self._stroke = 'dots'
        else:
            self._stroke = "solid"

    def _draw_color(self):
        if isinstance(self.color, PDFColor):
            self.color._set_type('d')
            if not self.session._compare_color(self.color):
                self.session._out(self.color._get_color_string(), self.page)
                self.session._save_color(self.color.copy())

    def _draw_colors(self):
        self._draw_color()
        if isinstance(self.fill_color, PDFColor):
            self.fill_color._set_type('f')
            if not self.session._compare_color(self.fill_color):
                self.session._out(self.fill_color._get_color_string(), self.page)
                self.session._save_color(self.fill_color.copy())

    def _draw_stroke(self):
        if self._stroke == "dashed":
            self.session._out('[%s] %s d' % (3, 0), self.page)
        elif self._stroke == "solid":
            self.session._out('[] 0 d', self.page)
        elif self._stroke == 'dots':
            self.session._out('[%s] %s d' % (1, 1), self.page)

    def _draw_line_size(self):
        self.session._out('%.2f w' % self.line_size, self.page)

    def _draw(self):
        raise NotImplementedError

