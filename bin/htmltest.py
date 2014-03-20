from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolor import PDFColor


def HtmlTest():
    writer = PDFLite("htmltest.pdf")
    document = writer.get_document()

    document.add_text('Sample text')
    document.add_newline(2)


    red = PDFColor("red")

    normalfont = document.get_font()
    header1 = document.set_font('helvetica', style='B', size=24)
    coolfont = document.set_font('comic sans ms', style='', size=12)

    document.add_html("""<h1>This is h1 text.</h1>
                    <p>This is a sample paragraph with a formatted variable equal to <span class="red coolfont" data-bind="myvar"></span></p>
                    """, context={"myvar": 5}, formats={"h1": header1, "red": red, "coolfont": coolfont, "p": normalfont}
                      )

    document.add_newline(2)
    document.add_text("After HTML.")
    writer.close()


if __name__ == "__main__":
    HtmlTest()
