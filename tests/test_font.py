import unittest
from pypdflite.pdfobjects.pdffont import PDFFont


class FontTest(unittest.TestCase):
    def setUp(self):
        self.testclass = PDFFont()

    def test_core(self):
        result = self.testclass.core_fonts
        self.assertEqual(result['timesB'], 'Times-Bold')

    def test_core_check(self):
        result = self.testclass._inCoreFonts('helvetica')
        self.assertEqual(result, True)
        result = self.testclass._inCoreFonts('Helvetica')
        self.assertEqual(result, True)
        result = self.testclass._inCoreFonts('Arial')
        self.assertEqual(result, False)

    def test_default_font_set(self):
        self.testclass.setFont()
        result = self.testclass
        self.assertEqual(result.font_family, "helvetica")
        self.assertEqual(result.fontsize, 20)
        self.assertEqual(result.style, None)
        self.assertEqual(result.fontkey, "helvetica")
        self.assertEqual(result.name, "Helvetica")

    def test_new_font_set(self):
        self.testclass.setFont("Times", "IBU", 20)
        result = self.testclass
        self.assertEqual(result.font_family, "times")
        self.assertEqual(result.fontsize, 20)
        self.assertEqual(result.style, "BI")
        self.assertEqual(result.underline, True)
        self.assertEqual(result.fontkey, "timesBI")
        self.assertEqual(result.name, "Times-BoldItalic")

    def test_string_width(self):
        result = self.testclass.stringWidth("Testing")
        self.assertEqual(result, 65.58)
