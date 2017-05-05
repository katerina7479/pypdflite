import os
from pypdflite.pdflite import PDFLite


def JustifyTest(test_dir):

    """ Functional test for text, paragraph, and page
    splitting.

    """

    #Create PDFLITE object, initialize with path & filename.
    writer = PDFLite(os.path.join(test_dir, "tests/JustifyTest.pdf"))

    # If desired (in production code), set compression
    # writer.setCompression(True)

    # Set general information metadata
    writer.set_information(title="Testing Text")  # set optional information

    # Use get_document method to get the generated document object.
    document = writer.get_document()

    # Example for adding short and long text and whitespaces
    document.add_text("Testing")
    document.add_newline(4)
    document.set_justification('right')
    document.add_text("Testing Right")
    document.add_text("Testing Right")
    document.add_newline(2)
    document.set_justification('center')
    document.add_text("In the middle")
    document.add_newline()
    document.add_text("Center")
    document.add_newline()
    document.add_text("""Lorem Ipsum is simply dummy text of the printing and\
        typesetting industry. Lorem Ipsum has been the industry's\
        standard dummy text ever since the 1500s, when an unknown\
        printer took a galley of type and scrambled it to make a\
        type specimen book. It has survived not only five centuries,\
        but also the leap into electronic typesetting, remaining\
        essentially unchanged. It was popularised in the 1960s with\
        the release of Letraset sheets containing Lorem Ipsum passages,\
        and more recently with desktop publishing software like Aldus\
        PageMaker including versions of Lorem Ipsum.""")

    document.set_justification('right')
    document.add_text("right")
    document.add_newline(2)
    document.add_text("""Lorem Ipsum is simply dummy text of the printing and\
        typesetting industry. Lorem Ipsum has been the industry's\
        standard dummy text ever since the 1500s, when an unknown\
        printer took a galley of type and scrambled it to make a\
        type specimen book. It has survived not only five centuries,\
        but also the leap into electronic typesetting, remaining\
        essentially unchanged. It was popularised in the 1960s with\
        the release of Letraset sheets containing Lorem Ipsum passages,\
        and more recently with desktop publishing software like Aldus\
        PageMaker including versions of Lorem Ipsum.""")

    # Close writer
    writer.close()

if __name__ == "__main__":
    JustifyTest()
