

class PDFCellBorder(object):
    def __init__(self, linesize, style, color):
        self.linesize = linesize
        self.style = self.set_style(style)
        self.color = color

    def set_style()