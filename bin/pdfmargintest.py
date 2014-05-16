from pypdflite.pdflite import PDFLite


def MarginTest():

    """ Functional test for text, paragraph, and page
    splitting.

    """

    #Create PDFLITE object, initialize with path & filename.
    writer = PDFLite("generated/MarginTest.pdf")

    # If desired (in production code), set compression
    # writer.setCompression(True)

    # Set general information metadata
    writer.set_information(title="Testing Margins")  # set optional information

    # Use get_document method to get the generated document object.
    document = writer.get_document()
    document.set_margins(20, 30, 20, 30)

    document.set_font("helvetica", size=20)
    # Add test text
    document.add_text("""|00 TTTT TTTTTT TTTTTT TTTTT TTTTT TTTTT TTTTT TTT|
                         |01.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |02.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |03.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |04.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |05.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |06.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |07.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |08.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |09.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |10.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |11.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |12.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |13.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |14.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |15.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |16.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |17.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |18.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |19.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |20.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |21.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |22.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |23.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |24.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |25.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |26.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |27.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |28.. .... .... .... .... .... .... .... .... ...... .... .... .... .... .... .... .... .... ... |\
                         |29.. .... .... .... ....
                      """)

    document.add_text(" Small words ")
    document.add_text(""" Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has
                          been the industry's standard dummy text ever since the 1500s, when an unknown printer took a
                          galley of type and scrambled it to make a type specimen book. It has survived not only five
                          centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
                          It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum
                          passages, and more recently with desktop publishing software like Aldus PageMaker including
                          versions of Lorem Ipsum.""")

    writer.close()