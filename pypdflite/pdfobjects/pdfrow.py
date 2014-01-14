

class PDFRow(object):
    def __init__(self, parent, font, color_scheme, number, textcursor, bordercursor):
        self.parent = parent
        self.font = font
        self.color_scheme = color_scheme
        self.number = number
        self.textcursor = textcursor
        self.bordercursor = bordercursor
        self.cells = []

    def __repr__(self):
        mystring = ''
        for cell in self.cells:
            mystring += cell.text + ' '
        return mystring

    def add_cell(self, cell):
        self.cells.append(cell)

    def draw_text(self):
        for cell in self.cells:
            cell.draw_text()

    def draw_borders(self):
        for cell in self.cells:
            cell.draw_borders()
            self.bordercursor.x_plus(cell.max_width)

    def _finish(self):
        self.max_height = 0
        for cell in self.cells:
            if cell.height > self.max_height:
                self.max_height = cell.height

        for cell in self.cells:
            cell.max_height = self.max_height

    def _advance_first_row(self):
        self.cells[0]._advance_initial()
