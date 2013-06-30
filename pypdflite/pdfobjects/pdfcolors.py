from colorref import ColorRef


class PDFColorScheme(object):
    def __init__(self, draw=None, fill=None, text=None):
        self._setColors(draw, fill, text)
        self._setColorFlag()

    def _setColors(self, draw=None, fill=None, text=None):
        if draw is None and hasattr(self, 'draw'):
            pass
        elif draw is None:
            self.draw = PDFColor()
        elif isinstance(draw, PDFColor):
            self.draw = draw
        else:
            raise ValueError("Invalid color object")

        if fill is None and hasattr(self, 'fill'):
            pass
        elif fill is None:
            self.fill = PDFColor()
        elif isinstance(fill, PDFColor):
            self.fill = fill
        else:
            raise ValueError("Invalid color object")

        if text is None and hasattr(self, 'text'):
            pass
        elif text is None:
            self.text = PDFColor()
        elif isinstance(text, PDFColor):
            self.text = text
        else:
            raise ValueError("Invalid color object")

    def _setColorFlag(self):
        if self.fill.isEqual(self.text):
            self.colorflag = False
        else:
            self.colorflag = True

    def getDrawColor(self):
        if self.draw.name is 'black':
            s = '%.3f G' % 0
        else:
            s = '%.3f %.3f %.3f RG' % (self.draw.red/255.0, self.draw.green/255.0, self.draw.blue/255.0)
        return s

    def getFillColor(self):
        if self.fill.name is 'black':
            s = '%.3f g' % 0
        else:
            s = '%.3f %.3f %.3f rg' % (self.fill.red/255.0, self.fill.green/255.0, self.fill.blue/255.0)
        return s

    def getTextColor(self):
        if self.text.name is 'black':
            s = '%.3f g' % 0
        else:
            s = '%.3f %.3f %.3f rg' % (self.text.red/255.0, self.text.green/255.0, self.text.blue/255.0)
        return s

        # Note (not written, if color flag is True, then the string must be wrapped for output as follows:
        # s = 'q ' + s (from here) + ' ' + text s + ' Q'


class PDFColor(object):
    def __init__(self, r=0, g=0, b=0, color=None):
        self.colordict = ColorRef

        if color is not None:
            self.setColorByName(color.lowercase())
        else:
            self.setColorByNumber(r, g, b)

    def _setFromDict(self, color):
        self.value = self.colordict[color]
        self.name = color
        self.red = self.value[0]
        self.blue = self.value[1]
        self.green = self.value[2]

    def setColorByName(self, color, r, g, b):
        if color in self.colordict:
            self._setFromDict(color)
        elif (r != 0 or g != 0 or b != 0):
            # Not default, assume defining new color
            self.colordict[color] = (r, g, b)
            self._setFromDict(color)
        else:
            raise ValueError("Color (%s) not found." % color)

    def setColorByNumber(self, r, g, b):
        self.red = r
        self.blue = b
        self.green = g
        self.value = (self.red, self.blue, self.green)
        self.name = None

    def isEqual(self, testcolor):
        if self.name == testcolor.name:
            ans = True
        elif (self.red == testcolor.red and
              self.blue == testcolor.blue and
              self.green == testcolor.green):
            ans = True
        else:
            ans = False
        return ans