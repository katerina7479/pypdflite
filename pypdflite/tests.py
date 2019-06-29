import unittest
import math
from unittest.mock import Mock
from session import _Session
from pdfobjects.pdfarc import PDFArc
from pdfobjects.pdfcursor import PDFCursor
from pdfobjects.pdflinegraph import PDFLineGraph
from pdfobjects.pdfpage import PDFPage


class TestPDFArc(unittest.TestCase):
    def setUp(self):
        self.page = Mock(PDFPage)
        self.session = Mock(_Session)

    def test_get_angle(self):
        center = PDFCursor(300, 300)
        radius = 30
        start_angle = 45
        arc_angle = 90
        inverted = False
        arc = PDFArc(self.session, self.page, center, radius, start_angle, arc_angle, inverted)
        self.assertEqual(math.degrees(arc._start_angle), 45.0)
        self.assertEqual(math.degrees(arc._end_angle), 135.0)

        inverted = True
        arc = PDFArc(self.session, self.page, center, radius, start_angle, arc_angle, inverted)
        self.assertEqual(math.degrees(arc._start_angle), 135.0)
        self.assertEqual(math.degrees(arc._end_angle), 45.0)

        center = PDFCursor(400, 400)
        start_angle = 0
        arc_angle = 180
        arc = PDFArc(self.session, self.page, center, 40, start_angle, arc_angle, False)
        self.assertEqual(math.degrees(arc._start_angle), 0.0)
        self.assertEqual(math.degrees(arc._end_angle), 180.0)

        arc = PDFArc(self.session, self.page, center, 40, start_angle, arc_angle, True)
        self.assertEqual(math.degrees(arc._start_angle), 180.0)
        self.assertEqual(math.degrees(arc._end_angle), 0.0)

        start_angle = 15
        arc_angle = 405
        arc = PDFArc(self.session, self.page, center, 40, start_angle, arc_angle, False)
        self.assertEqual(round(math.degrees(arc._start_angle)), 15.0)
        self.assertEqual(round(math.degrees(arc._end_angle)), 60.0)

        arc = PDFArc(self.session, self.page, center, 40, start_angle, arc_angle, True)
        self.assertEqual(round(math.degrees(arc._start_angle)), 60.0)
        self.assertEqual(round(math.degrees(arc._end_angle)), 15.0)


class TestLineGraphInterpolate(unittest.TestCase):
    def test_interpolate(self):
        result = PDFLineGraph.interpolate(2.0, [(0, 0), (4, 6), (7, 8)])
        self.assertEqual(result, 3)

        result = PDFLineGraph.interpolate(50, [(0, 100), (100, 300)])
        self.assertEqual(result, 200)


if __name__ == '__main__':
    unittest.main()