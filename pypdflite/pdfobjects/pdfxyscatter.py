from pdfgraph import PDFGraph
from pdfcolor import PDFColor
from pdfcursor import PDFCursor
from pdfline import PDFLine
from pdftext import PDFText
from pdfellipse import PDFEllipse
from pdflinegraph import PDFLineGraph


class PDFXYScatter(PDFLineGraph):
    def __init__(self, session, page, cursor, data, width, height, title, x_axis_limits, y_axis_limits, frequency, axis_titles, axis_labels, line_colors,
                 background_style="S", border_size=1, background_border_color=None, background_fill_color=None, padding=0.1, legend=None, dots=None):
        super(PDFXYScatter, self).__init__(session, page, cursor, data, width, height, title, x_axis_limits, y_axis_limits, frequency, axis_titles, axis_labels, line_colors,
                 background_style, border_size, background_border_color, background_fill_color, padding, legend, dots)

    def draw_data(self):
        if self.legend is not None:
            self._draw_legend_title()
        i = 0
        for series in self.data:
            self._set_color(i)
            if self.legend is not None:
                self._draw_legend_line(i, series.keys()[0])

            for values in series.itervalues():
                cursors = []
                for pair in values:
                    cursor = self.get_coord(pair)
                    cursors.append(cursor)
                self._draw_dots(cursors)
                i += 1

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
                dot = PDFEllipse(self.session, self.page, cursor, PDFCursor(self.dots, self.dots), stroke="F")
                dot._draw()

    def _set_color(self, index):
        color = self.line_colors[index]
        if isinstance(color, PDFColor):
            color._set_type('f')
            if not self.session._compare_color(color):
                self.session._out(color._get_color_string(), self.page)
                self.session._save_color(color.copy())