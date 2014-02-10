import os, sys
from pdfobjects.pdffont import PDFFont, CORE_FONTS
from pdfobjects.pdfpage import PDFPage
from pdfobjects.pdftext import PDFText
from pdfobjects.pdfcursor import PDFCursor
from pdfobjects.pdfline import PDFLine
from pdfobjects.pdfcolor import PDFColor
from pdfobjects.pdfrectangle import PDFRectangle
from pdfobjects.pdftable import PDFTable
from pdfobjects.pdfimage import PDFImage
from pdfobjects.pdfpng import PDFPNG
from pdfobjects.pdfjpg import PDFJPG
from pdfobjects.pdfttfonts import PDFTTFont
from pdfobjects.pdfmargin import PDFMargin
from pdfobjects.pdfcellformat import PDFCellFormat


class PDFDocument(object):

    """ The Document object is the base class that
        is used to add and manage the content of the
        pdf file.

        Document maintains lists of pages and other
        resources, provides for default selections,
        which can be changed through the convinence
        methods.

        Note that page and text objects do not maintain
        fonts themselves. If they must use them (for
        calculating widths or such), they must have
        the current font passed to them.

    """

    def __init__(self, session, orientation, layout):
        "Sets up a standard default document."
        self.session = session
        self.pages = []
        self.fonts = []
        self.fontkeys = []               # array of used fonts

        self.images = []
        self.imagekeys = []
        self.image_filter = None

        self.margins = None
        self.orientation_default = orientation
        self.layout_default = layout

        self.diffs = []

        self._set_defaults()

    # Set Defaults
    def _set_defaults(self):
        "Set color scheme & font to defaults."
        self._set_color_scheme()
        self._set_default_font()
        self.add_page()     # add first page

    def _set_color_scheme(self, draw_color=None, fill_color=None, text_color=None):
        """ Default color object is black letters
            & black lines.

        """
        if draw_color is None:
            draw_color = PDFColor()
            draw_color._set_type('d')
        if fill_color is None:
            fill_color = PDFColor()
            fill_color._set_type('f')
        if text_color is None:
            text_color = PDFColor()
            text_color._set_type('t')

        self.draw_color = draw_color
        self.fill_color = fill_color
        self.text_color = text_color

    def set_text_color(self, color):
        self.text_color = color

    def set_fill_color(self, color):
        self.fill_color = color

    def set_draw_color(self, color):
        self.draw_color = color

    def _set_default_font(self):
        """ Internal method to set the
            initial default font. Change
            the font using set_font method.

        """
        self.font = PDFFont(self.session)
        self.font._set_index()
        self.fonts.append(self.font)
        self.fontkeys.append(self.font.font_key)

    # Public methods, main interface
    # Pages
    def add_page(self, page=None):
        """ May generate and add a PDFPage
            separately, or use this to generate
            a default page.

        """
        if page is None:
            self.page = PDFPage(self.orientation_default, self.layout_default, self.margins)
        else:
            self.page = page
        self.page._set_index(len(self.pages))
        self.pages.append(self.page)
        currentfont = self.font
        self.set_font(font=currentfont)
        self.session._reset_colors()

    def get_page(self):
        "Returns reference to current page object."
        return self.page

    def set_margins(self, left, top=None, right=None, bottom=None):
        if isinstance(left, PDFMargin):
            self.margins = left
        else:
            self.margins = PDFMargin(left, top, right, bottom)

    def add_page_numbers(self, location='right', font=None, cursor=None, color=None, text1="Page %s", text2=None):
        self.page_numbers = location
        self.page_numbers_font = font
        self.page_numbers_cursor = cursor
        self.page_numbers_color = color
        self.page_numbers_text1 = text1
        self.page_numbers_text2 = text2

    # Cursor
    def get_new_cursor(self):
        " Returns a new default cursor "
        return PDFCursor()

    def set_cursor(self, x=None, y=None):
        if x is not None and isinstance(x, PDFCursor):
            self.page.cursor = x
        elif x is not None and y is not None:
            self.page.cursor = PDFCursor(x, y, True)
        else:
            raise Exception("Invalid cursor input")

    # Font
    def set_font(self, family=None, style='', size=None, font=None):
        """ Set the document font object, size given in points.
            If family, style, and/or size is given, generates
            a new Font object, checks to see if it is already
            in use, and selects it.

            May also use the font keyword to add an already
            instantiated PDFFont object.

        """
        if font:
            testfont = font
        elif isinstance(family, PDFFont):
            testfont = family
        else:
            # If size is not defined, keep the last size.
            if size is None:
                size = self.font.font_size

            # Create a font from givens to test its key
            if family in CORE_FONTS:
                testfont = PDFFont(self.session, family, style, size)
            else:
                testfont = PDFTTFont(self.session, family, style, size)

        testkey = testfont.font_key

        if testkey in self.fontkeys:
            index = self.fontkeys.index(testkey)
            self.font = self.fonts[index]
            if size != self.font.font_size:
                self.font._set_size(size)
            if style != self.font.style:
                self.font._set_style(style)
        else:
            self.font = testfont
            self._register_new_font(self.font)

        self.font.is_set = False

        if(self.page.index > 0):
                self.session._out('BT /F%d %.2f Tf ET' %
                                  (self.font.index, self.font.font_size),
                                  self.page)
                self.font.is_set = True
        return self.font

    def get_font(self):
        """ Get the current font object. Useful for storing
            in variables, and switching between styles.

        """
        return self.font

    def set_font_size(self, size):
        "Convinence method for just changing font size."
        if(self.font.font_size == size):
            pass
        else:
            self.font._set_size(size)

    def get_available_tt(self):
        ttfont = PDFTTFont()
        famlies = ttfont._get_available_font_families()
        print famlies
        return famlies

    # Writing
    def add_text(self, text, cursor=None):
        """ Input text, short or long. Writes in order, within the
            pre-defined page boundaries. Use add_newline as a return
            character. Sequential add_text commands will print without
            additional whitespace.

            Currently all "left-justified", although that may change in
            future version.

        """
        if cursor is None:
            cursor = self.page.cursor

        if '\n' in text:
            text_list = text.split('\n')
            for text in text_list:
                text = PDFText(self.session, self.page, text, self.font, self.text_color, cursor)
                self.add_newline()
        else:
            text = PDFText(self.session, self.page, text, self.font, self.text_color, cursor)

    def add_newline(self, number=1):
        """ Starts over again at the new line. If number is specified,
            it will leave multiple lines.
        """
        if isinstance(number, int):
            try:
                self.page._add_newline(self.font, number)
            except ValueError:
                self.add_page()
        else:
            raise TypeError("Number of newlines must be an integer.")

    def add_indent(self, spaces=4):
        """ Adds a standard tab of 4 spaces.
        """
        self.page._add_indent(self.font, spaces)

    def start_block_indent(self, px=20):
        self.px = px
        self.set_cursor(self.page.cursor.x + self.px, self.page.cursor.y)

    def end_block_indent(self):
        self.set_cursor(self.page.cursor.x - self.px, self.page.cursor.y)

    def add_list(self, *args, **kwargs):
        if 'bullet' in kwargs:
            if kwargs['bullet'] == 1:
                bullet_code = 149
            elif kwargs['bullet'] == 2:
                bullet_code = 186
            elif kwargs['bullet'] == 3:
                bullet_code = 150
        else:
            bullet_code = 149

        char = chr(bullet_code)

        if 'force' in kwargs and kwargs['force'] is True:
            saved_font = self.get_font()
            for arg in args:
                helvetica = self.set_font(family='helvetica', size=saved_font.font_size)
                self.add_text(char)
                self.set_font(saved_font)
                self.add_text(' %s' % arg)
                self.add_newline(2)
        else:
            for arg in args:
                self.add_text(char)
                self.add_text(' %s' % arg)
                self.add_newline(2)

    def add_line(self, x1=None, y1=None, x2=None, y2=None,
                 cursor1=None, cursor2=None, style="solid"):
        if cursor1 is not None:
            if cursor2 is not None:
                pass
        else:
            cursor1 = PDFCursor(x1, y1)
            cursor2 = PDFCursor(x2, y2)

        myline = PDFLine(self.session, self.page, cursor1, cursor2, self.draw_color, style)
        myline._draw()

    def draw_horizonal_line(self):
        end_cursor = self.page.cursor.copy()
        end_cursor.x = end_cursor.xmax

        myline = PDFLine(self.session, self.page, self.page.cursor, end_cursor, self.draw_color, None)
        myline._draw()

    def draw_rectangle(self, x1=None, y1=None, x2=None, y2=None,
                       width=None, height=None, cursor1=None, cursor2=None,
                       style='S', size=1):
        if cursor1 is not None:
            if cursor2 is not None:
                pass
            elif width is not None and height is not None:
                dims = PDFCursor(width, height)
                cursor2 = cursor1.add(dims)
            elif x2 is not None and y2 is not None:
                cursor2 = PDFCursor(x2, y2)
            else:
                raise Exception("Rectangle not defined")
        else:
            if x1 is not None and y1 is not None:
                cursor1 = PDFCursor(x1, y1)
                if x2 is not None and y2 is not None:
                    cursor2 = PDFCursor(x2, y2)
                elif width is not None and height is not None:
                    dims = PDFCursor(width, height)
                    cursor2 = cursor1.add(dims)
                else:
                    raise Exception("Rectangle not defined")
            else:
                raise Exception("Rectangle not defined")

        rectangle = PDFRectangle(self.session, self.page,
                                 cursor1, cursor2,
                                 self.draw_color, self.fill_color,
                                 style, size)

        rectangle._draw()

    def add_table(self, rows, columns, cursor=None):
        if cursor is None:
            cursor = self.page.cursor

        table = PDFTable(self.session, self.page, rows, columns, cursor, self.font)

        return table

    def draw_table(self, table):
        if isinstance(table, PDFTable):
            table._draw()
            self.page.cursor = table.cursor
        else:
            raise Exception("Invalid Table")

    def add_cell_format(self, data=None, default_font=None):
        if default_font is None:
            default_font = self.font
        if data is None:
            data = {}
        format = PDFCellFormat(data, default_font)
        return format

    def add_image(self, image=None, name=None):
        if isinstance(image, PDFImage):  # It's an image object
            myimage = self._get_image(image.name)
            if not myimage:
                self._register_new_image(image)
            myimage = image

        elif isinstance(image, str):  # Name or path
            image_string = image
            if image_string.find('.') == -1:  # Not a path, treat as name
                myimage = self._get_image(image_string)
                if not myimage:
                    raise Exception('Not a proper image path')
            else:  # Is a path
                if not name:  # But it doesn't have a name specified.
                    name = os.path.splitext(image_string)[0]  # Specify it
                myimage = self._get_image(name)
                if not myimage:  # New image
                    extension = os.path.splitext(image_string)[1]
                    if extension == '.png':
                        myimage = PDFPNG(self.session, image_string, name)
                    elif extension == '.jpg':
                        myimage = PDFJPG(self.session, image_string, name)
                    else:
                        raise Exception("Image format %s not supported" % extension)
                    self._register_new_image(myimage)

        return myimage

    def draw_image(self, image, cursor=None, width=None, height=None):
        if isinstance(image, PDFImage):  # It's an image object
            myimage = self._get_image(image.name)
        else:
            try:
                myimage = self._get_image(image)
            except:
                raise Exception("%s is an invalid image. Add it first.")

        if not cursor:
            imagecursor = self.page.cursor
        else:
            imagecursor = cursor
        myimage._set_cursor(imagecursor)
        myimage._set_size(width, height)
        myimage._draw(self.page)

        # If a cursor was not specified, place at the end
        if not cursor:
            self.page.cursor = myimage.cursor

    def set_background_image(self, image):
        margins = PDFMargin(0, 0, None, None)
        self.page.set_margins(margins)
        background_cursor = PDFCursor(0, 0)
        myimage = self.add_image(image)
        self.draw_image(myimage, background_cursor, width=self.page.width)

    # Private methods for outputting document
    def _get_image(self, image_name):
        if image_name in self.imagekeys:
            index = self.imagekeys.index(image_name)
            myimage = self.images[index]
            return myimage
        else:
            return False

    def _output_pages(self):
        """ Called by the PDFLite object to prompt creating
            the page objects.

        """
        if self.orientation_changes is None:
            self._get_orientation_changes()
        else:
            # Page
            for page in self.pages:
                obj = self.session._add_object()
                self.session._out('<</Type /Page')
                self.session._out('/Parent 1 0 R')
                if page in self.orientation_changes:
                    self.session._out(
                        '/MediaBox [0 0 %.2f %.2f]' %
                        (page.width, page.height))
                self.session._out('/Resources 2 0 R')
                self.session._out('/Group <</Type /Group /S /Transparency /CS /DeviceRGB>>')
                self.session._out('/Contents %s 0 R>>' % (obj.id + 1))
                self.session._out('endobj')

                # Page content
                self.session._add_object()
                if self.session.compression is True:
                    textfilter = ' /Filter /FlateDecode '
                    page._compress()
                else:
                    textfilter = ''
                self.session._out('<<%s/Length %s >>' % (textfilter, len(page.buffer)))
                self.session._put_stream(page.buffer)
                self.session._out('endobj')

    def _set_page_numbers(self):
        if hasattr(self, 'page_numbers'):
            for page in self.pages:
                self._add_page_number(page, len(self.pages))

    def _add_page_number(self, page, number_of_pages):
        if self.page_numbers_font is not None:
            fs = 'BT /F%d %.2f Tf ET' % (self.page_numbers_font.index, self.page_numbers_font.font_size)
            self.session._out(fs, page)

        if self.page_numbers_color is not None:
            self.page_numbers_color._set_type('t')
            self.session._out(self.page_numbers_color._get_color_string(), page)

        text_string = self.page_numbers_text1 % (page.index + 1)
        if self.page_numbers_text2 is not None:
            text_string += self.page_numbers_text2 % number_of_pages

        if self.page_numbers_cursor is None:
            sw = self.font._string_width(text_string)
            y = page.page_size[1]
            y = y - self.page.margin.bottom

            if self.page_numbers == 'left':
                x = self.page.margin.left
            elif self.page_numbers == 'right':
                x = page.page_size[0] - page.margin.right - sw
            else:
                x = page.page_size[0] / 2 - int(sw / 2.0)
            cursor = PDFCursor(x, y)
        else:
            cursor = self.page_numbers_cursor

        text_string = '(%s)' % text_string
        s = 'BT %.2f %.2f Td %s Tj ET' % (cursor.x, cursor.y_prime, text_string)
        self.session._out(s, page)

    def _get_orientation_changes(self):
        """ Returns a list of the pages that have
            orientation changes.

        """
        self.orientation_changes = []
        for page in self.pages:
            if page.orientation_change is True:
                self.orientation_changes.append(page.index)
            else:
                pass
        return self.orientation_changes

    def _register_new_font(self, font):
        font._set_index(len(self.fonts) + 1)
        self.fonts.append(self.font)
        self.fontkeys.append(self.font.font_key)
        if hasattr(font, 'diffs') and font.diffs is not None:
            try:
                index_of_diff = self.diffs.index(font.diffs)
            except:
                index_of_diff = len(self.diffs) + 1
                self.diffs.append(font.diffs)
            font.diff_number = index_of_diff

    def _output_fonts(self):
        """ Called by the PDFLite object to prompt creating
            the font objects.

        """
        self.session._save_object_number()
        self._output_encoding_diffs()
        self._output_font_files()

        for font in self.fonts:
            obj = self.session._add_object()
            font._set_number(obj.id)
            font._output()

    def _output_font_files(self):
        for font in self.fonts:
            if hasattr(font, 'file'):
                font.output_file()

    def _output_encoding_diffs(self):
        if self.diffs:
            for diff in self.diffs:
                obj = self.session._add_object()
                self.session._out('<</Type /Encoding /BaseEncoding /WinAnsiEncoding /Differences [%s]>>')
                self.session._out('endobj')

    def _register_new_image(self, image):
        image._set_index(len(self.images) + 1)
        self.images.append(image)
        self.imagekeys.append(image.name)

    def _output_images(self):
        """ Creates reference images, that can be
            drawn throughout the document.

        """
        for image in self.images:
            obj = self.session._add_object()
            image._set_number(obj.id)
            image._output()
