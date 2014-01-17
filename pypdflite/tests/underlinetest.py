from ..pdflite import PDFLite


def UnderlineTest():

    """ Functional test for text, paragraph, and page
    splitting.

    """

    #Create PDFLITE object, initialize with path & filename.
    writer = PDFLite("generated/UnderlineTest.pdf")

    # If desired (in production code), set compression
    # writer.setCompression(True)

    # Set general information metadata
    writer.set_information(title="Underlining")  # set optional information

    # Use get_document method to get the generated document object.
    document = writer.get_document()

    # Check underlines at sizes
    document.set_font('helvetica', style='U', size=8)
    document.add_text("Testing size 8, normal")
    document.add_newline(2)

    document.set_font('helvetica', style='U', size=12)
    document.add_text("Testing size 12, normal")
    document.add_newline(2)

    document.set_font('helvetica', style='U', size=16)
    document.add_text("Testing size 16, normal")
    document.add_newline(2)

    document.set_font('helvetica', style='U', size=20)
    document.add_text("Testing size 20, normal")
    document.add_newline(2)

    document.set_font('helvetica', style='U', size=24)
    document.add_text("Testing size 24, normal")
    document.add_newline(2)

    document.set_font('helvetica', style='U', size=28)
    document.add_text("Testing size 28, normal")
    document.add_newline(2)

    document.set_font('helvetica', style='U', size=32)
    document.add_text("Testing size 32, normal")
    document.add_newline(2)

    document.set_font('helvetica', style='U', size=36)
    document.add_text("Testing size 36, normal")
    document.add_newline(2)

    document.add_page()

    # Check underlines with Bold
    document.set_font('helvetica', style='BU', size=8)
    document.add_text("Testing size 8, bold")
    document.add_newline(2)

    document.set_font('helvetica', style='BU', size=12)
    document.add_text("Testing size 12, bold")
    document.add_newline(2)

    document.set_font('helvetica', style='BU', size=16)
    document.add_text("Testing size 16, bold")
    document.add_newline(2)

    document.set_font('helvetica', style='BU', size=20)
    document.add_text("Testing size 20, bold")
    document.add_newline(2)

    document.set_font('helvetica', style='BU', size=24)
    document.add_text("Testing size 24, bold")
    document.add_newline(2)

    document.set_font('helvetica', style='BU', size=28)
    document.add_text("Testing size 28, bold")
    document.add_newline(2)

    document.set_font('helvetica', style='BU', size=32)
    document.add_text("Testing size 32, bold")
    document.add_newline(2)

    document.set_font('helvetica', style='BU', size=36)
    document.add_text("Testing size 36, bold")
    document.add_newline(2)

    # Close writer
    writer.close()

if __name__ == "__main__":
    UnderlineTest()
