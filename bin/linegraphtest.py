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
    cursor = PDFCursor(100, 50)
    data = [{"series1": [(0, 100), (3600, 300), (7200, 550), (10800, 425), (17000, 825)]},
           {"series2": [(0, 50), (3600, 240), (7200, 675), (10800, 800), (14400, 980)]}]

    document.add_line_graph(data, cursor, 400, 300, "Hits over Time", None, None, (3600, 50), ("time (s)", "count"), "Auto", padding=0.11)

    cursor = PDFCursor(100, 400)
    document.add_line_graph(data, cursor, 400, 300, "Hits over Time", None, None, (3600, 50), ("time (s)", "count"), "Auto", padding=0.11)

    # Close Document
    writer.close()


if __name__ == '__main__':
    LineGraphTest()