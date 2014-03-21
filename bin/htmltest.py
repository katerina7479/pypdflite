from pypdflite.pdflite import PDFLite
from pypdflite.pdfobjects.pdfcolor import PDFColor


def HtmlTest():
    writer = PDFLite("generated/HTMLtest.pdf")
    document = writer.get_document()

    document.add_text('Sample text')
    document.add_newline(2)


    red = PDFColor(name="red")
    blue = PDFColor(name='blue')
    green = PDFColor(name='green')

    normalfont = document.get_font()
    header1 = document.set_font('helvetica', style='B', size=22)
    coolfont = document.set_font('comic sans ms', style='', size=12)


    html_text = """
                  <h1>My Week</h1>
                  <p>Today, the day is <span class="red coolfont" data-bind="daytoday"></span>, and it is sunny here in
                        <span class="green" data-bind="location"></span>. Honestly, it's almost always sunny. It
                        can get rather boring. I miss snow.
                  </p><br/>
                  <p>Next week I will go to the <span class="blue coolfont" data-bind="destination"></span>.....
                  </p>
                """

    document.add_html(html_text,
                      context={"daytoday": " Thursday", "location": " California", "destination": " opera"},
                      formats={"h1": header1, "red": red, "coolfont": coolfont, "p": normalfont, 'blue': blue, 'green': green}
                      )

    document.add_text("After HTML.")
    writer.close()


if __name__ == "__main__":
    HtmlTest()
