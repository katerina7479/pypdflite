from pypdflite.pdflite import PDFLite


def ImageTest():

    """ Functional test for adding images.

    """

    #Create PDFLITE object, initialize with path & filename.
    writer = PDFLite("ImageTest.pdf")

    # If desired (in production code), set compression
    # writer.setCompression(True)

    # Set general information metadata
    writer.set_information(title="Image Testing")  # set optional information

    # Use get_document method to get the generated document object.
    document = writer.get_document()

    # Example for adding short and long text and whitespaces
    document.add_text("This should be before the image.")
    document.add_newline(1)

    mylogo = document.add_image("testing_colors.png")
    document.add_newline(1)

    document.add_text("This should be after")

    document.add_newline(1)
    document.add_image(mylogo)

    document.add_text("There it is without a newline")

    document.add_page()
    bgcursor = document.get_new_cursor()

    document.add_image("background.png", cursor=bgcursor)
    document.add_text("This text, ")
    document.add_text("And this text")
    document.add_newline(2)
    document.add_text("Should be on the background.")

    # Close writer
    writer.close()

if __name__ == "__main__":
    ImageTest()
