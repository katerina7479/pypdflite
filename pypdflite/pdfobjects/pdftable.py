from pdfcell import PDFCell


class PDFTable(object):

    def __init__(self, session, page, table_data, text_font, color_scheme,
                 cursor, bycols=False):
        self.session = session
        self.page = page
        self.table_data = table_data
        self.text_font = text_font
        self.color_scheme = color_scheme
        self.cursor = cursor
        if bycols is True:
            self.invert_table_data()
        self.initiate_cells()
        self.set_text_cursor()

    def invert_table_data(self):
        rows = []
        number_of_rows = len(self.table_data[0])

        for x in range(0, number_of_rows):
            rows.append([])

        for column in self.table_data:
            for x in range(0, number_of_rows):
                rows[x].append(column[x])
        self.table_data = rows

    def initiate_cells(self):
        self.rows = []
        row_index = 0
        for row in self.table_data:
            temp_row = []
            column_index = 0
            for text in row:
                temp_row.append(PDFCell(self, text, self.text_font,
                                self.color_scheme, row_index, column_index))
                column_index += 1
            row_index += 1
            self.rows.append(temp_row)

        print self.rows

    def set_text_cursor(self):
        self.text_cursor = self.cursor.copy()
        self.text_cursor.x_plus(3)
        self.text_cursor.y_plus(4)

    def _advance_text_cursor_x(self):
        self.text_cursor.x_plus(10)

    def _advance_text_cursor_y(self):
        self.text_cursor.y_plus(7)
        self.text_cursor.x_reset()

    def draw(self):
        self.draw_text()
        self.draw_borders()

    def draw_text(self):
        for row in self.rows:
            for cell in row:
                cell.draw_text(self.text_cursor)
                self._advance_text_cursor_x()
            self._advance_text_cursor_y()

    def draw_borders(self):
        pass
