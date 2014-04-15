---
layout: default
title: Document
---

# PDFDocument

The document is the main interface with the library

1. [Intro](index.html)
1. [Writer](writer.html)
2. [Document](document.html)
    1. [Constructor](#construct)
    1. [Text](#text)
    2. [Page](#page)
    3. [Font](#font)
    4. [Color](#color)
    5. [Cursor](#cursor)
    6. [Shape](#shape)
    7. [Image](#image)
    8. [Table](#table)
3. [Cursor](cursor.html)
4. [Color](color.html)
5. [Table](tables.html)
6. [Cell Formats](cellformat.html)

# <a name='doc'></a>Constructor

The document object isn't instantiated directly, instead call the 
get_document() method on the writer class.


```
    document = writer.get_document()
```

# <a name='text'></a>Text Methods

## document.add_text(text, cursor=None)

* **text (string):**
    * Text may be strings of any length. The writer will wrap as necessary based on
    the margins, and will attempt to add new pages as well. 
    * Newline ('\n') characters are caught, and a new line is added.
    * For large text, use the Python '\' endline character to allow the writer to 
    determine where the wraps are.

* **cursor (PDFCursor):**
    * The cursor is optional. You may provide a PDFCursor object with specified x and y
    values to place text specifically. Otherwise the page cursor will be used.
    See [Cursor](cursor.html)

```
    document.add_text("This is my text\n")

    document.add_text(
        """Lorem ipsum dolor sit amet, consectetur adipiscing\
        elit.Cras et erat dolor. Nullam id aliquam neque. Vivamus\
        nec nibh orci. Nam faucibus dignissim diam eget tempor.\
        Aenean neque sem, euismod sit amet tellus nec, elementum\
        varius diam. Vestibulum in ultricies enim. Fusce imperdiet\
        tempus lacus facilisis vestibulum. Vestibulum urna magna,\
        dignissim vel venenatis in, pulvinar ac orci. Etiam vitae\
        tempor metus, eu tristique mauris. Donec tincidunt purus\
        et scelerisque sagittis. Proin semper facilisis\
        vehicula.""")

```

## document.add_newline(number)

* **number (int):**
    * Adds specified number of newlines. 
    * Line height is based on page font.
    * Default is 1.

```
    document.add_newline(20)

```

## document.add_indent(number)

* **number (int):**
    * Adds an indent of number spaces.
    * Space width based on page font.
    * Defaults to 4 spaces.

## document.draw\_horizonal\_line()

* Draws a horizontal line from margin to margin.
* Does not change the page cursor

## document.start\_block\_indent(int)

* Moves left margin in by int pixels (defaults to 20).
* Text will wrap between new left margin and the existing right margin.
* Stops with document.end_block_indent()

## document.end\_block\_indent()

* Resets left margin to previous position

# <a name='page'></a>Page Methods

## document.add_page()

* Starts a new page

## document.get_page()

**Returns:** current PDFPage object.

Note: There shouldn't be any need to call methods on the page object directly.

## document.set_margins(left, top=None, right=None, bottom=None)

* Margins are defined as distance in from the edge of the page border.

* Set margins in pixels. 
    * If only left is specified, all margins will be set the same.
    * If left and top are specified, right will be set equal to left, bottom equal to top
    * You may also pass a valid PDFMargin object in as left.
    * Becomes default margins for current and future pages.

## document.add\_page\_numbers(location, font, cursor, color, text1="Page %s", text2=None)

* **location (string):**
    * Location in the page footer of the page number
    * May be "right", "center" or "left"
    * Defaults to 'right'

* **font (PDFFont):**
    * Must be a PDFFont object (can get one by calling "document.get_font()")
    * If not specified, will default to the last font on each page

* **cursor (PDFCursor):**
    * Must be a PDFCursor object.
    * If location is not specific enough, you may specify a cursor
    * The page numbers will be placed starting at the specified x, y coordinate.
    * Careful! This method may not work well with page orientation changes, or different
    page sizes. In that case, consider using location.

* **color (PDFColor):**
    * Must be a PDFColor object.
    * Sets the text color of all page numbers (otherwise it will default to the 
    last text color on the page)

* **text1 (string):**
    * Must have a %s for the page number reference.
    * Defaults to "Page %s"
    * Options may include "%s", "page %s", "#%s", as desired.

* **text2 (string):**
    * Specify with %s for total pages
    * totalstring = text 1 + text 2
    * Defaults to None
    * Options may include " of %s", ", %s", " | %s", as desired.

## document.change\_page\_orientation()

* Toggles page orientation for current page only


# <a name='font'></a>Font Methods

## document.set_font(family, style, size, font=None)

**Returns:** PDFFont object

* **family (string):**
    * Specify the font name without style (i.e. no bold, italic, oblique)
    * Can use any of the Core PDF fonts
        * 'courier'
        * 'helvetica'
        * 'times'
        * 'symbol'
        * 'zapfdingbats'

    * May use system fonts from system font directories (if search path unmodified)
    * May use fonts set by font_list or font_dict in PDFLite (writer) object
    * Default page font is 'Helvetica'

Note: Only Core or TrueType fonts (.ttf) are supported. Non-english style fonts
are not supported at this time.

* **style (string):**
    * 'B' for bold
    * 'I' for italic
    * 'U' for underline
    * Concatenate for multiple styles, i.e. 'BU' is bold-underline
    * Order of characters is irrelevant
    * Defaults to no style

* **size (int):**
    * Size in pt for font
    * Default is 12

* **font (PDFFont):**
    * If a font object is specified with keyword 'font=', other input values
    are ignored.
    * May be used with document.get_font() as shown below:

```
    default_font = document.get_font()
    document.set_font('helvetica', style='B', size=24)
    document.add_text("Testing a Header")

    # Change font back
    document.set_font(font=default_font)
    document.add_newline(2)
    document.add_text("And we're back to normal after the header.")
```

## document.get_font()

**Returns:** current PDFFont object

## document.set\_font\_size(size)

* **size (int):**
    * Changes current font size to int. 
    * Use this instead of trying to modify font objects directly.


# <a name='color'></a>Color Methods
There are 3 document properties where color is defined: text, draw, and fill

* Colors are set by default to black text, black draw, and white fill

* If you want to change the colors, there are two ways to do it.

*Color Example*

```
    # Get a default and change it
    mycolor = document.get_color()
    mycolor.set_by_name('blue')
    mynewcolor = document.get_color()
    mynewcolor.set_by_number(125, 125, 0)

    # Or Create your Own
    from pypdflite import PDFColor

    blue = PDFColor(0, 0, 255)
```

See [Colors](color.html) for more details

## document.set\_text\_color(color)

* Color must be a PDFColor object.
* Default is black.

## document.set\_draw\_color(color)

* Color must be a PDFColor object.
* Default is black.

## document.set\_fill\_color(color)

* Color must be a PDFColor object.
* Default is white.


# <a name='cursor'></a>Cursors

A cursor stores an x and y value representing a point on the page. 

The origin, x=0, y=0 is at the upper left hand corner of each page. The cursor adjusts
the initial x, y for page margins (so it may start at x=20, y=20) by default.

x increases horizontally from left to right, y increases from top to bottom.

Each page maintains a cursor, but you may create multiple cursors for different purposes.

See [Cursors](cursors.html) for more cursor manipulation.

## document.set_cursor(x, y)

* x and y may be integers, or x may be a PDFCursor, with no y

* Changes the current page cursor to new point.

*Setting Cursors*

```
    # Easy
    document.set_cursor(150, 300)

    # Same as
    new_cursor = document.get_new_cursor()
    new_cursor.x = 150
    new_cursor.y = 300
    document.set_cursor(new_cursor)

    # Or
    from pypdflite import PDFCursor

    newcursor = PDFCursor(150, 300)
    document.set_cursor(newcursor)
```

## document.get\_new\_cursor()

**Returns:** a default PDFCursor 

You may set the x and y on this directly:

```
    mycursor = document.get_new_cursor()
    mycursor.x = 150
    mycursor.y = 300

```


## document.get_cursor()

**Returns:** a PDFCursor (copy of the current page cursor.)


# <a name='shape'></a>Shape Methods

## document.add_line(x1, y1, x2, y2, cursor1, cursor2, style='solid')

A line requires two points to define it. You may enter either by x's and y's,
or with cursors:

* **x1, y1, x2, y2 (int), cursor1, cursor2 (PDFCursor):**
* Specify one of the following:
    * x1, y1, x2, y2
    * x1, x2, cursor2
    * cursor1, cursor2
    * cursor1, x2, y2

* **style (string):**
    * May be 'solid', 'dashed', or 'dots'

*Line Example*

```
    document.add_line(20, 30, 150, 300)

    # Same as:
    from pypdflite import PDFCursor
    start = PDFCursor(20, 30)
    end = PDFCursor(150, 300)
    document.add_line(cursor1=start, cursor2=end)

```

## document.add_rectangle(x1, y1, x2, y2, width, height, cursor1, cursor2, style='S', size=1)

* **x1, y1, x2, y2 (int), cursor1, cursor2 (PDFCursor):**
* Specify one of the following:
    * x1, y1, x2, y2
    * x1, y1, width + height
    * x1, x2, cursor2
    * cursor1, cursor2
    * cursor1, width + height
    * cursor1, x2, y2

* **style (string):**
    * 'S' is borders only, no fill (default)
    * 'B' is borders and fill
    * 'F' is fill only, no borders

* **size (int):**
    * Thickness of the border in pixels, defaults to 1.

*Rectangle Example*

```
    # Simple
    document.add_rectangle(20, 30, 150, 300, style='B', size=2)

    # Or
    start = PDFCursor(20, 30)
    end = PDFCursor(150, 300)

    document.add_rectangle(cursor1=start, cursor2=end)

    # Or with more complex cursor manipulation
    diff = start - end
    w = diff.x
    h = diff.y

    document.add_rectangle(100, 100, width=w, height=h)
```

# <a name='image'></a>Image Methods

Currently .png and .jpeg images are supported.

Images are embedded into the pdf file. You must add the image first, and then
you can draw the image.

## document.add_image(image, name=None)

**Returns:** PDFImage object

* **image (string):**
    * Path to image file.

* **name (string):**
    * Optional name

## document.draw_image(image, cursor=None, width=None, height=None)

* **image:**
    * May be PDFImage object, or the specified image name

* **cursor:**
    * Must be a PDFCursor.
    * Defaults to page cursor

* **width (int):**
    * Image width specified in pixels.
    * Scales the image proportionally

* **height (int):**
    * Image height specified in pixels.
    * Scales the image proportionally

Note: If width and height are both specified, it may result in the image being
stretched.

*Image Example*

```
    # Simple Example
    mylogo = document.add_image("logo.png")
    document.draw_image(mylogo)

    # With cursor and width
    im_cursor = PDFCursor(40, 150)
    document.draw_image(mylogo, im_cursor, width=100)

```

## document.set\_background\_image(image)

Sets a background image, at cursor = (0,0) with no margins.
Stretches image to page width. Doesn't interfere with page cursor.

* **image (string or PDFImage):**
    * May be path to image file
    * May be previously added PDFImage object


# <a name='table'></a>Table Methods

Tables start by initializing with the specified number of rows and columns, and blank cells.
Each cell has a text and a cell_format object.

You can specify default fonts and cell_formats for the table, and write
to rows, columns, or individual cells. 

Table information is writen using the table object.

See [Tables](tables.html) for PDFTable methods.

## document.add_table(rows, columns, cursor=None)

**Returns:** PDFTable object.
    
* **rows (int):**
    * The number of rows

* **columns (int):**
    * The number of columns

* **cursor (PDFCursor):**
    * A PDFCursor object to specify the upper left hand point of the table.
    * Defaults to current page cursor at time of drawing.

Note: If the table does not have enough room on the page to draw itself, there 
will be errors on the page.

## document.draw_table(table)

* **table (PDFTable):**  
    * Requires the table object created from the document.add_table() method.

## document.add\_cell\_format(data=None, font=None)

* **data (dictionary):**
    Dictionary of key value pairs specifying a cell format.

    See [Cell Formats](cellformat.html) for data values, and defaults.

* **font (PDFFont):**
    Sets font for cell. Defaults to page font.

*Table Example*

```
data = [["Heading1", "Heading2", "Heading3"],
        ["Cell a2", "Cell b2", "Cell c2"],
        ["Cell a3", "Cell b3", "Cell c3"]]

mytable = document.add_table(3, 3)

default_format = document.add_cell_format({'font': default_font,
                                           'align': 'left',
                                           'border': (0, 1)})

header_format = document.add_cell_format({'font': underline,
                                          'align': 'right',
                                          'border': (0, 1)})

mytable.write_row(0, 0, data[0], header_format)
mytable.write_row(1, 0, data[1], default_format)
mytable.write_row(2, 0, data[2], default_format)

document.draw_table(mytable)
```
