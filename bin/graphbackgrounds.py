from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolor import PDFColor
from pypdflite.pdfobjects.pdfcursor import PDFCursor
from pypdflite.pdfobjects.pdfgraphformat import PDFGraphBackground


def GraphBackgroundTest():
    """
    Functional test for drawing eclipses
    """
    # Create PDFLite object
    writer = PDFLite("generated/GraphBackgrounds.pdf")

    # Set compression defaults to False
    writer.set_compression(False)

    # Set document metadata
    writer.set_information(title="Testing Graph Backgrounds")  # set optional information

    # Get document object
    document = writer.get_document()
    cursor = PDFCursor(100, 50)
    data = [{"series1": [(0, 100), (3600, 425), (7200, 550), (10800, 425), (14400, 500), (18000, 825)]},
           {"series2": [(0, 50), (3600, 240), (7200, 675), (10800, 775), (14400, 980)]}]

    document.add_line_graph(data, cursor, 400, 200, "Hits over Time", (0, 18000), (0, 1100), (3600, 100), ("time (s)", "count"), "Auto", padding=0.11, legend="right")

    cursor = PDFCursor(100, 400)
    data = [{"series1": [(14.2, 215), (16.4, 325), (11.9, 185), (15.2, 332), (18.5, 406), (22.1, 522), (19.4, 412), (25.1, 614), (23.4, 544), (18.1, 421), (22.6, 445), (17.2, 408)]}]

    document.add_xy_scatter(data, cursor, 400, 200, "Ice Cream Sales vs Temperature", (10, 26), (180, 660), (1, 50), ("temperature", "sales"), "Auto", padding=0.11, dots=1, legend="right")

    document.add_page()
    cursor = PDFCursor(100, 50)
    data = [{"Susan Smith": [("S", 47.5), ("M", 46.1), ("T", 48.3), ("W", 44.2), ("T", 46.7), ("F", 47.6), ("S", 46.3)]},
            {"Jane Doe": [("S", 38.2), ("M", 38.9), ("T", 39.2), ("W", 38.6), ("T", 40.1), ("F", 41.6), ("S", 42.2)]}
           ]

    document.add_multi_bar_chart(data, cursor, 400, 300, "Candidate Polls", axis_titles=("day", "percent vote"), y_axis_limits=(35, 50), y_axis_frequency=2)




    # Close Document
    writer.close()


if __name__ == '__main__':
    LineGraphTest()