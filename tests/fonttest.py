import unittest
from pypdflite.pdfobjects.pdffont import PDFFont


class FontTest(unittest.TestCase):
    def setUp(self):
        self.__class__.testclass = PDFFont()

    def testCore(self):
        result = self.testclass.core_fonts
        self.assertEqual(result['timesB'], 'Times-Bold')

    def testCoreCheck(self):
        result = self.testclass._inCoreFonts('helvetica')
        self.assertEqual(result, True)
        result = self.testclass._inCoreFonts('Helvetica')
        self.assertEqual(result, True)
        result = self.testclass._inCoreFonts('Arial')
        self.assertEqual(result, False)

    def testDefaultFontSet(self):
        self.testclass.setFont()
        result = self.testclass
        self.assertEqual(result.font_family, "helvetica")
        self.assertEqual(result.fontsize, 20)
        self.assertEqual(result.style, None)
        self.assertEqual(result.fontkey, "helvetica")
        self.assertEqual(result.name, "Helvetica")

    def testNewFontSet(self):
        self.testclass.setFont("Times", "IBU", 20)
        result = self.testclass
        self.assertEqual(result.font_family, "times")
        self.assertEqual(result.fontsize, 20)
        self.assertEqual(result.style, "BI")
        self.assertEqual(result.underline, True)
        self.assertEqual(result.fontkey, "timesBI")
        self.assertEqual(result.name, "Times-BoldItalic")

    def teststringWidth(self):
        result = self.testclass.stringWidth("Testing")
        self.assertEqual(result, 65.58)
