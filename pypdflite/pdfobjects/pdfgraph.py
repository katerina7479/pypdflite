from pdfrectangle import PDFRectangle
from pdfcolor import PDFColor
from pdfcursor import PDFCursor
from pdftext import PDFText
from pdfline import PDFLine


class PDFGraph(object):
    def __init__(self, session, page, cursor, width, height, background_style="S", background_size=1, background_border_color=None, background_fill_color=None, padding=0.1):
        self.session = session
        self.page = page
        self.font = self.session.parent.document.font
        self.origin = cursor
        self.axis_labels = None
        self.base_color = PDFColor(77, 77, 77)
        self.padding = (padding * width, padding * height)
        self._draw_background(width, height, background_style, background_size, background_border_color, background_fill_color)
        self._pad(width, height)

        self.default_color_list = [PDFColor(79, 129, 189), PDFColor(192, 80, 77), PDFColor(55, 187, 89),
                                PDFColor(128, 100, 162), PDFColor(72, 172, 198), PDFColor(247, 150, 70),
                                PDFColor(208, 146, 167), PDFColor(162, 200, 22), PDFColor(231, 188, 41),
                                PDFColor(156, 133, 192), PDFColor(243, 164, 71), PDFColor(128, 158, 194)]

    def _draw_background(self, width, height, style, size, border_color, fill_color):
        cursor_end = PDFCursor(self.origin.x + width, self.origin.y - height)
        rectangle = PDFRectangle(self.session, self.page, self.origin, cursor_end, border_color, fill_color, style, "solid", size)
        rectangle._draw()

    def _pad(self, width, height):
        self.origin.x_plus(self.padding[0])
        self.origin.y_plus(-self.padding[1] + height)
        self.width = width - 2 * self.padding[0]
        self.height = height - 2 * self.padding[1]

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
        return ((limits[1] - limits[0]) / 10.0)

    def draw_axis_titles(self, x_title=None, y_title=None):
        if x_title is not None:
            label_cursor_x = PDFCursor(self.origin.x + (self.width - self.padding[0])/ 2.0, self.origin.y + 0.8 * self.padding[1])
            PDFText(self.session, self.page, x_title, cursor=label_cursor_x)

        if y_title is not None:
            label_cursor_y = PDFCursor(self.origin.x - 0.8 * self.padding[0], self.origin.y - (self.height / 2.0) - 0.8 * self.padding[1])
            text = PDFText(self.session, self.page, None, cursor=label_cursor_y)
            text.text_rotate(-90)
            text._text(y_title)

    def draw_x_axis(self, zero=True):
        # Draw x axis ticks
        self.x_array = [(0, self.origin.x)]
        x_delta = self.width / (float(self.x_range[1] - self.x_range[0]) / float(self.frequency[0]))
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
        xaxis = PDFLine(self.session, self.page, self.origin, cursor2, self.base_color, style="solid")
        xaxis._draw()

    def draw_y_axis(self, zero=True):
        # Draw y axis ticks
        self.y_array = [(self.y_range[0], self.origin.y)]
        y_delta = self.height / (float(self.y_range[1] - self.y_range[0]) / float(self.frequency[1]))
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
        yaxis = PDFLine(self.session, self.page, cursor1, self.origin, self.base_color, style="solid")
        yaxis._draw()

    def draw_tick(self, x1, y1, x2, y2):
        x = PDFCursor(x1, y1)
        y = PDFCursor(x2, y2)
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
        ratio = (item - keys[index_low]) / float((keys[index_high] - keys[index_low]))
        value = ratio * (values[index_high] - values[index_low]) + values[index_low]
        return value