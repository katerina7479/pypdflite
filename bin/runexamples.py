from texttest import TextTest
from truetypetest import TrueTypeTest
from listtest import ListTest
from underlinetest import UnderlineTest
from landscapetest import LandscapeTest
from linetest import LinesTest
from tabletest import TableTest
from pngtest import PNGTest
from jpgtest import JPGTest


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


if __name__ == '__main__':
    main()
