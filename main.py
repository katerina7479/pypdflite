from pypdflite.pdflite import PDFLite


Writer = PDFLite("testing.pdf")
#Writer.setCompression(True)
Writer.setInformation(title="Testing")  # set optional information
Document = Writer.getDocument()
Document.addText("Testing")
Document.addText("Testing Again")
Writer.close()
