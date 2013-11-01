

class PDFCursor(object):

    def __init__(self, x=20, y=20):
        self.xmin = 0
        self.xmax = 612
        self.ymin = 0
        self.ymax = 792

        self.x = x
        self.y = y

        self.dx = 2
        self.dy = 2

    def set_bounds(self, xmin=0,  ymin=0, xmax=612, ymax=792):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

        self.x = self.x
        self.y = self.y

    def set_deltas(self, dx=2, dy=2):
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
        if value <= self.ymin:
            self._y = self.ymin
        elif value > self.ymax:
            raise ValueError("%s is > bounds %s" % (value, self.ymax))
        else:
            self._y = value
            self._y_real = self.ymax-self._y

    def x_fit(self, test_length):
        if (self.x + test_length) >= self.xmax:
            return False
        else:
            return True

    def y_fit(self, test_length):
        if (self.y + test_length) >= self.ymax:
            return False
        else:
            return True

    @property
    def x_left(self):
        return self.xmax - self.x

    @property
    def y_left(self):
        return self.ymax - self.y

    def _is_coordinate(self, test_ordinate):
        if isinstance(test_ordinate, PDFCursor):
            return True
        else:
            raise Exception("Not a valid PDFCursor object")

    def x_is_greater_than(self, test_ordinate):
        self._is_coordinate(test_ordinate)
        if self.x > test_ordinate.x:
            return True
        else:
            return False

    def y_is_greater_than(self, test_ordinate):
        self._is_coordinate(test_ordinate)
        if self.y > test_ordinate.y:
            return True
        else:
            return False

    def is_greater_than(self, test_ordinate):
        self._is_coordinate(test_ordinate)
        if self.y > test_ordinate.y:
            return True
        elif self.y == test_ordinate.y:
            if self.x > test_ordinate.x:
                return True
        else:
            return False

    def is_equal_to(self, test_ordinate):
        self._is_coordinate(test_ordinate)
        if self.y == test_ordinate.y:
            if self.x == test_ordinate.x:
                return True
        else:
            return False

    def is_less_than(self, test_ordinate):
        self._is_coordinate(test_ordinate)
        if self.y < test_ordinate.y:
            return True
        elif self.y == test_ordinate.y:
            if self.x < test_ordinate.x:
                return True
        else:
            return False

    def copy(self):
        new_cursor = self.__class__(self.x, self.y)
        new_cursor.set_bounds(self.xmin,  self.ymin, self.xmax, self.ymax)
        return new_cursor

    def add(self, add_ordinate):
        self._is_coordinate(add_ordinate)
        x = self.x + add_ordinate.x
        y = self.y + add_ordinate.y
        return self.__class__(x, y)

    def subtract(self, sub_ordinate):
        self._is_coordinate(sub_ordinate)
        x = self.x - sub_ordinate.x
        y = self.y - sub_ordinate.y
        return self.__class__(x, y)

    def scale(self, scale):
        scale = float(scale)
        x = self.x * scale
        y = self.y * scale
        return self.__class__(x, y)

    def invert(self):
        return self.__class__(self.y, self.x)

    def x_plus(self, dx=None):
        if dx is None:
            self.x = self.x + self.dx
        else:
            self.x = self.x + dx

    def y_plus(self, dy=None):
        if dy is None:
            self.y = self.y + self.dy
        else:
            self.y = self.y + dy

    def x_minus(self, dx=None):
        if dx is None:
            self.x = self.x - self.dx
        else:
            self.x = self.x - dx

    def y_minus(self, dy=None):
        if dy is None:
            self.y = self.y - self.dy
        else:
            self.y = self.y - dy

    def x_reset(self):
        self.x = self.xmin

    def y_reset(self):
        self.y = self.ymin
