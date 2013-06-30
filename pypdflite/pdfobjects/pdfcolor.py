from colorref import ColorRef


class PDFColor(object):
    def __init__(self, colortype="d", r=0, g=0, b=0, name=None):
        self.colordict = ColorRef

        self.typelist = ["d", "f", "t"]
        self.setColorType(colortype)

        if name is not None:
            self.setColorByName(name, r, g, b)
        else:
            self.setColorByNumber(r, g, b)

    def setColorType(self, colortype):
        colortype = colortype[0].lower()  # Just get the first letter right.
        if colortype in self.typelist:
            self.colortype = colortype
        else:
            raise TypeError("Invalid colortype %s, must be draw, fill or text" % colortype)

    def _setFromDict(self, name):
        self.value = self.colordict[name]
        self.name = name
        self.red = self.value[0]
        self.blue = self.value[1]
        self.green = self.value[2]

    def setColorByName(self, name, r, g, b):
        name = name.lower()
        if name in self.colordict:
            self._setFromDict(name)
        elif (r != 0 or g != 0 or b != 0):
            # Not default, assume defining new color
            self.colordict[name] = (r, g, b)
            self._setFromDict(name)
        else:
            raise ValueError("Color (%s) not found." % name)

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

    def _getColorString(self):
        if self.colortype == "d":
            if self.name is "black":
                s = '%.3f G' % 0
            else:
                s = '%.3f %.3f %.3f RG' % (self.red/255.0, self.green/255.0, self.blue/255.0)
        elif self.colortype == 'f' or self.colortype == 't':
            if self.name is "black":
                s = '%.3f g' % 0
            else:
                s = '%.3f %.3f %.3f rg' % (self.red/255.0, self.green/255.0, self.blue/255.0)
        return s
