from pypdflite.pdflite import PDFLite


Writer = PDFLite("testing.pdf")
#Writer.setCompression(True)
Writer.setInformation(title="Testing")  # set optional information
Document = Writer.getDocument()
Document.addText("Testing")
Document.newline(4)
Document.addText("Testing Again")
Document.newline()
Document.addText("This should be enough text to test going over the edge of the page, and having to wrap back around. Let's see if it works.")
Writer.close()
