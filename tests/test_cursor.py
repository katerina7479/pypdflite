import unittest
from pypdflite.pdfobjects.pdfcursor import PDFCursor


class CursorTest(unittest.TestCase):
    def setUp(self):
        self.testclass = PDFCursor()

    def test_base(self):
        x = self.testclass.x
        y = self.testclass.y
        self.assertEqual((x, y), (20, 720))

    def test_bounds(self):
        xmax = self.testclass.xmax
        self.assertEqual(xmax, 612)
        try:
            self.testclass.x = 613
        except ValueError:
            pass
        else:
            self.fail("Value Error Not Thrown")
