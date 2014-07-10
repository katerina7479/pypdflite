
from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolor import PDFColor
from pypdflite.pdfobjects.pdfcursor import PDFCursor


def PieChartTest():
    """
    Functional test for drawing eclipses
    """
    # Create PDFLite object
    writer = PDFLite("generated/PieChart.pdf")

    # Set compression defaults to False
    writer.set_compression(False)

    # Set document metadata
    writer.set_information(title="Testing Pie Charts")  # set optional information

    # Get document object
    document = writer.get_document()
    cursor = PDFCursor(100, 300)
    data = [("English", 565004126), ("Chinese", 509965013), ("Spanish", 164968742),
            ("Arabic", 65365400), ("French", 59779525), ("Russian", 59700000),
            ("Japanese", 99182000), ("Portuguese", 82586600), ("German", 75422674),
            ("Korean", 39440000)]

    document.add_pie_chart(data, cursor, 400, 300)

    # Close Document
    writer.close()


if __name__ == '__main__':
    PieChartTest()