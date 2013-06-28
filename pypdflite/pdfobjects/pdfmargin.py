

class PDFMargin(object):
    def __init__(self, left=20, top=20, right=None, bottom=None):
        self._setLeft(left)
        self._setTop(top)
        self._setRight(right)
        self._setBottom(bottom)

    def _setLeft(self, left):
        self.l = left

    def _setTop(self, top):
        self.t = top

    def _setRight(self, right):
        if right is None:
            self.r = self.l
        else:
            self.r = right

    def _setBottom(self, bottom):
        if bottom is None:
            self.b = self.t
        else:
            self.b = bottom
        self.setTrigger(2 * self.b)

    def setTrigger(self, value):
        self.trigger = 2 * self.b
