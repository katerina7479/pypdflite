from pdfgraph import PDFGraph
from pdfcolor import PDFColor
from pdfcursor import PDFCursor


class PDFLineGraph(PDFGraph):
    def __init__(self, session, page, cursor, data, width, height, title, x_axis_limits, y_axis_limits, frequency, axis_titles, axis_labels, line_colors,
                 background_style="S", border_size=1, background_border_color=None, background_fill_color=None, padding=0.1, legend=None):
        super(PDFLineGraph, self).__init__(session, page, cursor, width, height, title, background_style, border_size, background_border_color, background_fill_color, padding, legend)
        self.data = data
        self.stroke = "S"
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
            self.line_colors = self.default_color_list

    def _set_range(self, x_axis_limits, y_axis_limits):
        x_data = None
        if x_axis_limits == "Auto" or x_axis_limits is None:
            x_data = []
            for series in self.data:
                mylist = series.values()[0]
                for pair in mylist:
                    x_data.append(pair[0])
        y_data = None
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
        i = 0
        for series in self.data:
            for values in series.itervalues():
                self._set_color(i)
                self._set_line_size()

                cursor = self.get_coord(values[0])
                s = '%.2f %.2f m' % (cursor.x, cursor.y_prime)
                self.session._out(s, self.page)
                for pair in values[1:]:
                    cursor = self.get_coord(pair)
                    self.session._out('%.2f %.2f l' % (cursor.x, cursor.y_prime), self.page)
                self.session._out('%s ' % self.stroke, self.page)
                i += 1

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

