import os
from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolor import PDFColor


if __name__ == "__main__":
    writer = PDFLite("Hello World.pdf")
    writer.set_information(title="Hello")
    document = writer.get_document()
    document.add_text("Hello World")
    writer.close()