from colorref import color_reference


class PDFColor(object):
    def __init__(self, name=None, r=0, g=0, b=0):
        # Get color dictionary
        self.color_dict = color_reference

        # Type may be "draw", "fill", or "text"
        self.type_list = ["d", "f", "t"]
        self.color_type = 'd'

        if name is not None:
            self.set_color_by_name(name)
        else:
            self.set_color_by_number(r, g, b)

    def __repr__(self):
        return "%s: (%s, %s, %s)" % (self.color_type, self.red, self.green, self.blue)

    def set_color_by_name(self, name):
        name = name.lower()
        if name in self.color_dict:
            self._set_from_dict(name)
        else:
            raise ValueError("Color (%s) not found." % name)

    def set_color_by_number(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b

        self.value = (self.red, self.green, self.blue)
        self.name = None

    def copy(self):
        new_color = PDFColor(self.name, self.red, self.green, self.blue)
        new_color._set_type(self.color_type)
        return new_color

    # Used by other objects
    def _set_type(self, color_type):
        color_type = color_type[0].lower()  # Just get the first letter right.

        # Check to see if it's in the allowed types
        if color_type in self.type_list:
            self.color_type = color_type
        else:
            raise TypeError(
                "Invalid color_type %s, must be draw, fill or text" % color_type)

    def _set_from_dict(self, name):
        self.value = self.color_dict[name]  # Triplet from color ref
        self.name = name
        self.red = self.value[0]
        self.green = self.value[1]
        self.blue = self.value[2]

    def _is_equal(self, test_color):
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
