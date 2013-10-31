import unittest
from pypdflite.pdfobjects.pdfpage import PDFPage


class PageTest(unittest.TestCase):
    def setUp(self):
        self.__class__.testclass = PDFPage()

    def test_core(self):
        result = self.testclass.page_size[0]
        self.assertEqual(result, 612)
        result = self.testclass.page_size[1]
        self.assertEqual(result, 792)
