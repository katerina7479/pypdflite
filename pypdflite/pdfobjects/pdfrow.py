from pdfcell import PDFCell


class PDFRow(object):
    def __init__(self, parent, row_index, num_cols, textcursor, bordercursor):
        self.parent = parent
        self.row_index = row_index
        self.num_cols = num_cols
        self.text_cursor = textcursor
        self.border_cursor = bordercursor
        self.cells = []
        self._make_cells()
        self.max_height = 0

    def __getitem__(self, key):
        return self.cells[key]

    def _make_cells(self):
        for x in range(0, self.num_cols):
            cell = PDFCell(self.parent, self.row_index, x, self.text_cursor, self.border_cursor)
            self.cells.append(cell)

    def _draw_text(self):
        for cell in self.cells:
            cell._draw_text()

    def _draw_borders(self):
        for cell in self.cells:
            cell._draw_borders()

    def _set_borders(self):
        for cell in self.cells:
            cell._set_borders()
            self.border_cursor.x_plus(cell.max_width)

    def _draw_fill(self):
        for cell in self.cells:
            cell._draw_fill()

    def _finish(self):
        for cell in self.cells:
            if cell.height > self.max_height:
                self.max_height = cell.height
        for cell in self.cells:
            cell._set_max_height(self.max_height)

    def _advance_first_row(self):
        self.cells[0]._advance_initial()

    def _set_max_height(self, value):
        self.max_height = value
