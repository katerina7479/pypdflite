

class PDFCursor(object):

    def __init__(self, x=20, y=20, boundary_flag=False):
        """ Cursor object. Initialize with placement of cursor.
            This cursor places the origin (0,) at the upper left hand
            side of the page. X increases horizontally, and y increases
            vertically down the page. Note: This is different from the way
            Adobe sets the origin. They place the origin at the lower
            left hand corner, and y increases from the bottom to the
            top of the page. I feel that their way required more explanation,
            and was less intuitive. THerefore, I have provided the y_prime
            property for use in outputting the cursor data at document
            generation.

        """
        self._x = 0
        self._y = 0

        # Call to set default boundaries and increments.
        if boundary_flag is True:
            self.set_bounds(xmin=x, ymin=y)
        else:
            self.set_bounds()
        self.set_deltas()

        self.x = x
        self.y = y

    def __repr__(self):
        return "(%s, %s)" % (self.x, self.y)

    # May be used to change boundaries, and small offsets.
    def set_bounds(self, xmin=0, ymin=0, xmax=612, ymax=792):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

        # Setter called in case original placement
        # of cursor was out of newly set bounds
        self.x = self.x
        self.y = self.y

    def set_deltas(self, dx=2, dy=2):
        self.dx = dx
        self.dy = dy

    # Setters / getters for x & y
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value=0):
        # If in left margin, sets to minimum value.
        if value <= self.xmin:
            self._x = self.xmin
        elif value > self.xmax:
            # Consider resetting to minimum as well?
            #print "X ord %s is > bounds %s" % (value, self.xmax)
            self._x = value
        else:
            self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value=0):
        if value <= self.ymin:
            self._y = self.ymin
        elif value > self.ymax:
            #print "Y ord %s is > bounds %s" % (value, self.ymax)
            self._y = value
        else:
            self._y = value

    @property
    def y_prime(self):
        return self.ymax - self.y

    def x_fit(self, test_length):
        " Test to see if the line can has enough space for the given length. "
        if (self.x + test_length) >= self.xmax:
            return False
        else:
            return True

    def y_fit(self, test_length):
        " Test to see if the page has enough space for the given text height. "
        if (self.y + test_length) >= self.ymax:
            return False
        else:
            return True

    @property
    def x_left(self):
        " Space remaining on line. "
        return self.xmax - self.x

    @property
    def y_left(self):
        " Space remaining on page. "
        return self.ymax - self.y

    # Equality methods
    def _is_coordinate(self, test_ordinate):
        " Test to see if object is a proper PDFCursor. "
        if isinstance(test_ordinate, PDFCursor):
            return True
        else:
            raise Exception("Not a valid PDFCursor object")

    def x_is_greater_than(self, test_ordinate):
        " Comparison for x coordinate"
        self._is_coordinate(test_ordinate)
        if self.x > test_ordinate.x:
            return True
        else:
            return False

    def y_is_greater_than(self, test_ordinate):
        "Comparison for y coordinate"
        self._is_coordinate(test_ordinate)
        if self.y > test_ordinate.y:
            return True
        else:
            return False

    def is_greater_than(self, test_ordinate):
        " Comparison for both ordinates, prioritizing the y direction. "
        self._is_coordinate(test_ordinate)
        if self.y > test_ordinate.y:
            return True
        elif self.y == test_ordinate.y:
            if self.x > test_ordinate.x:
                return True
        else:
            return False

    def is_equal_to(self, test_ordinate):
        " Test to see if coordinates are equal to each other. "
        self._is_coordinate(test_ordinate)
        if self.y == test_ordinate.y:
            if self.x == test_ordinate.x:
                return True
        else:
            return False

    def is_less_than(self, test_ordinate):
        " Comparison for both ordinates, prioritizing the y direction."
        self._is_coordinate(test_ordinate)
        if self.y < test_ordinate.y:
            return True
        elif self.y == test_ordinate.y:
            if self.x < test_ordinate.x:
                return True
        else:
            return False

    # Returns a new cursor
    def copy(self):
        " Create a copy, and return it."
        new_cursor = self.__class__(self.x, self.y)
        new_cursor.set_bounds(self.xmin, self.ymin, self.xmax, self.ymax)
        new_cursor.set_deltas(self.dx, self.dy)
        return new_cursor

    def add(self, add_ordinate):
        " Add two coordinates to each other, return new coordinate. "
        self._is_coordinate(add_ordinate)
        x = self.x + add_ordinate.x
        y = self.y + add_ordinate.y
        return self.__class__(x, y)

    def subtract(self, sub_ordinate):
        " Subtract two coordinates from each other, suppress negatives. "
        self._is_coordinate(sub_ordinate)
        x = abs(self.x - sub_ordinate.x)
        y = abs(self.y - sub_ordinate.y)
        return self.__class__(x, y)

    def scale(self, scale):
        " Return scaled coordinate"
        scale = float(scale)
        x = self.x * scale
        y = self.y * scale
        return self.__class__(x, y)

    def invert(self):
        " Return inverse coordinate. "
        return self.__class__(self.y, self.x)

    # Changes this cursor
    def x_plus(self, dx=None):
        " Mutable x addition. Defaults to set delta value. "
        if dx is None:
            self.x = self.x + self.dx
        else:
            self.x = self.x + dx

    def y_plus(self, dy=None):
        " Mutable y addition. Defaults to set delta value. "
        if dy is None:
            self.y = self.y + self.dy
        else:
            self.y = self.y + dy

    def x_reset(self):
        " Resets x to xmin."
        self.x = self.xmin

    def y_reset(self):
        " Resets y to ymin."
        self.y = self.ymin
