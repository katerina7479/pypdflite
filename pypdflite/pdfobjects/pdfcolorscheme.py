from pdfcolor import PDFColor


class PDFColorScheme(object):

    """ ColorScheme is made up of three PDFColors,
        for the draw (stroke operations), fill, and text
        colors.

        The colors can be changed after the fact,
        but it may be more clear to create multiple
        PDFColorSchemes for different situations.

    """

    def __init__(self, draw_color=None, fill_color=None, text_color=None):
        print "Draw Color", draw_color
        print "Fill Color", fill_color
        print "Text Color", text_color

        self.set_draw_color(draw_color)
        self.set_fill_color(fill_color)
        self.set_text_color(text_color)

    def __repr__(self):
        return 'DC: %s, FC: %s, TC: %s' % (self.draw_color, self.fill_color, self.text_color)

    def set_draw_color(self, draw_color):
        if draw_color is None:
            draw_color = PDFColor("d")
        elif isinstance(draw_color, PDFColor) and draw_color.color_type is "d":
            pass
        else:
            draw_color.set_color_type("d")
        self.draw_color = draw_color

    def set_fill_color(self, fill_color):
        if fill_color is None:
            fill_color = PDFColor("f")
        elif isinstance(fill_color, PDFColor) and fill_color.color_type is "f":
            pass
        else:
            fill_color.set_color_type("f")
        self.fill_color = fill_color
        self._set_color_flag()

    def set_text_color(self, text_color):
        if text_color is None:
            text_color = PDFColor("t")
        elif isinstance(text_color, PDFColor) and text_color.color_type is "t":
            pass
        else:
            text_color.set_color_type("t")
        self.text_color = text_color
        self._set_color_flag()

    def _set_color_flag(self):
        if hasattr(self, "text_color") and hasattr(self, "fill_color"):
            if self.text_color.is_equal(self.fill_color):
                self.color_flag = False
            else:
                self.color_flag = True
        else:
            pass

    def _get_color_flag(self):
        return self.color_flag

    def _get_draw_color_string(self):
        return self.draw_color._get_color_string()

    def _get_fill_color_string(self):
        return self.fill_color._get_color_string()

    def _get_text_color_string(self):
        return self.text_color._get_color_string()
