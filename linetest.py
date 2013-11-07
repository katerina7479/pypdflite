from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolorscheme import PDFColorScheme
from pypdflite.pdfobjects.pdfcolor import PDFColor


def main():

    """ Functional tests for creating lines.

    """
    # Create PDFLite object
    writer = PDFLite("LinesTest.pdf")

    # Set compression defaults to False
    # writer.setCompression(True)

    # Set document metadata
    writer.set_information(title="Testing Lines")  # set optional information

    # Get documnet object
    document = writer.get_document()

    # Test add line by (x, y, x, y)
    document.add_line(20, 40, 300, 80)

    # Add Horizontal rule under text
    document.add_text("Testing")
    document.add_newline(1)
    document.draw_horizonal_line()

    # Create color Object, apply to fill color
    lightblue = PDFColor(name='lightblue')
    new_scheme = PDFColorScheme(fill_color=lightblue)

    # Draw styled rectangle.
    document.set_color_scheme(new_scheme)
    document.draw_rectangle(150, 500, 300, 600, style='B')

    # Draw Dashed Line
    document.add_line(300, 250, 300, 500, style="dashed")

    # Close Document
    writer.close()

if __name__ == "__main__":
    main()
