"""
Created on Mar 15, 2014

@author: tjoneslo
"""
from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolor import PDFColor
from pypdflite.pdfobjects.pdfcursor import PDFCursor


def LineGraphTest():
    """
    Functional test for drawing eclipses
    """
    # Create PDFLite object
    writer = PDFLite("generated/LineGraph.pdf")

    # Set compression defaults to False
    writer.set_compression(False)

    # Set document metadata
    writer.set_information(title="Testing Line Graphs")  # set optional information

    # Get document object
    document = writer.get_document()
    cursor = PDFCursor(100, 300)
    data = {"series1":[(0, 100), (3600, 300), (7200, 550), (10800, 425), (14400, 911)]}

    document.add_line_graph(data, cursor, 400, 300, (0, 14400, 0, 1000), (3600, 100), ("time", "count"), "S")

    # Close Document
    writer.close()


if __name__ == '__main__':
    LineGraphTest()