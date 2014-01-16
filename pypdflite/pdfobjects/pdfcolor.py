from colorref import color_reference


class PDFColor(object):
    """ Black by default.

    """

    def __init__(self, color_type="d", r=0, g=0, b=0, name=None):

        # Get color dictionary
        self.color_dict = color_reference

        # Type may be "draw", "fill", or "text"
        self.type_list = ["d", "f", "t"]
        self.set_type(color_type)

        if name is not None:
            self.set_color_by_name(name, r, g, b)
        else:
            self.set_color_by_number(r, g, b)

    def __repr__(self):
        return '%s, %s, %s' % (self.red, self.green, self.blue)

    def set_type(self, color_type):
        color_type = color_type[0].lower()  # Just get the first letter right.

        # Check to see if it's in the allowed types
        if color_type in self.type_list:
            self.color_type = color_type
        else:
            raise TypeError(
                "Invalid color_type %s, must be draw, fill or text" %
                color_type)

    def _set_from_dict(self, name):
        self.value = self.color_dict[name]  # Triplet from color ref
        self.name = name
        self.red = self.value[0]
        self.blue = self.value[1]
        self.green = self.value[2]

    def set_color_by_name(self, name, r, g, b):
        name = name.lower()
        if name in self.color_dict:
            # Ignore r, g, b
            self._set_from_dict(name)
        elif (r != 0 or g != 0 or b != 0):
            # Not default, assume defining new color
            # (If all 0, then it's black and already defined)
            # Could check for int between 0 - 255 here.
            self.color_dict[name] = (r, g, b)
            self._set_from_dict(name)
        else:
            raise ValueError("Color (%s) not found." % name)

    def set_color_by_number(self, r, g, b):
        self.red = r
        self.blue = b
        self.green = g

        self.value = (self.red, self.blue, self.green)
        self.name = None

    def is_equal(self, test_color):
        "Equality test"
        if test_color is None:
            ans = False
        elif test_color.color_type != self.color_type:
            ans = False
        elif self.name == test_color.name:
            ans = True
        elif (self.red == test_color.red and
              self.blue == test_color.blue and
              self.green == test_color.green):
            ans = True
        else:
            ans = False
        return ans

    def _get_color_string(self):
        "Adobe output string for defining colors"
        if self.color_type == "d":
            if self.name is "black":
                s = '%.3f G' % 0
            else:
                s = '%.3f %.3f %.3f RG' % (
                    self.red / 255.0, self.green / 255.0, self.blue / 255.0)
        elif self.color_type == 'f' or self.color_type == 't':
            if self.name is "black":
                s = '%.3f g' % 0
            else:
                s = '%.3f %.3f %.3f rg' % (
                    self.red / 255.0, self.green / 255.0, self.blue / 255.0)
        return s


    def copy(self):
        new_color = PDFColor(self.color_type, self.red, self.green, self.blue, self.name)
        return new_color
