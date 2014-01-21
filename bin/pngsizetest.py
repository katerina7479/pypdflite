from pypdflite.pdflite import PDFLite


def ImageSizeTest():
    """ Functional test for adding images.

    """

    #Create PDFLITE object, initialize with path & filename.
    writer = PDFLite("ImageSizeTest.pdf")

    # If desired (in production code), set compression
    # writer.setCompression(True)

    # Set general information metadata
    writer.set_information(title="PNG Size Testing")  # set optional information

    # Use get_document method to get the generated document object.
    document = writer.get_document()

    # Example for adding short and long text and whitespaces
    document.add_text("This is the image")
    document.add_newline(1)

    mylogo = document.add_image("elephant.png")
    document.draw_image(mylogo)
    document.add_newline(1)

    document.add_text("This is the image smaller")
    document.draw_image(mylogo, width=100)
    document.add_newline(1)

    document.add_page()
    document.add_text("This is the image larger")
    document.draw_image(mylogo, width=300)
    document.add_newline(3)


    # Close writer
    writer.close()

if __name__ == "__main__":
    ImageSizeTest()
