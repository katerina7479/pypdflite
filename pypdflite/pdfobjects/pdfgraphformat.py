from pdfcolor import PDFColor


class PDFGraphBackground(object):
    def __init__(self, background_style=None, border_size=None, background_border_color=None, background_fill_color=None, padding=0.0, stroke=None):
        self.style = background_style
        self.size = border_size
        self.border_color = background_border_color
        self.fill_color = background_fill_color
        self.padding = padding
        self.stroke = stroke

        self.default_color_list = [PDFColor(79, 129, 189), PDFColor(192, 80, 77), PDFColor(55, 187, 89),
                                   PDFColor(128, 100, 162), PDFColor(72, 172, 198), PDFColor(247, 150, 70),
                                   PDFColor(208, 146, 167), PDFColor(162, 200, 22), PDFColor(231, 188, 41),
                                   PDFColor(156, 133, 192), PDFColor(243, 164, 71), PDFColor(128, 158, 194)]


    @property
    def exists(self):
        if self.style is None and self.size is None and self.border_color is None and self.fill_color is None:
            return False
        else:
            return True

BasicBackground = PDFGraphBackground("S", 1, PDFColor(), None, 0.1, "solid")