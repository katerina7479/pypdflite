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

    # Example for adding short and long text and whitespaces
    document.add_table([["Heading1", "Heading 2", "Heading 3"],
                        ["cell a2", "cell b2", "cell c2"],
                        ["cell a3", "cell b3", "cell c3"],
                        ["cell a4", "cell b4", "cell c4"]
                        ])

    document.add_newline(4)
    document.add_text("Testing followup text")

    # Close writer
    writer.close()

if __name__ == "__main__":
    TableTest()
