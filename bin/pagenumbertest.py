from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolor import PDFColor


def TextTest():

    """ Functional test for text, paragraph, and page
    splitting.

    """

    #Create PDFLITE object, initialize with path & filename.
    writer = PDFLite("TextTest.pdf")

    # If desired (in production code), set compression
    # writer.setCompression(True)

    # Set general information metadata
    writer.set_information(title="Testing Text")  # set optional information

    # Use get_document method to get the generated document object.
    document = writer.get_document()

    # Example for adding short and long text and whitespaces
    document.add_text("Testing")
    document.add_newline(4)
    document.add_text("Testing Again")
    document.add_newline()
    document.add_indent()
    document.add_text(
        "This should be enough text to test going over the edge of the \
        page, and having to wrap back around. Let's see if it works!")
    document.add_page()

    # Save existing font, define a new font, use it for a header
    normal_font = document.get_font()
    document.set_font('helvetica', style='B', size=24)
    header_font = document.get_font()
    document.add_newline(2)
    document.add_text("1.0 Testing a Header")

    # Change font back
    document.set_font(font=normal_font)
    document.add_newline(2)
    document.add_indent()
    document.add_text("And we're back to normal after the header.")
    document.add_newline(2)

    # Test decoration, and size changes
    document.set_font('helvetica', style='BUI', size=12)
    document.add_text("Testing Bold Underline Italic Style")
    document.add_newline(2)
    document.set_font("helvetica", style="BUI", size=24)
    document.add_text("Testing Bold Underline Italic Style Bigger")
    document.add_newline(2)
    document.set_font("helvetica", style="BUI", size=8)
    document.add_text("Testing Bold Underline Italic Style Smaller")

    # Test automatic page split
    document.set_font(font=normal_font)
    document.add_newline(5)
    document.add_text("What")
    document.add_newline(5)
    document.add_text("will")
    document.add_newline(5)
    document.add_text("happen")
    document.add_newline(5)

    # Create color Object, apply to fill color
    document.add_text("when")
    document.add_newline(5)
    lightblue = PDFColor(name='lightblue')
    document.set_text_color(lightblue)
    document.add_text("I")
    document.add_newline(5)
    document.add_text("go")
    document.add_newline(5)
    document.add_text("on")
    document.add_newline(5)
    document.add_text("to")
    document.add_newline(5)
    document.add_text("the")
    document.add_newline(5)
    document.add_text("next")
    document.add_newline(5)
    document.add_text("page?")
    document.add_newline()

    # Test Page splitting with paragraphs
    document.add_text(
        """Lorem Ipsum is simply dummy text of the printing and\
        typesetting industry. Lorem Ipsum has been the industry's\
        standard dummy text ever since the 1500s, when an unknown\
        printer took a galley of type and scrambled it to make a\
        type specimen book. It has survived not only five centuries,\
        but also the leap into electronic typesetting, remaining\
        essentially unchanged. It was popularised in the 1960s with\
        the release of Letraset sheets containing Lorem Ipsum passages,\
        and more recently with desktop publishing software like Aldus\
        PageMaker including versions of Lorem Ipsum.""")
    document.add_newline(2)
    document.add_text(
        """Lorem ipsum dolor sit amet, consectetur adipiscing elit.\
        Cras et erat dolor. Nullam id aliquam neque. Vivamus nec nibh\
        orci. Nam faucibus dignissim diam eget tempor. Aenean neque sem,\
        euismod sit amet tellus nec, elementum varius diam. Vestibulum\
        in ultricies enim. Fusce imperdiet tempus lacus facilisis\
        vestibulum. Vestibulum urna magna, dignissim vel venenatis in,\
        pulvinar ac orci. Etiam vitae tempor metus, eu tristique mauris.\
        Donec tincidunt purus et scelerisque sagittis. Proin semper\
        facilisis vehicula.""")
    document.add_text(
        """Pellentesque rhoncus vestibulum turpis ut varius. Nunc a rutrum\
        est. Etiam sollicitudin rhoncus nisl, quis scelerisque felis\
        dignissim vitae. Maecenas rutrum quam at risus mattis congue. Sed\
        hendrerit nulla ac nunc consectetur suscipit. Fusce elementum\
        interdum nibh, et fermentum lacus egestas non. Sed consectetur\
        mollis tortor, eu aliquam leo tristique sit amet. Etiam nec lectus\
        magna. Nam faucibus scelerisque velit nec cursus. Ut a dolor\
        accumsan, gravida nunc vitae, luctus quam. Vestibulum quis gravida\
        quam. Proin feugiat urna ut rutrum facilisis. Vivamus gravida iaculis\
        nibh at feugiat.""")

    document.add_page_numbers(font=normal_font, color=PDFColor())
    # Close writer
    writer.close()

if __name__ == "__main__":
    TextTest()
