from .pdfrectangle import PDFRectangle
from .pdfcolor import PDFColor
from .pdfcursor import PDFCursor
from .pdftext import PDFText
from .pdfline import PDFLine
from .pdfgraphformat import PDFGraphBackground


class PDFGraph(object):
    def __init__(self, session, page, cursor, width, height, title=None, background=None, legend=None, axis=True):
        self.session = session
        self.page = page
        self.font = self.session.parent.document.font
        self.origin = cursor
        self.axis_labels = None
        self.legend = legend
        self.axis = axis
        self.base_color = PDFColor(77, 77, 77)
        if background is None:
            self.background = PDFGraphBackground()
        else:
            self.background = background
        self._set_accessories(title, width, height)
        self._draw_background(width, height)
        self._pad(width, height)
        self._draw_title()

    def _set_accessories(self, title, width, height):
        self.title = title
        if title is None:
            self.padding = (self.background.padding * width, self.background.padding * height)
        else:
            self.padding = (self.background.padding * width, (self.background.padding * height + 0.13 * height))

    def _draw_background(self, width, height):
        if self.background.exists:
            cursor_end = PDFCursor(self.origin.x + width, self.origin.y + height)
            rectangle = PDFRectangle(self.session, self.page, self.origin, cursor_end, self.background.border_color, self.background.fill_color, self.background.style, self.background.stroke, self.background.size)
            rectangle._draw()

    def _pad(self, width, height):
        self.origin.x_plus(self.padding[0])
        self.origin.y_plus(-self.padding[1] + height)
        if self.legend == "right":
            self.width = (0.8 * width) - (2 * self.padding[0])
            self.legend_width = 0.2 * width - (self.padding[0] * 0.2)
            self.height = height - 2 * self.padding[1]
            self.legend_height = self.height
            self.legend_start_cursor = PDFCursor(self.origin.x + self.width + self.padding[0], self.origin.y - self.height)
        else:
            self.width = width - 2 * self.padding[0]
            self.height = height - 2 * self.padding[1]

    def _draw_title(self):
        if self.title is not None:
            save_font = self.font
            self.session.parent.document.set_font(save_font.family, "b", save_font.font_size * 1.2)
            title_cursor = PDFCursor(self.origin.x + (self.width - self.session.parent.document.font._string_width(self.title))/ 2.0, self.origin.y - self.height - (self.padding[1] * 0.4))
            title = PDFText(self.session, self.page, self.title, cursor=title_cursor, color=self.base_color)
            self.session.parent.document.set_font(font=save_font)

    def _draw_legend_title(self, legend_title="Legend"):
        text_width = self.session.parent.document.font._string_width(legend_title)
        text_height = self.session.parent.document.font.font_size
        text_cursor = PDFCursor(self.legend_start_cursor.x + (self.legend_width - text_width) / 2.0, self.legend_start_cursor.y + 1.2 * text_height)
        legend_title = PDFText(self.session, self.page, "Legend", cursor=text_cursor)

        self.legend_data_start = PDFCursor(self.legend_start_cursor.x + 10, self.legend_start_cursor.y + 3 * text_height)

    def _draw_legend_box(self):
        end_cursor = PDFCursor(self.legend_start_cursor.x + self.legend_width, self.legend_data_start.y + 1.2 * self.session.parent.document.font.font_size)
        legend_box = PDFRectangle(self.session, self.page, self.legend_start_cursor, end_cursor, self.base_color)
        legend_box._draw()

    def _get_limits_from_data(self, data):
        axis_list = [data[0], data[0]]
        for item in data[1:]:
            if item < axis_list[0]:
                axis_list[0] = item
            elif item > axis_list[1]:
                axis_list[1] = item
            else:
                pass
        return tuple(axis_list)

    def get_axis_limits(self, x_data=None, y_data=None):
        x_limits = None
        if x_data is not None:
            x_limits = self._get_limits_from_data(x_data)

        y_limits = None
        if y_data is not None:
            y_limits = self._get_limits_from_data(y_data)

        return x_limits, y_limits

    def get_frequency(self, limits):
        if limits[1] != limits[0]:
            return ((limits[1] - limits[0]) / 10.0)
        else:
            return 1

    def draw_axis_titles(self, x_title=None, y_title=None):
        if x_title is not None:
            label_cursor_x = PDFCursor(self.origin.x + (self.width - self.padding[0])/ 2.0, self.origin.y + 0.8 * self.padding[1])
            PDFText(self.session, self.page, x_title, cursor=label_cursor_x)

        if y_title is not None:
            if self.padding[0] == 0:
                self.padding = (self.width * 0.12, self.padding[1])
            label_cursor_y = PDFCursor(self.origin.x - 0.8 * self.padding[0], self.origin.y - (self.height / 2.0) - 0.8 * self.padding[1])
            text = PDFText(self.session, self.page, None, cursor=label_cursor_y)
            text.text_rotate(-90)
            text._text(y_title)

    def draw_x_axis(self, zero=True):
        # Draw x axis ticks
        self.x_array = [(0, self.origin.x)]
        try:
            x_delta = self.width / (float(self.x_range[1] - self.x_range[0]) / float(self.frequency[0]))
        except ZeroDivisionError:
            x_delta = self.width / 2.0
        self.x_delta = x_delta
        y_delta = 3
        tick_x = self.origin.x
        i = self.x_range[0]
        k = 0
        self.draw_tick(tick_x, self.origin.y, tick_x, self.origin.y + y_delta)
        if zero:
            self.draw_x_label(i, k, tick_x, self.origin.y)
        while i < self.x_range[1]:
            i += self.frequency[0]
            tick_x += x_delta
            self.x_array.append((i, tick_x))
            self.draw_tick(tick_x, self.origin.y, tick_x, self.origin.y + y_delta)
            self.draw_x_label(i, k, tick_x, self.origin.y)
            k += 1

        cursor2 = PDFCursor(tick_x, self.origin.y)
        if self.axis:
            xaxis = PDFLine(self.session, self.page, self.origin, cursor2, self.base_color, stroke="solid")
            xaxis._draw()

    def draw_y_axis(self, zero=True):
        # Draw y axis ticks
        self.y_array = [(self.y_range[0], self.origin.y)]
        try:
            y_delta = self.height / (float(self.y_range[1] - self.y_range[0]) / float(self.frequency[1]))
        except ZeroDivisionError:
            y_delta = self.height / 2.0
        x_delta = 3
        tick_y = self.origin.y
        j = self.y_range[0]
        k = 0
        self.draw_tick(self.origin.x, tick_y, self.origin.x - x_delta, tick_y)
        if zero:
            self.draw_y_label(j, k, self.origin.x - x_delta, tick_y)
        while j < self.y_range[1]:
            j += self.frequency[1]
            tick_y -= y_delta
            self.y_array.append((j, tick_y))
            self.draw_tick(self.origin.x, tick_y, self.origin.x - x_delta, tick_y)
            self.draw_y_label(j, k, self.origin.x - x_delta, tick_y)
            k += 1

        # Draw axis lines
        cursor1 = PDFCursor(self.origin.x, tick_y)
        if self.axis:
            yaxis = PDFLine(self.session, self.page, cursor1, self.origin, self.base_color, stroke="solid")
            yaxis._draw()

    def draw_tick(self, x1, y1, x2, y2):
        x = PDFCursor(x1, y1)
        y = PDFCursor(x2, y2)
        if self.axis:
            tick = PDFLine(self.session, self.page, x, y, self.base_color, "solid")
            tick._draw()

    def draw_x_label(self, i, k, x1, y1):
        if self.axis_labels is None:
            return
        elif self.axis_labels is "Auto":
            text = i
        else:
            text = self.axis_labels["x"][k]

        cursor = PDFCursor(x1 - self.font._string_width(text) / 2.0, y1 + 10)
        label = PDFText(self.session, self.page, '%s' % text, cursor=cursor)

    def draw_y_label(self, i, k, x1, y1):
        if self.axis_labels is None:
            return
        elif self.axis_labels is "Auto":
            text = i
        else:
            text = self.axis_labels["y"][k]

        cursor = PDFCursor(x1 - self.font._string_width(text) - 1, y1 + 2)
        label = PDFText(self.session, self.page, '%s' % text, cursor=cursor)

    @classmethod
    def interpolate(cls, item, tuplelist):
        index_high = 0
        keys = [i[0] for i in tuplelist]
        values = [i[1] for i in tuplelist]
        for key in keys:
            if item < key:
                index_high = keys.index(key)
                break
        index_low = index_high - 1
        try:
            ratio = (item - keys[index_low]) / float((keys[index_high] - keys[index_low]))
        except ZeroDivisionError:
            ratio = 1
        value = ratio * (values[index_high] - values[index_low]) + values[index_low]
        return value