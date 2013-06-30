from pypdflite.pdflite import PDFLite


Writer = PDFLite("LinesTest.pdf")
#Writer.setCompression(True)
Writer.setInformation(title="Testing Lines")  # set optional information
Document = Writer.getDocument()
Document.addText("Testing")
Document.addNewline(4)
Document.addLine(20, 40, 20, 80)
Writer.close()
