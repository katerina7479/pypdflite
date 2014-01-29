from pdfcolor import PDFColor
from pdffont import PDFFont


class PDFCellFormat(object):
    """ Object represents formatting of table cells
        in a dictionary of key / value pairs.

    """
    def __init__(self, data, default_font):
        self.dict = {}
        self.available_keys = {'font': default_font,  # PDFFont
                               'num_format': None,  # ('percent', #decimals), ('decimal', #d), ('money' or '$', #d), ('comma', #d), ('$comma' or 'money_comma') # Tuples
                               'align': "left",  # Left, right, center
                               'valign': 'center',  # Top, center, bottom
                               'text_wrap': False,  # True  # Not implemented
                               'fill_color': None,  # PDFColor (type = f)
                               'text_color': PDFColor(),  # Functionality not confirmed.
                               'border': (0, 1),  # Style Index (type, weight)
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
                               'padding_top': 1,
                               'padding_bottom': 1,
                               'padding_left': 2,
                               'padding_right': 2
                               }

        for key, value in data.iteritems():
            self._set_keys(key, value)

        self._set_remaining()

    def __repr__(self):
        return "Cell format object, font %s" % self.dict['font']

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
