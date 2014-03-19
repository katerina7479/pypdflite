from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdftransforms import PDFTransform
from pypdflite.pdfobjects.pdftext import PDFText


def TransformTest():

    #Create PDFLITE object, initialize with path & filename.
    writer = PDFLite("generated/Transform.pdf", orientation="P")
    # If desired (in production code), set compression
    writer.set_compression(False)

    # Set general information metadata
    writer.set_information(title="Testing Transform")  # set optional information

    # Use get_document method to get the generated document object.
    document = writer.get_document()
    
    document.add_text("Transform test")
    
    document.add_newline(4)
    
    
    text = PDFText (document.session, document.page, None)
    text._text('transform')
    
    text.cursor.x_plus(20)
    text.text_rotate(90)
    text._text('transform')
    
    text = PDFText (document.session, document.page, None)
    text.cursor.x_plus(20)
    text.text_rotate(180)
    text._text('transform')
    
    text = PDFText (document.session, document.page, None)
    text.cursor.x_plus(20)
    text.text_rotate(-90)
    text._text('transform')
    
    document.add_newline(5)

    text = PDFText (document.session, document.page, None)
    text._text('transform  ')
    text.text_scale(2, 0.5)
    text._text('transform')

    document.add_newline(2)
    text = PDFText (document.session, document.page, None)
    text._text('transform  ')
    text.text_scale(0.5, 2)
    text._text('transform')

    document.add_newline(2)
    text = PDFText (document.session, document.page, None)
    text._text('transform  ')
    text.text_skew(30, 0)
    text._text('transform')

    document.add_newline(2)
    text = PDFText (document.session, document.page, None)
    text._text('transform  ')
    text.text_skew(0, 30)
    text._text('transform')

    
    # Close writer
    writer.close()


if __name__ == "__main__":
    TransformTest()
