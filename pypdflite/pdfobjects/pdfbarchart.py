from pdfgraph import PDFGraph
from pdfcolor import PDFColor
from pdfcursor import PDFCursor
from pdftext import PDFText
from pdfrectangle import PDFRectangle


class PDFBarChart(PDFGraph):
    def __init__(self, session, page, data, cursor, width, height, title=None, axis_titles=None, y_axis_limits=None, y_axis_frequency=None, bar_style="F", bar_padding=0, bar_border_colors=None, bar_fill_colors=None,
                 background=None, legend=None):
        super(PDFBarChart, self).__init__(session, page, cursor, width, height, title, background, legend)
        self.data = data
        self.bar_style = bar_style
        self.bar_padding = bar_padding
        self.axis_labels = "Auto"
        self.draw_axis_titles(axis_titles[0], axis_titles[1])
        self.set_colors(bar_border_colors, bar_fill_colors)
        self.make_y_axis(y_axis_limits, y_axis_frequency)
        self.make_x_axis()
        self.draw_bars()

    def set_colors(self, border_colors, fill_colors):
        if self.bar_style == "S":
            self.bar_border_colors = border_colors
            self.bar_fill_colors = None
            if border_colors is None:
                self.bar_border_colors = self.background.default_color_list

        if self.bar_style == "F":
            self.bar_border_colors = None
            self.bar_fill_colors = fill_colors
            if fill_colors is None:
                self.bar_fill_colors = self.background.default_color_list

        if self.bar_style == "B":
            self.bar_border_colors = border_colors
            self.bar_fill_colors = fill_colors
            if fill_colors is None:
                self.bar_fill_colors = self.background.default_color_list
            if border_colors is None:
                self.bar_border_colors = []
                for color in self.background.default_color_list:
                    r = min(int(color.red * 0.75), 255)
                    g = min(int(color.green * 0.75), 255)
                    b = min(int(color.blue * 0.75), 255)
                    self.bar_border_colors.append(PDFColor(r, g, b))

        if self.bar_fill_colors is not None:
            if isinstance(self.bar_fill_colors, PDFColor):
                self.bar_fill_colors._set_type('f')
            else:
                for color in self.bar_fill_colors:
                    color._set_type('f')

    def make_y_axis(self, y_axis_limits, y_axis_frequency):
        if y_axis_limits is None:
            y_data = []
            for pair in self.data:
                y_data.append(pair[1])
            _, self.y_range = self.get_axis_limits(None, y_data)
        else:
            self.y_range = y_axis_limits

        if y_axis_frequency is None:
            y = self.get_frequency(self.y_range)
        else:
            y = y_axis_frequency
        self.frequency = (1, y)

        self.draw_y_axis()

    def make_x_axis(self):
        self.x_range = (0, len(self.data))
        self.draw_x_axis(zero=False)

    def draw_x_label(self, i, k, x1, y1):
        text = self.data[k][0]
        cursor = PDFCursor(x1 - (self.x_delta + self.font._string_width(text)) / 2.0, y1 + 9)
        label = PDFText(self.session, self.page,'%s' % text, cursor=cursor)

    def draw_bars(self):
        x_space = int(self.bar_padding * self.x_delta)
        i = 0
        for pair in self.data:
            draw, fill = self._get_colors(i)
            cursor1 = PDFCursor(self.x_array[i][1] + x_space, self.interpolate(pair[1], self.y_array))
            cursor2 = PDFCursor(self.x_array[i][1] + self.x_delta - x_space, self.origin.y)
            rect = PDFRectangle(self.session, self.page, cursor1, cursor2, draw, fill, self.bar_style, "solid")
            rect._draw()
            i += 1

    def _get_colors(self, index):
        if isinstance(self.bar_fill_colors, PDFColor):
            fill_color = self.bar_fill_colors
        elif self.bar_fill_colors:
            fill_color = self.bar_fill_colors[index]
        else:
            fill_color = None

        if isinstance(self.bar_border_colors, PDFColor):
            draw_color = self.bar_border_colors
        elif self.bar_border_colors:
            draw_color = self.bar_border_colors[index]
        else:
            draw_color = None
        return draw_color, fill_color


