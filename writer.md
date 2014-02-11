# <a name="top"></a>Pypdflite Documentation

1. [Intro](index.html)
1. [Writer](writer.html)
    1. [Constructor](#construct)
    2. [Closing](#close)
    3. [Options](#options)
2. [Document Object](document.html)
3. [Cursor Object](cursor.html)
4. [Color Object](color.html)
5. [Tables](tables.html)
6. [Cell Formats](cellformat.html)

# Writer Object

The writer object does the initial setup on the document.

## <a name="construct"></a>Constructor

### writer = PDFLite(filepath, orientation, layout, font_list, font_dir)

```
from pypdflite import PDFLite

writer = PDFLite("hello.pdf")

```

**Parameters:** 

* **filepath :**

    * A string file path for the pdf to store the document to,

    * A writable object like StringIO,

    * The literal string "string", to return the buffer as a string

*  **orientation (string):**

    * 'P' for portrait default

    * 'L' for landscape default

* **layout (string):**

    * One of : 'a3', 'a4', 'a5', 'letter', 'legal', '11x17'

* **font_list (list):**

    * A list of paths to truetype font files you wish to include

* **font_dir (string):**

    * The path to a directory where you want to load fonts from. 

Note: PDFLite searches system files for fonts if font_list and font_dir are not set.

### writer.get_document()

* Returns PDFDocument object.

```
    document = writer.get_document()
```

## <a name="close"></a>Closing

*[top](#top)*

### writer.close()

```
    result = writer.close()
```

* Required at the end to close and generate the pdf.

* Returns None if saved as a document, else returns either a string or the 
writable object given in the constructor.

*[top](#top)*

## <a name="options"></a>Other Options

### writer.set_compression(bool)

* Defaults to True, pdf will be compressed. Set to False if you would like to 
debug the pdf in a text editor.

### writer.set_information(title, subject, author, keywords, creator)

Information is metadata that can be seen in the 'properties' dialog in readers.

* Set with strings, in order or by keyword, use None to skip

*[top](#top)*