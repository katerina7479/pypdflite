from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolorscheme import PDFColorScheme
from pypdflite.pdfobjects.pdfcolor import PDFColor


Writer = PDFLite("LinesTest.pdf")
#Writer.setCompression(True)
Writer.setInformation(title="Testing Lines")  # set optional information
Document = Writer.getDocument()
Document.addLine(20, 40, 300, 80)

Document.addText("Testing")
Document.addNewline(1)
Document.drawHorizonalLine()

lightblue = PDFColor(name='lightblue')
newscheme = PDFColorScheme(fillcolor=lightblue)

Document.setColorScheme(newscheme)
Document.drawRectangle(0, 0, 10, 10, style='B')

Writer.close()
