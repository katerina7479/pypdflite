from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolor import PDFColor


def LinesTest():

    """ Functional tests for creating lines.

    """
    # Create PDFLite object
    writer = PDFLite("generated/LinesTest.pdf")

    # Set compression defaults to False
    writer.set_compression(False)

    # Set document metadata
    writer.set_information(title="Testing Lines")  # set optional information

    # Get document object
    document = writer.get_document()

    # Test add line by (x, y, x, y)
    document.add_line(20, 40, 300, 80)

    # Add Horizontal rule under text
    document.add_text("Testing")
    document.add_newline(1)
    document.draw_horizontal_line()

    # Create color Object, apply to fill color
    lightblue = PDFColor(name='lightblue')

    # Draw styled rectangle.
    document.set_fill_color(lightblue)
    document.draw_rectangle(150, 500, 300, 600, style='B')

    # Draw Dashed Line
    document.add_line(400, 250, 300, 500, stroke="dots")

    # Close Document
    writer.close()

if __name__ == "__main__":
    LinesTest()
