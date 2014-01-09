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
        if bycols is True:
            self.invert_table_data()
        self.initiate_cells()
        self.text_cursor = self.cursor.copy()
        self.border_cursor = self.cursor.copy()

        for column in self.columns:
            column.get_max_sizes()

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
        row_index = 0
        number_of_columns = len(self.table_data)
        for x in range(0, number_of_columns):
            self.columns.append(PDFColumn(self, self.font, self.color_scheme))

        for row in self.table_data:
            temp_row = PDFRow(self, self.font, self.color_scheme)
            column_index = 0
            for text in row:
                cell = PDFCell(self, text, self.font,
                               self.color_scheme, row_index, column_index)
                temp_row.add_cell(cell)
                self.columns[column_index].add_cell(cell)
                column_index += 1
            row_index += 1
            self.rows.append(temp_row)

    def set_final_cursor(self):
        if self.text_cursor.is_greater_than(self.border_cursor):
            self.cursor = self.text_cursor
        else:
            self.cursor = self.border_cursor

    def draw(self):
        self.draw_text()
        self.draw_borders()
        self.set_final_cursor()

    def draw_text(self):
        for row in self.rows:
            row.draw_text(self.text_cursor.copy())
            self.text_cursor.y_plus(row.max_height)

    def draw_borders(self):
        for row in self.rows:
            row.draw_borders(self.border_cursor.copy())
            self.border_cursor.y_plus(row.max_height)
