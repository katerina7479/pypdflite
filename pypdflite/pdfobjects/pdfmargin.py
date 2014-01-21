

class PDFMargin(object):

    def __init__(self, left=20, top=None, right=None, bottom=None):
        self.set(left, top, right, bottom)

    def set(self, left, top=None, right=None, bottom=None):
        self.left = left
        if top is None:
            top = left
        if right is None:
            right = left
        if bottom is None:
            bottom = top
        self.top = top
        self.right = right
        self.bottom = bottom
