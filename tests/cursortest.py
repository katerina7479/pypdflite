import unittest
from pdflite.pdfcursor import PDFCursor


class CursorTest(unittest.TestCase):
    def setUp(self):
        self.__class__.testclass = PDFCursor()

    def testBase(self):
        x = self.testclass.x
        y = self.testclass.y
        self.assertEqual((x, y), (1, 790))

    def testBounds(self):
        xmax = self.testclass.xmax
        self.assertEqual(xmax, 612)
        try:
            self.testclass.x = 613
        except ValueError:
            pass
        else:
            self.fail("Value Error Not Thrown")
