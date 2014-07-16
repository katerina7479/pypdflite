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
            if self.legend is not None:
                self._draw_legend_line(i, series.keys()[0])
            series = series.values()[0]
            self._set_color(i)
            self.line = LinearRegressionLine()
            i += 1

            cursors = []
            for value in series:
                cursor = self.get_coord(value)
                cursors.append(cursor)
                self.line.add_data(value)
            self._draw_dots(cursors)

            if self.linear_regression:
                self.line.calculate_line()
                cursor1, cursor2 = self.line.get_cursors(cursors)
                trend = PDFLine(self.session, self.page, cursor1, cursor2)
                trend._draw()
                if self.linear_regression_equation:
                    text = self.line.get_equation()
                    text_width = self.session.parent.document.font._string_width(text)
                    text_height = self.session.parent.document.font.font_size * 1.2
                    x = cursor2.x + (-text_width)
                    y = self.line._get_y_at_x(x) + text_height
                    PDFText(self.session, self.page, text, cursor=PDFCursor(x, y))

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
        if self.dots is not None:
            for cursor in cursors:
                dot = PDFEllipse(self.session, self.page, cursor, PDFCursor(self.dots, self.dots), style="F")
                dot._draw()

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
        self.x_sum = 0
        self.y_sum = 0
        self.xy_sum = 0
        self.x2_sum = 0
        self.y2_sum = 0
        self.N = 0

    def add_data(self, data):
        x = data[0]
        y = data[1]
        self.x_sum += x
        self.y_sum += y
        self.xy_sum += x * y
        self.x2_sum += x ** 2
        self.y2_sum += y ** 2
        self.N += 1

    def calculate_line(self):
        self.data_slope = ((self.N * self.xy_sum) - (self.x_sum * self.y_sum)) / ((self.N * self.x2_sum) - (self.x_sum ** 2))
        self.data_intercept = ((self.x2_sum * self.y_sum) - (self.x_sum * self.xy_sum)) / ((self.N * self.x2_sum) - (self.x_sum ** 2))
        return self.data_slope, self.data_intercept

    def get_cursors(self, cursors):
        xlist = [i.x for i in cursors]
        ylist = [i.y for i in cursors]

        min_x = min(xlist)
        min_y = min(ylist)
        max_x = max(xlist)
        max_y = max(ylist)

        x_sum = 0
        y_sum = 0
        xy_sum = 0
        x2_sum = 0
        y2_sum = 0
        N = 0

        for cursor in cursors:
            x = cursor.x
            y = cursor.y
            x_sum += x
            y_sum += y
            xy_sum += x * y
            x2_sum += x ** 2
            y2_sum += y ** 2
            N += 1

        self.cursor_slope = ((N * xy_sum) - (x_sum * y_sum)) / ((N * x2_sum) - (x_sum ** 2))
        self.cursor_intercept = ((x2_sum * y_sum) - (x_sum * xy_sum)) / ((N * x2_sum) - (x_sum ** 2))

        x1 = 0
        y1 = 0
        if self.cursor_intercept < min_y:
            y1 = min_y
            x1 = self._get_x_at_y(y1)
        if self.cursor_intercept >= min_y:
            x1 = min_x
            y1 = self._get_y_at_x(x1)

        x2 = max_x
        y2 = self._get_y_at_x(x2)
        if y2 > max_y:
            y2 = max_y
            x2 = self._get_x_at_y(y2)

        return PDFCursor(x1, y1), PDFCursor(x2, y2)

    def _get_x_at_y(self, y):
        return (y - self.cursor_intercept) / float(self.cursor_slope)

    def _get_y_at_x(self, x):
        return self.cursor_slope * x + self.cursor_intercept

    def get_equation(self):
        equation =  "y = %0.2f x + %0.2f" % (self.data_slope, self.data_intercept)
        return equation

    def interpolate(self, item, tuplelist):
        index_high = 0
        keys = [i[0] for i in tuplelist]
        values = [i[1] for i in tuplelist]
        for key in keys:
            if item < key:
                index_high = keys.index(key)
                break
        index_low = index_high - 1
        ratio = (item - keys[index_low]) / float((keys[index_high] - keys[index_low]))
        value = ratio * (values[index_high] - values[index_low]) + values[index_low]
        return value
