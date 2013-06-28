import unittest
from pdflite.pdfpage import PDFPage
from pdflite.session import Session


class PageTest(unittest.TestCase):
    def setUp(self):
        self.SS = Session(self)
        self.__class__.testclass = PDFPage(self.SS)

    def testCore(self):
        result = self.testclass.pagesize[0]
        self.assertEqual(result, 612)
        result = self.testclass.pagesize[1]
        self.assertEqual(result, 792)
