

class PDFColumn(object):
    def __init__(self, parent):
        self.parent = parent
        self.cells = []
        self.max_width = 0

    def add_cell(self, cell):
        self.cells.append(cell)

    def get_max_width(self):
        for cell in self.cells:
            if cell.width > self.max_width and cell.text_wrap is False:
                self.max_width = cell.width
        for cell in self.cells:
            cell.set_max_width(self.max_width)

    def _finish(self):
        self.get_max_width()

    def set_max_width(self, value):
        self.max_width = value
