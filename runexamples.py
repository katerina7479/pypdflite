from texttest import TextTest
from landscapetest import LandscapeTest
from linetest import LinesTest
from tabletest import TableTest
from imagetest import ImageTest
from truetypetest import TrueTypeTest


def main():
    print "Running TextTest"
    TextTest()
    print "Running LandscapeTest"
    LandscapeTest()
    print "Running LinesTest"
    LinesTest()
    print "Running TableTest"
    TableTest()
    print "Running ImageTest"
    ImageTest()
    print "Running TrueTypeTest"
    TrueTypeTest()


if __name__ == '__main__':
    main()
