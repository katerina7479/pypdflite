from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolor import PDFColor
from pypdflite.pdfobjects.pdfcursor import PDFCursor


def XYScatterPlotTest():
    """
    Functional test for drawing eclipses
    """
    # Create PDFLite object
    writer = PDFLite("generated/XYScatterPlot.pdf")

    # Set compression defaults to False
    writer.set_compression(False)

    # Set document metadata
    writer.set_information(title="Testing XY Scatter Plots")  # set optional information

    # Get document object
    document = writer.get_document()
    cursor = PDFCursor(100, 50)
    data = [{"series1": [(14.2, 215), (16.4, 325), (11.9, 185), (15.2, 332), (18.5, 406), (22.1, 522), (19.4, 412), (25.1, 614), (23.4, 544), (18.1, 421), (22.6, 445), (17.2, 408)]}]

    document.add_xy_scatter(data, cursor, 400, 200, "Ice Cream Sales vs Temperature", None, None, None, ("temperature", "sales"), "Auto", padding=0.11, dots=1)

    # Close Document
    writer.close()


if __name__ == '__main__':
    XYScatterPlotTest()