from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolorscheme import PDFColorScheme
from pypdflite.pdfobjects.pdfcolor import PDFColor


writer = PDFLite("LinesTest.pdf")
#writer.setCompression(True)
writer.set_information(title="Testing Lines")  # set optional information
document = writer.get_document()
document.add_line(20, 40, 300, 80)

document.add_text("Testing")
document.add_newline(1)
document.draw_horizonal_line()

lightblue = PDFColor(name='lightblue')
newscheme = PDFColorScheme(fillcolor=lightblue)

<<<<<<< HEAD
Document.setColorScheme(newscheme)
Document.drawRectangle(0, 0, 10, 10, style='B')
=======
document.set_color_scheme(newscheme)
document.draw_rectangle(150, 500, 300, 600, style='B')
>>>>>>> 6bde21802808269f749a812a05224ad4b0ca4698

writer.close()
