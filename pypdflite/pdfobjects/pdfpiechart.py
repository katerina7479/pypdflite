from pdfcolor import PDFColor
from pdfcursor import PDFCursor
import math
from pdftext import PDFText
from pdfarc import PDFArc
from pdfellipse import PDFEllipse
from pdfgraph import PDFGraph
from pdfrectangle import PDFRectangle


class PDFPieChart(PDFGraph):
    """
    Create a pie chart from data dict(series labels)

    """
    def __init__(self, session, page, data, cursor, width, height, title, data_type="raw", fill_colors=None, labels=False,
                 background=None, legend=None):
        super(PDFPieChart, self).__init__(session, page, cursor, width, height, title, background, legend)
        self._parse_data(data, data_type)
        self._set_center()
        self.style = "S"
        self.fill_colors = fill_colors
        self.labels = labels
        self.base_color = PDFColor(77, 77, 77)

        self.get_colors()
        self.draw_base_circle()
        self.draw_data()

    def _parse_data(self, data, data_type):
        if data_type == "raw":
            total = 0
            for pair in data:
                total += pair[1]
            percent_data = []
            for pair in data:
                percent_data.append((pair[0], (pair[1] / float(total)) * 100))
            data = percent_data
        elif data_type == "percent":
            pass
        else:
            raise ValueError("Data must be raw or percent")

        formatted_data = []
        for pair in data:
            formatted_data.append((pair[0], pair[1], "%.1f%%" % pair[1]))

        # Sort
        self.data = sorted(formatted_data, key=lambda x: x[1], reverse=True)

    def _set_center(self):
        self.center_cursor = PDFCursor(self.origin.x + self.width / 2.0, self.origin.y - self.height / 2.0)
        self.radius = min(self.width, self.height) / 2.0

    def get_colors(self):
        if self.fill_colors is None:
            self.fill_colors = self.background.default_color_list

        for color in self.fill_colors:
            color._set_type("f")

    def draw_base_circle(self):
        circle = PDFEllipse(self.session, self.page, self.center_cursor, PDFCursor(self.radius, self.radius), self.base_color, None, style="S", stroke="solid", size=1)
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
        if self.legend is not None:
            self._legend_line_height = self.session.parent.document.font.font_size
            self.legend_start_cursor.x_plus(-self.padding[0] * 0.5)
            self.legend_width += self.padding[0] * 0.55
            self._draw_legend_title()
        start_angle = 0
        i = 0
        for pair in self.data:
            if self.legend is not None:
                self._draw_legend_line(i, pair[0])
            arc_angle = round(360 * (pair[1] / 100.0), 2)
            arc = PDFArc(self.session, self.page, self.center_cursor, self.radius, start_angle, arc_angle, False, None, None, self.fill_colors[i], "F", "solid", 1)
            if self.labels:
                self.point_cursor = arc.curves[0]["p1"].copy()
                self.test_angle = start_angle
            start_angle = math.degrees(arc.end_angle)
            arc._draw()
            if self.labels and self.legend is None:
                self.draw_label(pair[0])
            i += 1
            if i > len(self.fill_colors):
                i = 0
        if self.legend is not None:
            self.legend_data_start.y_plus(-1.75 * self._legend_line_height)
            self._draw_legend_box()

    def _draw_legend_line(self, index, series_name):
        end = PDFCursor(self.legend_data_start.x + 10, self.legend_data_start.y + 10)
        box = PDFRectangle(self.session, self.page, self.legend_data_start, end, None, self.fill_colors[index], style="F", stroke="solid")
        box._draw()
        end.x_plus(10)
        text = PDFText(self.session, self.page, series_name, cursor=end, color=self.base_color)
        self.legend_data_start.y_plus(1.75 * self._legend_line_height)