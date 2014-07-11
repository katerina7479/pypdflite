from pdfgraph import PDFGraph
from pdfcolor import PDFColor
from pdfcursor import PDFCursor


class PDFBarChart(PDFGraph):
    def __init__(self, session, page, data, cursor, width, height, axis_titles=None, y_axis_limits=None, y_axis_frequency=None, bar_style="S", bar_padding=0, bar_border_colors=None, bar_fill_colors=None,
                 background_style="S", background_size=1, background_border_color=None, background_fill_color=None):
        super(PDFBarChart, self).__init__(session, page, cursor, width, height, background_style, background_size, background_border_color, background_fill_color)
        self.data = data
        self.bar_style = bar_style
        self.axis_labels = "Auto"
        self.set_colors(bar_border_colors, bar_fill_colors)
        self.make_axis(y_axis_limits, y_axis_frequency)

    def set_colors(self, border_colors, fill_colors):
        if self.bar_style == "S":
            self.bar_border_colors = border_colors
            self.bar_fill_colors = None
            if border_colors is None:
                self.bar_border_colors = self.default_color_list

        if self.bar_style == "F":
            self.bar_border_colors = None
            self.bar_fill_colors = fill_colors
            if fill_colors is None:
                self.bar_fill_colors = self.default_color_list

        if self.bar_style == "B":
            self.bar_border_colors = border_colors
            self.bar_fill_colors = fill_colors
            if fill_colors is None:
                self.bar_fill_colors = self.default_color_list
            if border_colors is None:
                self.bar_border_colors = []
                for color in self.default_color_list:
                    r = max(int(color.red * 1.25), 255)
                    g = max(int(color.green * 1.25), 255)
                    b = max(int(color.blue * 1.25), 255)
                    self.bar_border_colors.append(PDFColor(r, g, b))

        if self.bar_fill_colors is not None:
            for color in self.bar_fill_colors:
                color._set_type('f')

    def make_axis(self, y_axis_limits, y_axis_frequency):
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
        self.frequency = (None, y)

        self.draw_y_axis()
