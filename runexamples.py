import os

from bin.texttest import TextTest
from bin.truetypetest import TrueTypeTest
from bin.listtest import ListTest
from bin.underlinetest import UnderlineTest
from bin.landscapetest import LandscapeTest
from bin.linetest import LinesTest
from bin.tabletest import TableTest
from bin.pngtest import PNGTest
from bin.jpgtest import JPGTest
from bin.pagenumbertest import PageNumberTest
from bin.pngsizetest import ImageSizeTest
from bin.ellipsetest import EllipseTest
from bin.circletest import CircleTest
from bin.transformtest import TransformTest
from bin.htmltest import HtmlTest
from bin.htmltest2 import HtmlTest2
from bin.justifytest import JustifyTest
from bin.pdfmargintest import MarginTest
from bin.arctest import ArcTest
from bin.linegraphtest import LineGraphTest
from bin.xyscatterplot import XYScatterPlotTest
from bin.piecharttest import PieChartTest
from bin.barcharttest import BarChartTest
from bin.multibartest import MultiBarChartTest
from bin.graphbackgrounds import GraphBackgroundTest

TEST_DIR = os.path.abspath('bin')

def main():
    print ("Running TextTest")
    TextTest(TEST_DIR)
    print ("Running TrueTypeTest")
    TrueTypeTest(TEST_DIR)
    print ("Running List Test")
    ListTest(TEST_DIR)
    print ("Running Margin Test")
    MarginTest(TEST_DIR)
    print ("Running Underline Test")
    UnderlineTest(TEST_DIR)
    print ("Running LandscapeTest")
    LandscapeTest(TEST_DIR)
    print ("Running LinesTest")
    LinesTest(TEST_DIR)
    print ("Running TableTest")
    TableTest(TEST_DIR)
    print ("Running PNGTest")
    PNGTest(TEST_DIR)
    print ("Running JPGTest")
    JPGTest(TEST_DIR)
    print ("Running PageNumberTest")
    PageNumberTest(TEST_DIR)
    print ("Running PNGSizeTest")
    ImageSizeTest(TEST_DIR)
    print ("Running EllipseTest")
    EllipseTest(TEST_DIR)
    print ("Running CircleTest")
    CircleTest(TEST_DIR)
    print ("Running Arctest")
    ArcTest(TEST_DIR)
    print ("Running TransformTest")
    TransformTest(TEST_DIR)
    print ("Running HTMLTest")
    HtmlTest(TEST_DIR)
    print ("Running HTMLTest2")
    HtmlTest2(TEST_DIR)
    print ("Running Justify Test")
    JustifyTest(TEST_DIR)
    print ("Running LineGraph Test")
    LineGraphTest(TEST_DIR)
    print ("Running XYScatter Test")
    XYScatterPlotTest(TEST_DIR)
    print ("Running PieChart Test")
    PieChartTest(TEST_DIR)
    print ("Running BarChart Test")
    BarChartTest(TEST_DIR)
    print ("Running MultiBarChart Test")
    MultiBarChartTest(TEST_DIR)
    print ("Running GraphBackgrounds Test")
    GraphBackgroundTest(TEST_DIR)


if __name__ == '__main__':
    
    generated_dir = os.path.join(TEST_DIR, 'tests')
    if not os.path.isdir(generated_dir):
        print ("Creating directory at ".format(generated_dir))
        os.mkdir(generated_dir)
    main()
