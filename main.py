from pypdflite.pdflite import PDFLite


Writer = PDFLite("testing.pdf")
Document = Writer.getDocument()
Document.addText(40, 50, "Testing")
Writer.close()
