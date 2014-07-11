from pdfgraph import PDFGraph
from pdfcolor import PDFColor
from pdfcursor import PDFCursor


class PDFBarChart(PDFGraph):
    def __init__(self, session, page, data, cursor, width, height, axis_titles=None, bar_style="S", bar_padding=0, bar_border_colors=None, bar_fill_colors=None,
                 background_style="S", background_size=1, background_border_color=None, background_fill_color=None):
        super(PDFBarChart, self).__init__(session, page, cursor, width, height, background_style, background_size, background_border_color, background_fill_color)
        self.data = data
        self.bar_style = bar_style
        self.set_colors(bar_border_colors, bar_fill_colors)

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

