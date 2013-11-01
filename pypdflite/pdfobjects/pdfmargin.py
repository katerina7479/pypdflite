

class PDFMargin(object):

    def __init__(self, left=20, top=20, right=None, bottom=None):
        self._set_left(left)
        self._set_top(top)
        self._set_right(right)
        self._set_bottom(bottom)

    def _set_left(self, left):
        self.left = left

    def _set_top(self, top):
        self.top = top

    def _set_right(self, right):
        if right is None:
            self.right = self.left
        else:
            self.right = right

    def _set_bottom(self, bottom):
        if bottom is None:
            self.bottom = self.top
        else:
            self.bottom = bottom
        self._set_trigger(2 * self.bottom)

    def _set_trigger(self, value):
        self.trigger = 2 * self.bottom
