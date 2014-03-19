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
from bin.transformtest import TransformTest

def main():
    print "Running TextTest"
    TextTest()
    print "Running TrueTypeTest"
    TrueTypeTest()
    print "Running List Test"
    ListTest()
    print "Running Underline Test"
    UnderlineTest()
    print "Running LandscapeTest"
    LandscapeTest()
    print "Running LinesTest"
    LinesTest()
    print "Running TableTest"
    TableTest()
    print "Running PNGTest"
    PNGTest()
    print "Running JPGTest"
    JPGTest()
    print "Running PageNumberTest"
    PageNumberTest()
    print "Running PNGSizeTest"
    ImageSizeTest()
    print "Running EllipseTest"
    EllipseTest()
    print "Running TransormTest"
    TransformTest()

if __name__ == '__main__':
    main()
