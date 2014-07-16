from pdfgraph import PDFGraph
from pdfcolor import PDFColor
from pdfcursor import PDFCursor
from pdfline import PDFLine
from pdftext import PDFText
from pdfellipse import PDFEllipse


class PDFLineGraph(PDFGraph):
    def __init__(self, session, page, cursor, data, width, height, title, x_axis_limits, y_axis_limits, frequency, axis_titles, axis_labels, line_colors,
                 background=None, legend=None, dots=None, stroke="S"):
        super(PDFLineGraph, self).__init__(session, page, cursor, width, height, title, background, legend)
        self.data = data
        self.stroke = stroke
        self.dots = dots
        self._set_colors(line_colors)
        self._set_range(x_axis_limits, y_axis_limits)
        self._set_frequency(frequency)
        self.draw_axis_titles(axis_titles[0], axis_titles[1])
        self.axis_labels = axis_labels
        self.draw_x_axis()
        self.draw_y_axis()
        self.draw_data()

    def _set_colors(self, line_colors):
        if line_colors is not None:
            self.line_colors = line_colors
        else:
            self.line_colors = self.background.default_color_list

    def _set_range(self, x_axis_limits, y_axis_limits):
        x_data = x_axis_limits
        if x_axis_limits == "Auto" or x_axis_limits is None:
            x_data = []
            for series in self.data:
                mylist = series.values()[0]
                for pair in mylist:
                    x_data.append(pair[0])
        y_data = y_axis_limits
        if y_axis_limits == "Auto" or y_axis_limits is None:
            y_data = []
            for series in self.data:
                mylist = series.values()[0]
                for pair in mylist:
                    y_data.append(pair[1])
        self.x_range, self.y_range = self.get_axis_limits(x_data, y_data)

    def _set_frequency(self, frequency):
        if frequency == "Auto" or frequency is None:
            self.frequency = (self.get_frequency(self.x_range), self.get_frequency(self.y_range))
        else:
            self.frequency = frequency

    def draw_data(self):
        if self.legend is not None:
            self._draw_legend_title()
        i = 0
        for series in self.data:
            self._set_color(i)
            self._set_line_size()
            if self.legend is not None:
                self._draw_legend_line(i, series.keys()[0])

            for values in series.itervalues():
                cursor = self.get_coord(values[0])
                s = '%.2f %.2f m' % (cursor.x, cursor.y_prime)
                self.session._out(s, self.page)
                cursors = []
                for pair in values[1:]:
                    cursor = self.get_coord(pair)
                    self.session._out('%.2f %.2f l' % (cursor.x, cursor.y_prime), self.page)
                    cursors.append(cursor)
                self.session._out('%s ' % self.stroke, self.page)
                self._draw_dots(cursors)
                i += 1
        if self.legend is not None:
            self._draw_legend_box()

    def get_coord(self, tuple):
        x = self.interpolate(tuple[0], self.x_array)
        y = self.interpolate(tuple[1], self.y_array)
        return PDFCursor(x, y)

    def _set_color(self, index):
        color = self.line_colors[index]
        if isinstance(color, PDFColor):
            color._set_type('d')
            if not self.session._compare_color(color):
                self.session._out(color._get_color_string(), self.page)
                self.session._save_color(color.copy())

    def _set_line_size(self):
        pass

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
                dot = PDFEllipse(self.session, self.page, cursor, PDFCursor(self.dots, self.dots))
                dot._draw()