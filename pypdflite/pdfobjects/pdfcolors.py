

class PDFColors(object):
    def __init__(self, dc='0 G', fc='0 g', tc='0 g'):
        self.draw_color = dc
        self.fill_color = fc
        self.text_color = tc
        self.color_flag = 0        # indicates whether fill and text colors are different

    def set_draw_color(self, r, g=-1, b=-1):
        "Set color for all stroking operations"
        if((r == 0 and g == 0 and b == 0) or g == -1):
            self.draw_color = '%.3f G' % r/255.0
        else:
            self.draw_color = '%.3f %.3f %.3f RG' % (r/255.0, g/255.0, b/255.0)
        if(self.page.index > 0):
            self.SS._out(self.draw_color)

    def set_fill_color(self, r, g=-1, b=-1):
        "Set color for all filling operations"
        if((r == 0 and g == 0 and b == 0) or g == -1):
            self.fill_color = '%.3f g' % r/255.0
        else:
            self.fill_color = '%.3f %.3f %.3f rg' % (r/255.0, g/255.0, b/255.0)
        self.color_flag = (self.fill_color != self.text_color)

        if(self.page.index > 0):
            self.SS._out(self.fill_color)

    def set_text_color(self, r, g=-1, b=-1):
        "Set color for text"
        if((r == 0 and g == 0 and b == 0) or g == -1):
            self.text_color = '%.3f g' % (r/255.0)
        else:
            self.text_color = '%.3f %.3f %.3f rg' % (r/255.0, g/255.0, b/255.0)
        self.color_flag = (self.fill_color != self.text_color)