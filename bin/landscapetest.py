from pypdflite.pdflite import PDFLite


def LandscapeTest():

    """ Test landscape orientation & background images.

    """

    #Create PDFLITE object, initialize with path & filename.
    writer = PDFLite("generated/Landscape.pdf", orientation="P")
    # If desired (in production code), set compression
    # writer.setCompression(True)

    # Set general information metadata
    writer.set_information(title="Testing Landscape")  # set optional information

    # Use get_document method to get the generated document object.
    document = writer.get_document()

    # Example for adding short and long text and whitespaces
    document.add_text("Testing")
    document.add_newline(4)
    document.add_text("Testing Again")
    document.add_newline()
    document.add_page()
    document.change_page_orientation()
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
    # Close writer
    writer.close()

if __name__ == "__main__":
    LandscapeTest()
