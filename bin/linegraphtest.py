from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcursor import PDFCursor
from pypdflite.pdfobjects.pdfgraphformat import BasicBackground

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
    data = [{"series1": [(0, 100), (3600, 425), (7200, 550), (10800, 425), (14400, 500), (18000, 825)]},
           {"series2": [(0, 50), (3600, 240), (7200, 675), (10800, 775), (14400, 980)]}]

    document.add_line_graph(data, cursor, 400, 200, "Hits over Time", (0, 18000), (0, 1100), (3600, 100), ("time (s)", "count"), "Auto", background=BasicBackground, legend="right")

    cursor = PDFCursor(100, 400)
    document.add_line_graph(data, cursor, 400, 300, "Hits over Time", None, None, (3600, 50), ("time (s)", "count"), "Auto", background=BasicBackground, dots=1)

    # Close Document
    writer.close()


if __name__ == '__main__':
    LineGraphTest()