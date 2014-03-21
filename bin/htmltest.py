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
    header2 = document.set_font('helvetica', style='I', size=18)

    html_text = """
                  <h1>My Week</h1>
                  <p>Today, the day is <span class="red coolfont" data-bind="daytoday"></span>, and it is sunny here in
                        <span class="green" data-bind="location"></span>. Honestly, it's almost always sunny. It
                        can get rather boring.</p>
                  <br/>
                  <h2>Things I miss</h2>
                  <ul>
                  <li>Fall Carnivals</li>
                  <li>Skiing <span class='blue' data-bind="skiing"></span></li>
                  <li>Museums</li>
                  <li><p>And a whole bunch of other things, that I'm not sure if I just liked it because I was a kid,
                  or because it was actually a lot of fun.</p></li>
                  </ul>
                  <p>Next week I will go to the <span class="blue coolfont" data-bind="destination"></span>.....
                  </p>
                """

    document.add_html(html_text,
                      context={"daytoday": " Thursday", "location": " California", "destination": " opera", "skiing": " at Stowe."},
                      formats={"h1": header1, "h2": header2, "red": red, "coolfont": coolfont, "p": normalfont,
                               'ul': normalfont, 'blue': blue, 'green': green}
                      )

    document.add_text("After HTML.")
    writer.close()


if __name__ == "__main__":
    HtmlTest()
