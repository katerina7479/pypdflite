'''
Created on Mar 15, 2014

@author: tjoneslo
'''
from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolor import PDFColor
from pypdflite.pdfobjects.pdfcursor import PDFCursor
from pypdflite.pdfobjects.pdfellipse import PDFEllipse

def EllipseTest():
    '''
    Functional test for drawing eclipses
    '''
    # Create PDFLite object
    writer = PDFLite("generated/EllipseTest.pdf")

    # Set compression defaults to False
    writer.set_compression(False)

    # Set document metadata
    writer.set_information(title="Testing Lines")  # set optional information

    # Get documnet object
    document = writer.get_document()

    color  = PDFColor(name = 'red')
    center = PDFCursor(100, 100)
    radius = PDFCursor(10,10)
    
    circle = PDFEllipse (document.session, document.page, center, radius, color)
    circle._draw()
    
    center.x = 200
    center.y = 200
    circle = PDFEllipse (document.session, document.page, center, radius, color, stroke='F')
    circle._draw()
    
    center.x=100
    center.y=200
    radius.x=20
    circle = PDFEllipse(document.session, document.page, center, radius, color, size=3)
    circle._draw()
    radius.x = 10
    radius.y = 20
    
    color.set_color_by_name('green')
    circle._draw()
    

    # Close Document
    writer.close()


if __name__ == '__main__':
    EllipseTest()