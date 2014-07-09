from pdfcolor import PDFColor
from pdfcursor import PDFCursor
from pdfline import PDFLine


class PDFLineGraph(object):
    """
    Create a line graph from data dict(series labels)

    """
    def __init__(self, session, page, cursor, data, width, height, axistuple, frequency, line_colors):
        self.session = session
        self.page = page
        self.origin = cursor
        self.data = data
        self.width = width
        self.height = height
        self.stroke = "S"
        self.line_colors = line_colors
        self.x_range = (axistuple[0], axistuple[1])
        self.y_range = (axistuple[2], axistuple[3])
        self.frequency = frequency
        self.make_axis()
        self.draw_data()

    def make_axis(self):
        cursor1 = PDFCursor(self.origin.x, self.origin.y - self.height)
        yaxis = PDFLine(self.session, self.page, cursor1, self.origin, self.line_colors[0], style="solid")
        yaxis._draw()

        cursor2 = PDFCursor(self.origin.x + self.width, self.origin.y)
        xaxis = PDFLine(self.session, self.page, self.origin, cursor2, self.line_colors[0], style="solid")
        xaxis._draw()

        self.x_array = [(0, self.origin.x)]
        x_delta = self.width / (float(self.x_range[1] - self.x_range[0]) / float(self.frequency[0]))
        y_delta = 3
        tick_x = self.origin.x
        i = self.x_range[0]
        while i < self.x_range[1]:
            i += self.frequency[0]
            tick_x += x_delta
            self.x_array.append((i, tick_x))
            self.draw_tick(tick_x, self.origin.y, tick_x, self.origin.y + y_delta)

        self.y_array = [(0, self.origin.y)]
        y_delta = self.height / (float(self.y_range[1] - self.y_range[0]) / float(self.frequency[1]))
        x_delta = 3
        tick_y = self.origin.y
        j = self.y_range[0]
        while j < self.y_range[1]:
            j += self.frequency[1]
            tick_y -= y_delta
            self.y_array.append((j, tick_y))
            self.draw_tick(self.origin.x, tick_y, self.origin.x - x_delta, tick_y)
        print self.x_array


    def draw_tick(self, x1, y1, x2, y2):
        x = PDFCursor(x1, y1)
        y = PDFCursor(x2, y2)
        tick = PDFLine(self.session, self.page, x, y, self.line_colors[0], "solid")
        tick._draw()

    def draw_data(self):
        i = 0
        for series, values in self.data.iteritems():
            self._set_color(i+1)
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

    def interpolate(self, item, tuplelist):
        index_high = 0
        keys = [i[0] for i in tuplelist]
        values = [i[1] for i in tuplelist]
        for key in keys:
            if item < key:
                index_high = keys.index(key)
                break
        index_low = index_high - 1
        ratio = (item - keys[index_low]) / (keys[index_high] - keys[index_low])
        value = ratio * (values[index_high] - values[index_low]) + values[index_low]
        return value