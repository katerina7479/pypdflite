from texttest import TextTest
from truetypetest import TrueTypeTest
from underlinetest import UnderlineTest
from landscapetest import LandscapeTest
from linetest import LinesTest
from tabletest import TableTest
from imagetest import ImageTest



def main():
    print "Running TextTest"
    TextTest()
    print "Running TrueTypeTest"
    TrueTypeTest()
    print "Running Underline Test"
    UnderlineTest()
    print "Running LandscapeTest"
    LandscapeTest()
    print "Running LinesTest"
    LinesTest()
    print "Running TableTest"
    TableTest()
    print "Running ImageTest"
    ImageTest()


if __name__ == '__main__':
    main()
