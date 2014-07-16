"""
Created on Mar 15, 2014

@author: tjoneslo
"""
from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolor import PDFColor
from pypdflite.pdfobjects.pdfcursor import PDFCursor
from pypdflite.pdfobjects.pdfellipse import PDFEllipse


def EllipseTest():
    """
    Functional test for drawing eclipses
    """
    # Create PDFLite object
    writer = PDFLite("generated/EllipseTest.pdf")

    # Set compression defaults to False
    writer.set_compression(False)

    # Set document metadata
    writer.set_information(title="Testing Lines")  # set optional information

    # Get document object
    document = writer.get_document()

    color = PDFColor(name='red')
    center = PDFCursor(100, 100)
    radius = PDFCursor(20, 30)
    
    circle = PDFEllipse(document.session, document.page, center, radius, color)
    circle._draw()
    
    center.x = 200
    center.y = 200
    circle = PDFEllipse(document.session, document.page, center, radius, color, style='F')
    circle._draw()
    
    center.x = 100
    center.y = 200
    radius.x = 40
    circle = PDFEllipse(document.session, document.page, center, radius, color, size=3)
    circle._draw()


    # Close Document
    writer.close()


if __name__ == '__main__':
    EllipseTest()