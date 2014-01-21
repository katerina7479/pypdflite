from pypdflite.pdflite import PDFLite


def ListTest():

    """ Functional test for text, paragraph, and page
    splitting.

    """

    #Create PDFLITE object, initialize with path & filename.
    writer = PDFLite("generated/ListTest.pdf")

    # If desired (in production code), set compression
    # writer.setCompression(True)

    # Set general information metadata
    writer.set_information(title="Testing Lists")  # set optional information

    # Use get_document method to get the generated document object.
    document = writer.get_document()



    # Make a header
    document.set_font(family='helvetica', style='B', size=24)
    document.add_text("This is my list!")
    document.add_newline(2)

    # Make a list
    document.set_font(family='helvetica', size=16)
    document.add_list("Testing1", "Testing2", "Testing3")
    document.add_newline(4)

    document.set_font(family='arial', size=18)
    document.start_block_indent()
    document.add_list("Arial didn't", "have native", "bullets", force=True)
    document.end_block_indent()

    document.add_newline(2)
    document.add_text("And this is my followup text")

    # Close writer
    writer.close()

if __name__ == "__main__":
    ListTest()
