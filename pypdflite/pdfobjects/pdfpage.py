from pdfmargin import PDFMargin
from pdfcursor import PDFCursor
from zlib import compress


class PDFPage(object):

    """ Defines the structure of an individual page.
        Margins are set by default. If you want to change
        them, it should be done through the Document object,
        or before any content is written to the page.

    """

    def __init__(self, orientation="P", layout="letter", margin=None):
        # Additional layout sizes may be added to this dictionary.
        # Width then height, in pixels, in portrait orientation.
        self.layout_dict = {'a3': (841.89, 1190.55),
                            'a4': (595.28, 841.89),
                            'a5': (420.94, 595.28),
                            'letter': (612, 792),
                            'legal': (612, 1008),
                            '11x17': (792, 1224)
                            }

        self.set_page_size(layout)

        # "P" or "L"
        self.orientation = orientation

        # Each page has a cursor.
        self.cursor = PDFCursor()

        # Initialize the Page Margin.
        self.margin = margin
        self.set_orientation(orientation)
        self.set_margins()

        self.orientation_change = False
        self.buffer = ""

    # Page may be retrieved and manipulated using these:
    def set_orientation(self, orientation="P"):
        self.orientation = orientation.lower()
        if(self.orientation == 'p' or self.orientation == 'portrait'):
            self.size = self.page_size
        elif(self.orientation == 'l' or self.orientation == 'landscape'):
            self.size = (self.page_size[1], self.page_size[0])
        else:
            raise Exception('Incorrect orientation: ', self.orientation)
        self._set_dimensions()
        self._set_bounds()

    def set_page_size(self, layout):
        """ Valid choices: 'a3, 'a4', 'a5', 'letter', 'legal', '11x17'.

        """
        self.layout = layout.lower()
        if self.layout in self.layout_dict:
            self.page_size = self.layout_dict[self.layout]
        else:
            raise Exception('Unknown page layout: ', self.layout)

    def set_margins(self, margin=None):
        if margin is None:
            self.margin = PDFMargin()
        elif isinstance(margin, PDFMargin):
            self.margin = margin
        else:
            raise Exception("Invalid Margin object")
        self._set_dimensions()
        self._set_bounds()

    def get_margins(self):
        return self.margin

    # Private methods for building pages
    def _compress(self):
        """ Uses zlib to compress page buffers. Compression
            option is enabled through PDFLite object's
            setCompression method.

        """
        self.buffer = compress(self.buffer)

    def _set_index(self, value):
        self.index = value

    def _set_dimensions(self):
        self.width = self.size[0]
        self.height = self.size[1]

    def _change_orientation(self):
        if self.orientation_change is False:
            self.size = (self.size[1], self.size[0])
            self.orientation_change = True
            self._set_dimensions()
            self._set_bounds()
        else:
            pass

    def _set_cursor(self, cursor):
        self.cursor = cursor
        self._set_bounds()

    def _set_bounds(self):
        if self.margin is None:
            xmin = 0
            xmax = self.size[0]
            ymin = 0
            ymax = self.size[1]
        else:
            xmin = 0 + self.margin.left
            xmax = self.size[0] - self.margin.right
            ymin = 0 + self.margin.top
            ymax = self.size[1] - self.margin.bottom

        self.cursor.set_bounds(xmin, ymin, xmax, ymax)

    def _add_newline(self, font, number=1):
        self.cursor.y_plus((font.line_size * number))
        self.cursor.x_reset()

    def _add_indent(self, font, number=4):
        self.cursor.x_plus(number * font._string_width(' '))
