from pdfgraph import PDFGraph
from pdfcolor import PDFColor
from pdfcursor import PDFCursor
from pdfline import PDFLine
from pdftext import PDFText
from pdfellipse import PDFEllipse
from pdflinegraph import PDFLineGraph


class PDFXYScatter(PDFLineGraph):
    def __init__(self, session, page, cursor, data, width, height, title, x_axis_limits, y_axis_limits, frequency, axis_titles, axis_labels, line_colors,
                 background=None, legend=None, dots=None, linear_regression=None, linear_regression_equation=None):
        self.linear_regression = linear_regression
        self.linear_regression_equation = linear_regression_equation
        super(PDFXYScatter, self).__init__(session, page, cursor, data, width, height, title, x_axis_limits, y_axis_limits, frequency, axis_titles, axis_labels, line_colors,
                                           background, legend, dots)

    def draw_data(self):
        if self.legend is not None:
            self._draw_legend_title()

        i = 0
        for series in self.data:
            self._set_color(i)
            if self.legend is not None:
                self._draw_legend_line(i, series.keys()[0])
                i += 1

            for values in series.itervalues():
                cursors = []
                for pair in values:
                    cursor = self.get_coord(pair)
                    cursors.append(cursor)
                self._draw_dots(cursors)

        if self.legend is not None:
            self._draw_legend_box()

    def _draw_legend_line(self, index, series_name):
        line_height = self.session.parent.document.font.font_size
        end = PDFCursor(self.legend_data_start.x + 15, self.legend_data_start.y)
        line = PDFLine(self.session, self.page, self.legend_data_start, end, color=self.line_colors[index])
        line._draw()
        end.x_plus(10)
        end.y_plus(0.25 * line_height)
        text = PDFText(self.session, self.page, series_name, cursor=end)
        self.legend_data_start.y_plus(1.75 * line_height)

    def _draw_dots(self, cursors):
        if self.linear_regression:
            self.linear_regression_line = LinearRegressionLine()
        if self.dots is not None:
            for cursor in cursors:
                dot = PDFEllipse(self.session, self.page, cursor, PDFCursor(self.dots, self.dots), style="F")
                dot._draw()
                if self.linear_regression:
                    self.linear_regression_line.add_coord(cursor)
            if self.linear_regression:
                self.linear_regression_line.calculate_line()
                cursor1, cursor2 = self.linear_regression_line.get_cursors()
                line = PDFLine(self.session, self.page, cursor1, cursor2)
                line._draw()
                if self.linear_regression_equation:
                    text = self.linear_regression_line.get_equation()
                    text_width = self.session.parent.document.font._string_width(text)
                    text_height = self.session.parent.document.font.font_size * 1.2
                    x = cursor2.x + (-text_width)
                    y = self.linear_regression_line._get_y_at_x(x) + text_height
                    text = PDFText(self.session, self.page, text, cursor=PDFCursor(x, y))

    def _set_color(self, index):
        color = self.line_colors[index]
        if isinstance(color, PDFColor):
            color._set_type('f')
            if not self.session._compare_color(color):
                self.session._out(color._get_color_string(), self.page)
                self.session._save_color(color.copy())
            color._set_type('d')
            if not self.session._compare_color(color):
                self.session._out(color._get_color_string(), self.page)
                self.session._save_color(color.copy())


class LinearRegressionLine(object):
    def __init__(self):
        self.min_x = None
        self.min_y = None
        self.max_x = None
        self.max_y = None
        self.x_sum = 0
        self.y_sum = 0
        self.xy_sum = 0
        self.x2_sum = 0
        self.y2_sum = 0
        self.N = 0

    def add_coord(self, cursor):
        x = cursor.x
        y = cursor.y
        self.x_sum += x
        self.y_sum += y
        self.xy_sum += x * y
        self.x2_sum += x ** 2
        self.y2_sum += y ** 2
        self.N += 1

        if self.min_x is None:
            self.min_x = x
        elif x < self.min_x:
            self.min_x = x

        if self.max_x is None:
            self.max_x = x
        elif x > self.max_x:
            self.max_x = x

        if self.min_y is None:
            self.min_y = y
        elif y < self.min_y:
            self.min_y = y

        if self.max_y is None:
            self.max_y = y
        elif y > self.max_y:
            self.max_y = y

    def calculate_line(self):
        self.slope = ((self.N * self.xy_sum) - (self.x_sum * self.y_sum)) / ((self.N * self.x2_sum) - (self.x_sum ** 2))
        self.intercept = ((self.x2_sum * self.y_sum) - (self.x_sum * self.xy_sum)) / ((self.N * self.x2_sum) - (self.x_sum ** 2))

        return self.slope, self.intercept

    def get_cursors(self):
        x1 = 0
        y1 = 0
        if self.intercept < self.min_y:
            y1 = self.min_y
            x1 = self._get_x_at_y(y1)
        if self.intercept >= self.min_y:
            x1 = self.min_x
            y1 = self._get_y_at_x(x1)

        x2 = self.max_x
        y2 = self._get_y_at_x(x2)
        if y2 > self.max_y:
            y2 = self.max_y
            x2 = self._get_x_at_y(y2)

        return PDFCursor(x1, y1), PDFCursor(x2, y2)

    def _get_x_at_y(self, y):
        return (y - self.intercept) / float(self.slope)

    def _get_y_at_x(self, x):
        return self.slope * x + self.intercept

    def get_equation(self):
        equation =  "y = %0.2f x + %0.2f" % (self.slope, self.intercept)
        return equation