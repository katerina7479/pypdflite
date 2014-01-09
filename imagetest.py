from pypdflite.pdflite import PDFLite


def main():

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
    applelogo = document.add_image("testing_colors.png")

    # Close writer
    writer.close()

if __name__ == "__main__":
    main()
