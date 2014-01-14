from pdftext import PDFText
from pdfline import PDFLine


class PDFCell(object):
    def __init__(self, parent, text, font, color_scheme,
                 row_index, column_index, text_cursor, border_cursor):
        self.parent = parent
        self.row_index = row_index
        self.column_index = column_index

        self.text = text
        self.set_font(font)

        self.text_cursor = text_cursor
        self.border_cursor = border_cursor

        self.set_text_padding()
        self.set_color_scheme()
        self.max_width = None
        self.width_diff = None

    def __repr__(self):
        return '(%s, %s)' % (self.row_index, self.column_index)

    def set_font(self, font=None):
        if font is None:
            self.font = self.parent.font
        else:
            self.font = font
        self.text_width = self.font.string_width(self.text)

    def set_color_scheme(self, color_scheme=None):
        if color_scheme is None:
            self.color_scheme = self.parent.color_scheme
        else:
            self.color_scheme = color_scheme

    def draw_text(self):
        self.text_cursor.y_plus(-self.padding_bottom)
        self.text_cursor.x_plus(self.padding_left)
        self.text_object = PDFText(self.parent.session, self.parent.page,
                                   self.font, self.color_scheme, self.text,
                                   self.text_cursor)
        self.text_cursor.x_plus(self.padding_right + self.width_diff)
        self.text_cursor.y_plus(self.padding_bottom)

    def _get_points(self):
        self.point_nw = self.border_cursor
        self.point_sw = self.border_cursor.copy()
        self.point_se = self.border_cursor.copy()
        self.point_ne = self.border_cursor.copy()

        # cursor start is NW point
        self.point_sw.y_plus(self.max_height)
        self.point_ne.x_plus(self.max_width)

        self.point_se.x_plus(self.max_width)
        self.point_se.y_plus(self.max_height)

        # print "Points, sw, se, nw, ne", self.point_sw, self.point_se, self.point_nw, self.point_ne

    def draw_borders(self):
        self._get_points()
        self.bottom_line = PDFLine(self.parent.session, self.parent.page,
                                   self.color_scheme, self.point_sw, self.point_se, style=None, size=1)
        self.right_line = PDFLine(self.parent.session, self.parent.page,
                                  self.color_scheme, self.point_se, self.point_ne, style=None, size=1)
        self.left_line = PDFLine(self.parent.session, self.parent.page,
                                 self.color_scheme, self.point_sw, self.point_nw, style=None, size=1)
        self.top_line = PDFLine(self.parent.session, self.parent.page,
                                self.color_scheme, self.point_ne, self.point_nw, style=None, size=1)

        self.bottom_line.draw()
        self.right_line.draw()
        self.left_line.draw()
        self.top_line.draw()

        self.border_cursor = self.point_ne

    def set_text_padding(self, top=10, right=10, bottom=8, left=10):
        self.padding_top = top
        self.padding_right = right
        self.padding_left = left
        self.padding_bottom = bottom

        self.width = (self.font.string_width(self.text) +
                      self.padding_right + self.padding_left)

        self.height = (self.font.line_size + self.padding_top +
                       self.padding_bottom)

    def _advance_initial(self):
        self.text_cursor.y_plus(self.height - self.padding_bottom)
