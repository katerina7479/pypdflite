

class PDFColumn(object):
    def __init__(self, parent, font, color_scheme):
        self.parent = parent
        self.font = font
        self.color_scheme = color_scheme

        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)

    def get_max_sizes(self):
        self.max_width = 0
        for cell in self.cells:
            if cell.width > self.max_width:
                self.max_width = cell.width
        for cell in self.cells:
            cell.max_width = self.max_width
