from pypdflite.pdflite import PDFLite


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

    document.set_font(family='arial', style='UB', size=12, tt=True)
    underline = document.get_font()

    document.set_font(family='arial', size=12, tt=True)
    default_font = document.get_font()
    # Example for adding short and long text and whitespaces
    mytable = document.add_table(3, 3)

    default = document.add_cell_format({'font': default_font, 'align': 'left', 'border': (0, 1)})
    justleft = document.add_cell_format({'left': (0, 1)})
    uformat = document.add_cell_format({'font': underline, 'align': 'right', 'border': (0, 1)})

    mytable.set_column_width(1, 200)
    mytable.set_row_height(2, 200)

    for r in range(1):
        for c in range(3):
            mytable.write(r, c, data[r][c], uformat)
    for r in range(1, 3):
        for c in range(3):
            mytable.write(r, c, data[r][c], default)


    document.draw_table(mytable)
    document.add_newline(4)
    document.add_text("Testing followup text")

    # Close writer
    writer.close()

if __name__ == "__main__":
    TableTest()
