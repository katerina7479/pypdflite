from pdftext import PDFText
from pdfline import PDFLine
from pdfcellformat import PDFCellFormat
from pdfrectangle import PDFRectangle
from pdfcolor import PDFColor


class PDFCell(object):
    def __init__(self, table, row_index, column_index, text_cursor, border_cursor):
        self.table = table
        self.font = self.table.font
        self.row_index = row_index
        self.column_index = column_index

        self.text_cursor = text_cursor
        self.border_cursor = border_cursor

        self.height = 0
        self.width = 0
        self.max_width = 0

        self.line_space = 2

    def __repr__(self):
        return '(%s, %s)' % (self.row_index, self.column_index)

    # Text
    def _set_text(self, text):
        self.text = text
        if hasattr(self, 'format'):
            numf = self.format['num_format']
            if numf is not None:
                precision = numf[1]
                numf = numf[0]
                if precision <= 0:
                    self.text = str(int(self.text))
                else:
                    self.text = '%0.*f' % (precision, float(self.text))
                if 'euro' in numf:
                    self.text = self.text.replace('.', ',')
                    self.text = '%s%s' % (chr(128), self.text)
                if any(s in numf for s in ['comma', ',']):
                    self.text = str('{:,}'.format(int(self.text)))
                if any(s in numf for s in ['percent', '%']):
                    self.text = '%s %' % (self.text)
                if any(s in numf for s in ['$', 'money', 'dollar']):
                    self.text = '$%s' % (self.text)

    def _draw_text(self):
        if self.text == '' or self.text is None:
            self.text_cursor.x_plus(self.max_width)
        elif hasattr(self, 'text_list'):
            self.text_cursor.y_plus(-self.padding_bottom - ((len(self.text_list) - 1) * (self.line_size + self.line_space)) - self.diff_bottom)
            i = 0
            for item in self.text_list:
                self.text_cursor.x_plus(self.padding_left + self.width_diff_l[i])
                self.text_object = PDFText(self.table.session, self.table.page, item, self.font, self.text_color, self.text_cursor)
                self.text_cursor.x_plus(-self.font._string_width(item) - self.width_diff_l[i])
                self.text_cursor.y_plus(self.line_space + self.line_size)
                i += 1
            self.text_cursor.x_plus(self.font._string_width(self.text_list[-1]) + self.padding_right + self.width_diff_right + self.width_diff_l[-1])
            self.text_cursor.y_plus(self.padding_bottom + self.diff_bottom - self.line_space - self.line_size)
        else:
            self.text_cursor.y_plus(-(self.padding_bottom + self.diff_bottom))
            self.text_cursor.x_plus(self.padding_left + self.width_diff_left)
            self.text_object = PDFText(self.table.session, self.table.page, self.text, self.font, self.text_color, self.text_cursor)
            self.text_cursor.x_plus(self.padding_right + self.width_diff_right)
            self.text_cursor.y_plus(self.padding_bottom + self.diff_bottom)

    def _set_text_padding(self):
        if self.format['padding'] is not False:
            self.padding_top = self.padding_right = self.padding_left = self.padding_bottom = self.format['padding']
        else:
            self.padding_top = self.format['padding_top']
            self.padding_right = self.format['padding_right']
            self.padding_left = self.format['padding_left']
            self.padding_bottom = self.format['padding_bottom']

        self.width = (self.text_width +
                      self.padding_right + self.padding_left)

        self.height = (self.line_size + self.padding_top +
                       self.padding_bottom)

    # Format
    def _set_format(self, format):
        self.format = format
        self.font = self.format['font']
        self.text_wrap = self.format['text_wrap']
        self.text_color = self.format['text_color']
        if self.text != '' and self.text is not None:
            self.text_width = self.font._string_width(self.text)
            self._set_text(self.text)
        else:
            self.text_width = 0
        if self.font is not None:
            self.line_size = self.font.line_size
        else:
            self.line_size = 0
        self._set_text_padding()

    # Borders
    def _get_points(self):
        self.point_nw = self.border_cursor.copy()
        self.point_sw = self.border_cursor.copy()
        self.point_se = self.border_cursor.copy()
        self.point_ne = self.border_cursor.copy()

        # cursor start is NW point
        self.point_sw.y_plus(self.max_height)
        self.point_ne.x_plus(self.max_width)

        self.point_se.x_plus(self.max_width)
        self.point_se.y_plus(self.max_height)

        self.border_cursor = self.point_ne

        #print "Points, sw, se, nw, ne", self.point_sw, self.point_se, self.point_nw, self.point_ne

    def _get_border_formats(self):
        self.style = {}
        self.size = {}
        if self.format['border'][0] is not None:
            style, size = self.format['border']
            self.style['left'] = self.style['right'] = self.style['top'] = self.style['bottom'] = style
            self.size['left'] = self.size['right'] = self.size['top'] = self.size['bottom'] = size
        else:
            self.style['right'], self.size['right'] = self.format['right']
            self.style['left'], self.size['left'] = self.format['left']
            self.style['top'], self.size['top'] = self.format['top']
            self.style['bottom'], self.size['bottom'] = self.format['bottom']

    def _set_borders(self):
        self._get_points()
        self._get_border_formats()
        if self.style['bottom'] is not None:
            self.bottom_line = PDFLine(self.table.session, self.table.page,
                                       self.point_sw, self.point_se, self.format['bottom_color'],
                                       self.style['bottom'], self.size['bottom'])
        if self.style['right'] is not None:
            self.right_line = PDFLine(self.table.session, self.table.page,
                                      self.point_se, self.point_ne, self.format['right_color'],
                                      self.style['right'], self.size['right'])
        if self.style['left'] is not None:
            self.left_line = PDFLine(self.table.session, self.table.page,
                                     self.point_sw, self.point_nw, self.format['left_color'],
                                     self.style['left'], self.size['left'])
        if self.style['top'] is not None:
            self.top_line = PDFLine(self.table.session, self.table.page,
                                    self.point_ne, self.point_nw, self.format['top_color'],
                                    self.style['top'], self.size['top'])

    def _draw_borders(self):
        if self.style['bottom'] is not None:
            self.bottom_line._draw()
        if self.style['right'] is not None:
            self.right_line._draw()
        if self.style['left'] is not None:
            self.left_line._draw()
        if self.style['top'] is not None:
            self.top_line._draw()

    # Fill
    def _draw_fill(self):
        if self.format['fill_color'] is not None:
            if isinstance(self.format['fill_color'], PDFColor):
                rect = PDFRectangle(self.table.session, self.table.page,
                                    self.point_nw, self.point_se, None,
                                    self.format['fill_color'], 'F', 1)
                rect._draw()
            else:
                raise Exception("Color %s is not a PDFColor" % self.format['fill_color'])

    # Finishing
    def _compile(self):
        if hasattr(self, 'format'):
            if self.text_wrap is not False:
                self.text_wrap = self.format['text_wrap']
        else:
            self.text = ''
            self.text_width = 1
            self.line_size = 1
            self.format = PDFCellFormat()
            self.text_wrap = False
            self._set_text_padding()

    def _finish(self):
        if self.text_wrap is True and self.width > self.max_width:
            self.text_list = self.text.split('\n')
            self.height = len(self.text_list) * (self.line_size + self.padding_bottom + self.padding_top) + self.diff_bottom + self.diff_top
            for item in self.text_list:
                w = self.font._string_width(item)
                self.width = 0
                if w > self.width:
                    self.width = w
            self.text_wrap = False
            self.table._compile()

    def _advance_initial(self):
        self.text_cursor.y_plus(self.max_height - self.padding_bottom)

    def _set_max_width(self, value):
        self.max_width = value
        self.width = self.font._string_width(self.text) + self.padding_right + self.padding_left
        self._set_side_diffs()

    def _set_side_diffs(self):
        if hasattr(self, 'text_list'):
            self.width_diff_l = []
            for item in self.text_list:
                textwidth = self.font._string_width(item)
                width_diff = self.max_width - self.padding_right - self.padding_left - textwidth
                if self.format['align'] == 'left':
                    self.width_diff_l.append(0)
                    self.width_diff_right = width_diff
                elif self.format['align'] == 'right':
                    self.width_diff_l.append(width_diff)
                    self.width_diff_right = 0
                else:
                    self.width_diff_l.append(int(width_diff / 2.0))
                    self.width_diff_right = width_diff - int(width_diff / 2.0)
        else:
            width_diff = self.max_width - self.width
            if self.format['align'] == 'left':
                self.width_diff_left = 0
                self.width_diff_right = width_diff
            elif self.format['align'] == 'right':
                self.width_diff_right = 0
                self.width_diff_left = width_diff
            else:
                self.width_diff_left = int(width_diff / 2.0)
                self.width_diff_right = width_diff - self.width_diff_left

    def _set_max_height(self, value):
        self.max_height = value
        self._set_vertical_diffs()

    def _set_vertical_diffs(self):
        if hasattr(self, 'text_list'):
            diff = self.max_height - (len(self.text_list) * (self.line_size + self.line_space)) + self.line_space - self.padding_bottom - self.padding_top
        else:
            diff = self.max_height - self.height

        if self.format['valign'] == 'bottom':
            self.diff_bottom = 0
            self.diff_top = diff
        elif self.format['valign'] == 'top':
            self.diff_top = 0
            self.diff_bottom = diff
        else:
            self.diff_bottom = int(diff / 2.0)
            self.diff_top = diff - self.diff_bottom
