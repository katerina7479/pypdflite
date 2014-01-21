from pdfrow import PDFRow
from pdfcolumn import PDFColumn
from pdfcell import PDFCell


class PDFTable(object):
    def __init__(self, session, page, rows, cols, cursor, def_font):
        self.session = session
        self.page = page
        self.font = def_font
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

    # Public Methods, called to create table
    def write(self, row, col, text, format=None):
        cell = self.rows[row][col]
        cell._set_text(text)
        if format is not None:
            cell._set_format(format)

    def write_row(self, row, col_start, data, format):
        i = 0
        for c in range(col_start, col_start + len(data)):
            self.write(row, c, data[i], format)
            i += 1

    def write_column(self, row_start, col, data, format):
        i = 0
        for r in range(row_start, row_start + len(data)):
            self.write(r, col, data[i], format)
            i += 1

    def set_format(self, row, col, format):
        cell = self.rows[row][col]
        cell.set_format(format)

    def set_format_row(self, row, col_start, format):
        for c in range(col_start, self.number_of_columns):
            self.set_format(row, c, format)

    def set_format_column(self, row_start, col, format):
        for r in range(row_start, self.number_of_rows):
            self.set_format(r, col, format)

    def set_column_width(self, column, value):
        self.columns[column]._set_max_width(value)

    def set_row_height(self, row, value):
        self.rows[row]._set_max_height(value)

    # Private methods to build table
    def _draw(self):
        """ Don't use this, use document.draw_table """
        self._compile()
        self.rows[0]._advance_first_row()
        self._set_borders()
        self._draw_fill()
        self._draw_borders()
        self._draw_text()
        self._set_final_cursor()

    def _draw_text(self):
        for i in range(len(self.rows)):
            self.rows[i]._draw_text()
            self.text_cursor.x_reset()
            if (i + 1) < len(self.rows):
                self.text_cursor.y_plus(self.rows[i + 1].max_height)

    def _set_borders(self):
        for i in range(len(self.rows)):
            self.rows[i]._set_borders()
            self.border_cursor.x_reset()
            if (i + 1) < len(self.rows):
                self.border_cursor.y_plus(self.rows[i].max_height)

    def _draw_borders(self):
        for i in range(len(self.rows)):
            self.rows[i]._draw_borders()

    def _draw_fill(self):
        for i in range(len(self.rows)):
            self.rows[i]._draw_fill()

    def _set_final_cursor(self):
        if self.text_cursor.is_greater_than(self.border_cursor):
            self.cursor = self.text_cursor
        else:
            self.cursor = self.border_cursor

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