class PDFMultiBarChart(PDFBarChart):
    def __init__(self, session, page, data, cursor, width, height, title=None, axis_titles=None, y_axis_limits=None, y_axis_frequency=None, bar_style="F", bar_padding=0, bar_border_colors=None, bar_fill_colors=None, background=None, legend=None):
        super(PDFMultiBarChart, self).__init__(session, page, data, cursor, width, height, title, axis_titles, y_axis_limits, y_axis_frequency, bar_style, bar_padding, bar_border_colors, bar_fill_colors, background, legend)

    def draw_bars(self):
        x_space = int(self.bar_padding * self.x_delta)

        sub_array = []
        for x in self.x_array:
            sub_array.append((x[0], x[1] + x_space))
        self.new_x_array = [sub_array]

        new_x_delta = self.x_delta / float(len(self.data))
        for series in range(1, len(self.data)):
            sub_array = []
            for pair in self.x_array:
                sub_array.append((pair[0], pair[1] + new_x_delta))
            self.new_x_array.append(sub_array)

        if self.legend is not None:
            self._legend_line_height = self.session.parent.document.font.font_size
            self.legend_start_cursor.x_plus(-self.padding[0] * 0.5)
            self.legend_width += self.padding[0] * 0.55
            self._draw_legend_title()

        j = 0
        for series in self.data:
            values_list = series.values()[0]
            draw, fill = self._get_colors(j)
            if self.legend is not None:
                self._draw_legend_line(j, series.keys()[0])
            i = 0
            for pair in values_list:
                cursor1 = PDFCursor(self.new_x_array[j][i][1], self.interpolate(pair[1], self.y_array))
                cursor2 = PDFCursor(self.new_x_array[j][i][1] + new_x_delta - x_space, self.origin.y)
                rect = PDFRectangle(self.session, self.page, cursor1, cursor2, draw, fill, self.bar_style, "solid")
                rect._draw()
                i += 1
            j += 1

        if self.legend is not None:
            self._draw_legend_box()

    def make_x_axis(self):
        max_len = 0
        self.x_labels = []
        for series in self.data:
            values_list = series.values()[0]
            if len(values_list) > max_len:
                max_len = len(values_list)
            for pair in values_list:
                self.x_labels.append(pair[0])

        self.x_range = (0, max_len)
        self.draw_x_axis(zero=False)

    def make_y_axis(self, y_axis_limits, y_axis_frequency):
        if y_axis_limits is None:
            y_data = []
            for series in self.data:
                for pair in series.values()[0]:
                    y_data.append(pair[1])
                _, self.y_range = self.get_axis_limits(None, y_data)
        else:
            self.y_range = y_axis_limits

        if y_axis_frequency is None:
            y = self.get_frequency(self.y_range)
        else:
            y = y_axis_frequency
        self.frequency = (1, y)
        self.draw_y_axis()

    def _draw_legend_line(self, index, series_name):
        end = PDFCursor(self.legend_data_start.x + 10, self.legend_data_start.y + 10)
        box = PDFRectangle(self.session, self.page, self.legend_data_start, end, None, self.bar_fill_colors[index], style="F", stroke="solid")
        box._draw()
        end.x_plus(10)
        text = PDFText(self.session, self.page, series_name, cursor=end, color=self.base_color)
        self.legend_data_start.y_plus(1.75 * self._legend_line_height)

    def draw_x_label(self, i, k, x1, y1):
        text = self.x_labels[k]
        cursor = PDFCursor(x1 - (self.x_delta + self.font._string_width(text)) / 2.0, y1 + 9)
        label = PDFText(self.session, self.page,'%s' % text, cursor=cursor)