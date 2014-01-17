from pypdflite.pdflite import PDFLite


def GIFTest():

    """ Functional test for adding images.

    """

    #Create PDFLITE object, initialize with path & filename.
    writer = PDFLite("GIFTest.pdf")

    # If desired (in production code), set compression
    # writer.setCompression(True)

    # Set general information metadata
    writer.set_information(title="Image Testing")  # set optional information

    # Use get_document method to get the generated document object.
    document = writer.get_document()

    # Example for adding short and long text and whitespaces
    document.add_text("This should be before the image.")
    document.add_newline(1)

    example = document.add_image("example.gif")
    document.add_newline(1)

    document.add_text("This should be after")

    document.add_newline(1)
    document.add_image(example)

    document.add_text("There it is without a newline")

    # Close writer
    writer.close()

if __name__ == "__main__":
    GIFTest()
