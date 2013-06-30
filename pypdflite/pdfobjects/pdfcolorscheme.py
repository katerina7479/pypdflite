from pdfcolor import PDFColor


class PDFColorScheme(object):
    """ ColorScheme is made up of three PDFColors,
        for the draw (stroke operations), fill, and text
        colors.

        The colors can be changed after the fact,
        but it may be more clear to create multiple
        PDFColorSchemes for different situations.

    """
    def __init__(self, drawcolor=None, fillcolor=None, textcolor=None):
        self.setDrawColor(drawcolor)
        self.setFillColor(fillcolor)
        self.setTextColor(textcolor)

    def setDrawColor(self, drawcolor):
        if drawcolor is None:
            drawcolor = PDFColor("d")
        elif isinstance(drawcolor, PDFColor) and drawcolor.colortype is "d":
            pass
        else:
            drawcolor.setColorType("d")
        self.drawcolor = drawcolor

    def setFillColor(self, fillcolor):
        if fillcolor is None:
            fillcolor = PDFColor("f")
        elif isinstance(fillcolor, PDFColor) and fillcolor.colortype is "f":
            pass
        else:
            fillcolor.setColorType("f")
        self.fillcolor = fillcolor
        self._setColorFlag()

    def setTextColor(self, textcolor):
        if textcolor is None:
            textcolor = PDFColor("t")
        elif isinstance(textcolor, PDFColor) and textcolor.colortype is "t":
            pass
        else:
            textcolor.setColorType("t")
        self.textcolor = textcolor
        self._setColorFlag()

    def _setColorFlag(self):
        if hasattr(self, "textcolor") and hasattr(self, "fillcolor"):
            if self.textcolor.isEqual(self.fillcolor):
                self.colorFlag = False
            else:
                self.colorFlag = True
        else:
            pass

    def _getColorFlag(self):
        return self.colorFlag

    def _getDrawColorString(self):
        return self.drawcolor._getColorString()

    def _getFillColorString(self):
        return self.fillcolor._getColorString()

    def _getTextColorString(self, text=None):
        s = self.fillcolor._getColorString()
        return s