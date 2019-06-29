import os
from pypdflite.pdflite import PDFLite


def PNGTest(test_dir):

    """ Functional test for adding images.

    """
    #Create PDFLITE object, initialize with path & filename.
    writer = PDFLite(os.path.join(test_dir, "tests/PNGTest.pdf"))

    # If desired (in production code), set compression
    # writer.setCompression(True)

    # Set general information metadata
    writer.set_information(title="PNG Testing")  # set optional information

    # Use get_document method to get the generated document object.
    document = writer.get_document()

    # Example for adding short and long text and whitespaces
    document.add_text("This should be before the image.")
    document.add_newline(1)

    mylogo = document.add_image(os.path.join(test_dir, "example.png"))
    document.draw_image(mylogo)
    document.add_newline(1)

    document.add_text("This should be after")

    document.add_newline(1)
    document.draw_image(mylogo)

    document.add_text("There it is without a newline")

    document.add_newline(3)
    apple = document.add_image(os.path.join(test_dir, 'apple_logo.png'))
    document.draw_image(apple)

    document.add_page()

    document.set_background_image(os.path.join(test_dir, "example.png"))

    document.add_text("This text, ")
    document.add_text("And this text")
    document.add_newline(2)
    document.add_text("Should be on the background.")

    # Close writer
    writer.close()

if __name__ == "__main__":
    PNGTest()
