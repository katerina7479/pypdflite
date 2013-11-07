from pdftext import PDFText


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

    def __repr__(self):
        return '(%s, %s)' % (self.row_index, self.column_index)

    def set_font(self, font=None):
        print "My font is", font
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
        self.text_object = PDFText(self.parent.session, self.parent.page,
                                   self.font, self.color_scheme, self.text,
                                   cursor)

    def set_padding(self, top=3, right=3, bottom=3, left=3):
        self.padding_top = top
        self.padding_right = right
        self.padding_left = left
        self.padding_bottom = bottom

        self.cell_width = (self.text_width +
                           self.padding_right + self.padding_left)
