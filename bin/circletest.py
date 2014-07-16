from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolor import PDFColor
from pypdflite.pdfobjects.pdfcursor import PDFCursor


def CircleTest():
    """
    Functional test for drawing eclipses
    """
    # Create PDFLite object
    writer = PDFLite("generated/CircleTest.pdf")

    # Set compression defaults to False
    writer.set_compression(False)

    # Set document metadata
    writer.set_information(title="Testing Circles")  # set optional information

    # Get document object
    document = writer.get_document()
    black = PDFColor()

    red = PDFColor(name='red')
    center = PDFCursor(100, 100)

    document.draw_circle(center, 10, black, red, style='F')

    green = PDFColor(name='green')
    center = PDFCursor(300, 300)
    document.draw_circle(center, 20, black, green, style='B', stroke="dotted")

    center = PDFCursor(350, 400)
    document.draw_circle(center, 30, None, None, size=2)

    # Close Document
    writer.close()


if __name__ == '__main__':
    CircleTest()