import os
from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcursor import PDFCursor


def MultiBarChartTest(test_dir):
    """
    Functional test for drawing eclipses
    """
    # Create PDFLite object
    writer = PDFLite(os.path.join(test_dir, "tests/MultiBarChart.pdf"))

    # Set compression defaults to False
    writer.set_compression(False)

    # Set document metadata
    writer.set_information(title="Testing Multi Bar Chart")  # set optional information

    # Get document object
    document = writer.get_document()

    cursor = PDFCursor(100, 50)
    data = [{"Susan Smith": [("S", 47.5), ("M", 46.1), ("T", 48.3), ("W", 44.2), ("T", 46.7), ("F", 47.6), ("S", 46.3)]},
            {"Jane Doe": [("S", 38.2), ("M", 38.9), ("T", 39.2), ("W", 38.6), ("T", 40.1), ("F", 41.6), ("S", 42.2)]}
           ]

    document.add_multi_bar_chart(data, cursor, 400, 300, "Candidate Polls", axis_titles=("day", "percent vote"), y_axis_limits=(35, 50), y_axis_frequency=2)

    cursor = PDFCursor(100, 400)
    document.add_multi_bar_chart(data, cursor, 400, 300, "Candidate Polls", ("day", "percent of votes"), y_axis_limits=(35, 50), y_axis_frequency=2, legend="right")

    # Close Document
    writer.close()


if __name__ == '__main__':
    MultiBarChartTest()