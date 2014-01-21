

class PDFColumn(object):
    def __init__(self, parent):
        self.parent = parent
        self.cells = []
        self.max_width = 0

    def _add_cell(self, cell):
        self.cells.append(cell)

    def _set_max_width(self, value):
        self.max_width = value

    def _get_max_width(self):
        for cell in self.cells:
            if cell.width > self.max_width and cell.text_wrap is False:
                self.max_width = cell.width

        for cell in self.cells:
            cell._set_max_width(self.max_width)

    def _finish(self):
        self._get_max_width()
