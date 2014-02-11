from pypdflite.pdflite import PDFLite


def JPGTest():

    """ Functional test for adding images.

    """

    #Create PDFLITE object, initialize with path & filename.
    writer = PDFLite("generated/JPGTest.pdf")

    # If desired (in production code), set compression
    # writer.setCompression(True)

    # Set general information metadata
    writer.set_information(title="JPG Testing")  # set optional information

    # Use get_document method to get the generated document object.
    document = writer.get_document()

    # Example for adding short and long text and whitespaces
    document.add_text("This should be before the image.")
    document.add_newline(1)

    mylogo = document.add_image("bin/example.jpg")
    document.draw_image(mylogo)
    document.add_newline(1)

    document.add_text("This should be after")

    document.add_newline(1)
    document.draw_image(mylogo)

    document.add_text("There it is without a newline")

    # Close writer
    writer.close()

if __name__ == "__main__":
    JPGTest()
