from pypdflite.pdflite import PDFLite


def TableTest():

    """ Functional test for text, paragraph, and page
    splitting.

    """

    #Create PDFLITE object, initialize with path & filename.
    writer = PDFLite("TableTest.pdf")

    # If desired (in production code), set compression
    # writer.setCompression(True)

    # Set general information metadata
    writer.set_information(title="Testing Table")  # set optional information

    # Use get_document method to get the generated document object.
    document = writer.get_document()

    document.set_cursor(100, 100)
    # Example for adding short and long text and whitespaces
    mytable = document.add_table(3, 3)

    format = document.add_cell_format({'align': 'right', 'border': (0, 1)})
    justleft = document.add_cell_format({'left': (0, 1)})

    mytable.set_column_width(1, 200)
    mytable.set_row_height(2, 200)

    for row in range(2):
        for column in range(3):
            mytable.write(row, column, 'cell %s, %s' % (row, column), format)
    for column in range(3):
            mytable.write(2, column, 'look', justleft)

    document.draw_table(mytable)
    document.add_newline(4)
    document.add_text("Testing followup text")

    # Close writer
    writer.close()

if __name__ == "__main__":
    TableTest()
