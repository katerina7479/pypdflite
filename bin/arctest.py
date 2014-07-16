from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolor import PDFColor
from pypdflite.pdfobjects.pdfcursor import PDFCursor


def ArcTest():
    """
    Functional test for drawing eclipses
    """
    # Create PDFLite object
    writer = PDFLite("generated/ArcTest.pdf")

    # Set compression defaults to False
    writer.set_compression(False)

    # Set document metadata
    writer.set_information(title="Testing Arcs")  # set optional information

    # Get document object
    document = writer.get_document()
    black = PDFColor()

    center = PDFCursor(300, 300)
    radius = 50
    document.draw_circle(center, radius, black)


    red = PDFColor(name='red')
    starting_angle = 15
    arc_angle = 135

    document.draw_arc(center, radius, starting_angle, arc_angle, inverted=False, border_color=red, style='F')


    center = PDFCursor(300, 400)

    document.draw_arc(center, radius, starting_angle, arc_angle, inverted=True, border_color=red)
    # Close Document
    writer.close()


if __name__ == '__main__':
    ArcTest()