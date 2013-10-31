

class PDFCursor(object):
    def __init__(self, x=20, y=720):
        self.xmin = 0
        self.xmax = 612
        self.ymin = 0
        self.ymax = 792

        self.x = x
        self.y = y

        self.dx = 2
        self.dy = 2

    def setBounds(self, xmin=0,  ymin=0, xmax=612, ymax=792):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

        self.x = self.x
        self.y = self.y

    def setDeltas(self, dx=2, dy=2):
        self.dx = dx
        self.dy = dy

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if value <= self.xmin:
            self._x = self.xmin
        elif value > self.xmax:
            raise ValueError("%s is > bounds %s" % (value, self.xmax))
        else:
            self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value >= self.ymin:
            self._y = self.ymin
        elif value < self.ymax:
            raise ValueError("%s is < bounds %s" % (value, self.ymax))
        else:
            self._y = value

    def xfit(self, testlength):
        if (self.x + testlength) >= self.xmax:
            return False
        else:
            return True

    def yfit(self, testlength):
        if (self.y + testlength) >= self.ymax:
            return False
        else:
            return True

    @property
    def xleft(self):
        return self.xmax - self.x

    @property
    def yleft(self):
        return self.y - self.ymin

    def _isCoordinate(self, testord):
        if isinstance(testord, PDFCursor):
            return True
        else:
            raise Exception("Not a valid PDFCursor object")

    def xIsGreaterThan(self, testord):
        self._isCoordinate(testord)
        if self.x > testord.x:
            return True
        else:
            return False

    def yIsGreaterThan(self, testord):
        self._isCoordinate(testord)
        if self.y < testord.y:
            return True
        else:
            return False

    def isGreaterThan(self, testord):
        self._isCoordinate(testord)
        if self.y < testord.y:
            return True
        elif self.y == testord.y:
            if self.x > testord.x:
                return True
        else:
            return False

    def isEqualTo(self, testord):
        self._isCoordinate(testord)
        if self.y == testord.y:
            if self.x == testord.x:
                return True
        else:
            return False

    def isLessThan(self, testord):
        self._isCoordinate(testord)
        if self.y > testord.y:
            return True
        elif self.y == testord.y:
            if self.x < testord.x:
                return True
        else:
            return False

    def copy(self):
        newcursor = self.__class__(self.x, self.y)
        newcursor.setBounds(self.xmin,  self.ymin, self.xmax, self.ymax)
        return newcursor

    def add(self, addord):
        self._isCoordinate(addord)
        x = self.x + addord.x
        y = self.y + addord.y
        return self.__class__(x, y)

    def subtract(self, subord):
        self._isCoordinate(subord)
        x = self.x - subord.x
        y = self.y - subord.y
        return self.__class__(x, y)

    def scale(self, scale):
        scale = float(scale)
        x = self.x * scale
        y = self.y * scale
        return self.__class__(x, y)

    def invert(self):
        return self.__class__(self.y, self.x)

    def xPlus(self, dx=None):
        if dx is None:
            self.x = self.x + self.dx
        else:
            self.x = self.x + dx

    def yPlus(self, dy=None):
        if dy is None:
            self.y = self.y - self.dy
        else:
            self.y = self.y - dy

    def xMinus(self, dx=None):
        if dx is None:
            self.x = self.x - self.dx
        else:
            self.x = self.x - dx

    def yMinus(self, dy=None):
        if dy is None:
            self.y = self.y + self.dy
        else:
            self.y = self.y + dy

    def xReset(self):
        self.x = self.xmin

    def yReset(self):
        self.y = self.ymin