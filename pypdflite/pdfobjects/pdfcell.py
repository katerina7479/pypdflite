from pdftext import PDFText
from pdfline import PDFLine


class PDFCell(object):
    def __init__(self, parent, text, font, color_scheme,
                 row_index, column_index):
        self.parent = parent
        self.row_index = row_index
        self.column_index = column_index

        self.text = text
        self.set_font(font)

        self.set_color_scheme()
        self.set_padding()
        self.max_width = None

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

    def draw_text(self, cursor):
        text_cursor = cursor.copy()
        self.text_object = PDFText(self.parent.session, self.parent.page,
                                   self.font, self.color_scheme, self.text,
                                   text_cursor)

    def get_points(self, cursor):
        self.point_sw = cursor.copy()
        self.point_se = cursor.copy()
        self.point_ne = cursor.copy()
        self.point_nw = cursor.copy()

        self.point_se.x_plus(self.max_width)
        self.point_nw.y_minus(self.max_height)
        self.point_ne.x_plus(self.max_width)
        self.point_ne.y_minus(self.max_height)

        return self.point_se

    def draw_borders(self, cursor):
        cursor = self.get_points(cursor)
        self.bottom_line = PDFLine(self.parent.session, self.parent.page,
                                   self.color_scheme, self.point_sw,
                                   self.point_se, style=None, size=1)

        self.right_line = PDFLine(self.parent.session, self.parent.page,
                                  self.color_scheme, self.point_se,
                                  self.point_ne, style=None, size=1)
        self.left_line = PDFLine(self.parent.session, self.parent.page,
                                 self.color_scheme, self.point_sw,
                                 self.point_nw, style=None, size=1)
        self.top_line = PDFLine(self.parent.session, self.parent.page,
                                self.color_scheme, self.point_ne,
                                self.point_nw, style=None, size=1)

        self.bottom_line.draw()
        self.right_line.draw()
        self.left_line.draw()
        self.top_line.draw()

    def set_padding(self, top=3, right=10, bottom=3, left=3):
        self.padding_top = top
        self.padding_right = right
        self.padding_left = left
        self.padding_bottom = bottom

        self.width = (self.text_width +
                      self.padding_right + self.padding_left)
        self.height = (self.font.line_size + self.padding_top +
                       self.padding_bottom)
