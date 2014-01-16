from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolor import PDFColor


def TableTest():

    """ Functional test for text, paragraph, and page
    splitting.

    """

    data = [["Heading1", "Heading2", "Heading3"],
            ["Cell a2", "Cell b2", "Cell c2"],
            ["Cell a3", "Cell b3", "Cell c3"]]

    #Create PDFLITE object, initialize with path & filename.
    writer = PDFLite("TableTest.pdf")

    # If desired (in production code), set compression
    # writer.setCompression(True)

    # Set general information metadata
    writer.set_information(title="Testing Table")  # set optional information

    # Use get_document method to get the generated document object.
    document = writer.get_document()

    document.set_cursor(100, 100)

    document.set_font(family='arial', style='UB', size=12)
    underline = document.get_font()

    document.set_font(family='arial', size=12)
    default_font = document.get_font()
    # Example for adding short and long text and whitespaces
    mytable = document.add_table(3, 3)
    green = PDFColor(name='green')

    default = document.add_cell_format({'font': default_font, 'align': 'left', 'border': (0, 1)})
    justleft = document.add_cell_format({'left': (0, 1)})
    header_format = document.add_cell_format({'font': underline, 'align': 'right', 'border': (0, 1)})
    green_format = document.add_cell_format({'font': default_font, 'border': (0, 1), 'fill_color': green})

    #mytable.set_column_width(1, 200)
    #mytable.set_row_height(2, 200)

    mytable.write_row(0, 0, data[0], header_format)
    mytable.write_row(1, 0, data[1], justleft)
    mytable.write_row(2, 0, data[2], green_format)


    document.draw_table(mytable)
    document.add_newline(4)
    document.add_text("Testing followup text")

    # Close writer
    writer.close()

if __name__ == "__main__":
    TableTest()
