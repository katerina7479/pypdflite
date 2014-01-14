from pdfrow import PDFRow
from pdfcolumn import PDFColumn
from pdfcell import PDFCell


class PDFTable(object):

    def __init__(self, session, page, table_data, font, color_scheme,
                 cursor, bycols=False):
        self.session = session
        self.page = page
        self.table_data = table_data
        self.font = font
        self.color_scheme = color_scheme
        self.cursor = cursor
        self.text_cursor = self.cursor.copy()
        self.border_cursor = self.cursor.copy()

        if bycols is True:
            self.invert_table_data()
        self.initiate_cells()

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
        self.columns = []

        number_of_rows = len(self.table_data)
        number_of_columns = len(self.table_data[0])

        for x in range(number_of_columns):
            self.columns.append(PDFColumn(self, self.font, self.color_scheme))

        row_index = 0
        row_num = 1
        for row in self.table_data:
            next_row = PDFRow(self, self.font, self.color_scheme, row_num, self.text_cursor, self.border_cursor)
            row_num += 1
            column_index = 0
            for text in row:
                cell = PDFCell(self, text, self.font, self.color_scheme, row_index, column_index, self.text_cursor, self.border_cursor)
                next_row.add_cell(cell)
                self.columns[column_index].add_cell(cell)
                column_index += 1
            next_row._finish()
            row_index += 1
            self.rows.append(next_row)

        for column in self.columns:
            column.get_max_sizes()

    def draw(self):
        self.rows[0]._advance_first_row()
        self.draw_text()
        self.draw_borders()
        self.set_final_cursor()

    def draw_text(self):
        for i in range(len(self.rows)):
            self.rows[i].draw_text()
            self.text_cursor.x_reset()
            if (i + 1) < len(self.rows):
                self.text_cursor.y_plus(self.rows[i + 1].max_height)

    def draw_borders(self):
        for i in range(len(self.rows)):
            self.rows[i].draw_borders()
            self.border_cursor.x_reset()
            if (i + 1) < len(self.rows):
                self.border_cursor.y_plus(self.rows[i + 1].max_height)

    def set_final_cursor(self):
        if self.text_cursor.is_greater_than(self.border_cursor):
            self.cursor = self.text_cursor
        else:
            self.cursor = self.border_cursor
