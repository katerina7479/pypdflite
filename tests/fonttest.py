import unittest
from pypdflite.pdfobjects.pdffont import PDFFont


class FontTest(unittest.TestCase):

    def setUp(self):
        self.__class__.testclass = PDFFont()

    def test_core(self):
        result = self.testclass.core_fonts
        self.assertEqual(result['timesB'], 'Times-Bold')

    def test_core_check(self):
        result = self.testclass._in_core_fonts('helvetica')
        self.assertEqual(result, True)
        result = self.testclass._in_core_fonts('Helvetica')
        self.assertEqual(result, True)
        result = self.testclass._in_core_fonts('Arial')
        self.assertEqual(result, False)

    def test_default_font_set(self):
        self.testclass.set_font()
        result = self.testclass
        self.assertEqual(result.font_family, "helvetica")
        self.assertEqual(result.font_size, 20)
        self.assertEqual(result.style, None)
        self.assertEqual(result.font_key, "helvetica")
        self.assertEqual(result.name, "Helvetica")

    def test_set_new_font(self):
        self.testclass.set_font("Times", "IBU", 20)
        result = self.testclass
        self.assertEqual(result.font_family, "times")
        self.assertEqual(result.font_size, 20)
        self.assertEqual(result.style, "BI")
        self.assertEqual(result.underline, True)
        self.assertEqual(result.font_key, "timesBI")
        self.assertEqual(result.name, "Times-BoldItalic")

    def test_string_width(self):
        result = self.testclass.string_width("Testing")
        self.assertEqual(result, 65.58)
