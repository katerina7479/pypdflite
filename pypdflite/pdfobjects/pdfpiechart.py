from pdfcolor import PDFColor
from pdfcursor import PDFCursor
import math
from pdftext import PDFText
from pdfarc import PDFArc
from pdfellipse import PDFEllipse


class PDFPieChart(object):
    """
    Create a pie chart from data dict(series labels)

    """
    def __init__(self, session, page, data, center_cursor, radius, fill_colors=None, labels=False):
        self.session = session
        self.page = page
        self.data = data
        self.center_cursor = center_cursor
        self.radius = radius
        self.stroke = "S"
        self.fill_colors = fill_colors
        self.labels = labels

        self.get_colors()
        self.draw_base_circle()
        self.draw_data()

    def get_colors(self):
        if self.fill_colors is None:
            self.fill_colors = [PDFColor(79, 129, 189), PDFColor(192, 80, 77), PDFColor(55, 187, 89),
                                PDFColor(128, 100, 162), PDFColor(72, 172, 198), PDFColor(247, 150, 70),
                                PDFColor(208, 146, 167), PDFColor(231, 188, 41), PDFColor(156, 133, 192),
                                PDFColor(243, 164, 71), PDFColor(128, 158, 194)]

        for color in self.fill_colors:
            color._set_type("f")

    def draw_base_circle(self):
        circle = PDFEllipse(self.session, self.page, self.center_cursor, PDFCursor(self.radius, self.radius), PDFColor(77, 77, 77), None, "solid", "S", 1)
        circle._draw()

    def draw_data(self):
        start_angle = 0
        i = 0
        for pair in self.data:
            arc_angle = round(360 * (pair[1] / 100.0), 2)
            arc = PDFArc(self.session, self.page, self.center_cursor, self.radius, start_angle, arc_angle, False, None, None, self.fill_colors[i], "solid", "F", 1)
            start_angle = math.degrees(arc.end_angle)
            arc._draw()
            i += 1
            if i > len(self.fill_colors):
                i = 0