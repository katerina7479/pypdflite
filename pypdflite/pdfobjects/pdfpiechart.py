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
        self.base_color = PDFColor(77, 77, 77)

        self.get_colors()
        self.draw_base_circle()
        self.draw_data()

    def get_colors(self):
        if self.fill_colors is None:
            self.fill_colors = [PDFColor(79, 129, 189), PDFColor(192, 80, 77), PDFColor(55, 187, 89),
                                PDFColor(128, 100, 162), PDFColor(72, 172, 198), PDFColor(247, 150, 70),
                                PDFColor(208, 146, 167), PDFColor(162, 200, 22), PDFColor(231, 188, 41),
                                PDFColor(156, 133, 192), PDFColor(243, 164, 71), PDFColor(128, 158, 194)]

        for color in self.fill_colors:
            color._set_type("f")

    def draw_base_circle(self):
        circle = PDFEllipse(self.session, self.page, self.center_cursor, PDFCursor(self.radius, self.radius), self.base_color, None, "solid", "S", 1)
        circle._draw()

    def draw_label(self, text):
        self.session.parent.document.set_font_size(10)
        if self.test_angle < 90:
            self.point_cursor.x_plus(-3)
        if self.test_angle > 90 and self.test_angle < 250:
            width = self.session.parent.document.font._string_width(text)
            self.point_cursor.x_plus(-(width))
        if self.test_angle > 180 and self.test_angle < 250:
            self.point_cursor.x_plus(-4)
            self.point_cursor.y_plus(2)
        if self.test_angle > 250 and self.test_angle < 270:
            self.point_cursor.y_plus(12)
        if self.test_angle > 270 and self.test_angle < 360:
            self.point_cursor.y_plus(8)
            self.point_cursor.x_plus(2)

        PDFText(self.session, self.page, text, color=self.base_color, cursor=self.point_cursor)

    def draw_data(self):
        start_angle = 0
        i = 0
        for pair in self.data:
            arc_angle = round(360 * (pair[1] / 100.0), 2)
            arc = PDFArc(self.session, self.page, self.center_cursor, self.radius, start_angle, arc_angle, False, None, None, self.fill_colors[i], "solid", "F", 1)
            if self.labels:
                self.point_cursor = arc.curves[0]["p1"].copy()
                self.test_angle = start_angle
            start_angle = math.degrees(arc.end_angle)
            arc._draw()
            if self.labels:
                self.draw_label(pair[0])
            i += 1
            if i > len(self.fill_colors):
                i = 0