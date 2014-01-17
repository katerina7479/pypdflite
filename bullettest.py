from pypdflite.pdflite import PDFLite


def BulletTest():

    """ Functional test for text, paragraph, and page
    splitting.

    """

    #Create PDFLITE object, initialize with path & filename.
    writer = PDFLite("BulletTest.pdf")

    # If desired (in production code), set compression
    # writer.setCompression(True)

    # Set general information metadata
    writer.set_information(title="Testing Text")  # set optional information

    # Use get_document method to get the generated document object.
    document = writer.get_document()

    # Example for adding short and long text and whitespaces
    document.add_list("Testing", "Testing")
    document.add_newline(4)


    # Close writer
    writer.close()

if __name__ == "__main__":
    BulletTest()
