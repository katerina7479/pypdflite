

class PDFRow(object):
    def __init__(self, parent, font, color_scheme):
        self.parent = parent
        self.font = font
        self.color_scheme = color_scheme

        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)

    def draw_text(self, cursor):
        self.get_max_height()
        for cell in self.cells:
            cell.draw_text(cursor)
            cursor.x_plus(cell.max_width)

    def draw_borders(self, cursor):
        for cell in self.cells:
            cell.draw_borders(cursor)
            cursor.x_plus(cell.max_width)

    def get_max_height(self):
        self.max_height = 0
        for cell in self.cells:
            if cell.height > self.max_height:
                self.max_height = cell.height
        for cell in self.cells:
            cell.max_height = self.max_height
