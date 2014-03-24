from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolor import PDFColor


def HtmlTest2():
    writer = PDFLite("generated/HTMLtest2.pdf")
    document = writer.get_document()

    document.add_text('Sample text')
    document.add_newline(2)


    red = PDFColor(name="red")
    blue = PDFColor(name='blue')
    green = PDFColor(name='green')

    normalfont = document.get_font()
    header1 = document.set_font('helvetica', style='B', size=22)
    coolfont = document.set_font('comic sans ms', style='', size=12)
    header2 = document.set_font('helvetica', style='I', size=18)

    html_text = open("bin/test.html")

    document.add_html(html_text,
                      context={"daytoday": " Thursday", "location": " California", "destination": " opera", "skiing": " at Stowe."},
                      formats={"h1": header1, "h2": header2, "red": red, "coolfont": coolfont, "p": normalfont,
                               'ul': normalfont, 'ol': normalfont, 'blue': blue, 'green': green}
                      )

    document.add_text("After HTML.")
    writer.close()


if __name__ == "__main__":
    HtmlTest()