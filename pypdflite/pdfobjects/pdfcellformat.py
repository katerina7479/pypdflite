from pdfcolor import PDFColor


class PDFCellFormat(object):
    """ Object represents formatting of table cells
        in a dictionary of key / value pairs.

    """
    def __init__(self, data=None, font=None, **kwargs):
        self.dict = {}
        self.available_keys = {'font': None,  # PDFFont
                               'num_format': None,  # 'float', 'int', 'percent', 'decimal_#', 'money' # Not implemented
                               'align': "left",  # Left, right, center
                               'valign': 'center',  # Top, center, bottom
                               'text_wrap': False,  # True  # Not implemented
                               'fill_color': None,  # PDFColor (type = f)
                               'text_color': PDFColor(),  # Functionality not confirmed.
                               'border': (None, None),  # Style Index (type, weight)
                               'bottom': (None, None),  # index
                               'top': (None, None),  # index tuple
                               'left': (None, None),  # index
                               'right': (None, None),  # index
                               'border_color': None,  # PDFColor # Functionality not confirmed.
                               'bottom_color': None,  # PDFColor
                               'top_color': None,  # PDFColor
                               'left_color': None,  # PDFColor
                               'right_color': None,  # PDFColor
                               'padding': False,  # Integer, applies to all text_padding
                               'padding_top': 5,
                               'padding_bottom': 5,
                               'padding_left': 10,
                               'padding_right': 10
                               }
        if font is not None:
            self.dict['font'] = font
        if data is not None:
            for key, value in data.iteritems():
                self._set_keys(key, value)
        else:
            for key, value in kwargs:
                self._set_keys(key, value)

        self._set_remaining()

    def __repr__(self):
        return "Format object, font %s" % self.dict['font']

    def __getitem__(self, key):
        return self.dict[key]

    def _set_keys(self, key, value):
        if key in self.available_keys:
            self.dict[key] = value
        else:
            raise Exception("%s not valid pdfcell format key" % key)

    def _set_remaining(self):
        for key in self.available_keys:
            if key in self.dict:
                pass
            else:
                self.dict[key] = self.available_keys[key]
