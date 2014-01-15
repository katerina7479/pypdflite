from pdfrow import PDFRow
from pdfcolumn import PDFColumn
from pdfcell import PDFCell


class PDFTable(object):
    def __init__(self, session, page, rows, cols, cursor):
        self.session = session
        self.page = page

        self.number_of_rows = rows
        self.number_of_columns = cols

        self.cursor = cursor
        self.text_cursor = self.cursor.copy()
        self.border_cursor = self.cursor.copy()

        self._initiate_cells()

    def _initiate_cells(self):
        self.rows = []
        self.columns = []

        for x in range(self.number_of_columns):
            self.columns.append(PDFColumn(parent=self))


        for x in range(self.number_of_rows):
            self.rows.append(PDFRow(self, x, self.number_of_columns,
                                    self.text_cursor, self.border_cursor))

        for x in range(self.number_of_rows):
            for y in range(self.number_of_columns):
                self.columns[y].cells.append(self.rows[x].cells[y])


    def write(self, row, col, text, format):
        cell = self.rows[row][col]
        cell.set_text(text)
        cell.set_format(format)

    def _compile(self):
        for row in self.rows:
            for cell in row:
                cell._compile()

        for col in self.columns:
            col._finish()

        for row in self.rows:
            row._finish()
            for cell in row:
                cell._finish()

        self.rows[0]._advance_first_row()

    def draw(self):
        self._compile()
        self._draw_borders()
        self._draw_text()
        self._set_final_cursor()

    def _draw_text(self):
        for i in range(len(self.rows)):
            self.rows[i].draw_text()
            self.text_cursor.x_reset()
            if (i + 1) < len(self.rows):
                self.text_cursor.y_plus(self.rows[i + 1].max_height)

    def _draw_borders(self):
        for i in range(len(self.rows)):
            self.rows[i].draw_borders()
            self.border_cursor.x_reset()
            if (i + 1) < len(self.rows):
                self.border_cursor.y_plus(self.rows[i].max_height)

    def _set_final_cursor(self):
        if self.text_cursor.is_greater_than(self.border_cursor):
            self.cursor = self.text_cursor
        else:
            self.cursor = self.border_cursor


    def set_column_width(self, column, value):
        self.columns[column].set_max_width(value)

    def set_row_height(self, row, value):
        self.rows[row].set_max_height(value)
