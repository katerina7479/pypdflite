from pypdflite.pdflite import PDFLite


Writer = PDFLite("testing.pdf")
#Writer.setCompression(True)
Writer.setInformation(title="Testing")  # set optional information
Document = Writer.getDocument()
Document.addText("Testing")
Document.newline(4)
Document.addText("Testing Again")
Document.newline()
Document.indent()
Document.addText("This should be enough text to test going over the edge of the page, and having to wrap back around. Let's see if it works!")
normalfont = Document.getFont()

Document.setFont('helvetica', style='B', size=24)
Document.newline(2)
Document.addText("1.0 Testing a Header")

Document.setFont(font=normalfont)
Document.newline(2)
Document.indent()
Document.addText("And we're back to normal after the header.")

Writer.close()
