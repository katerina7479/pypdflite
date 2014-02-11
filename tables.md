# <a name="top"></a>Pypdflite Documentation

1. [Intro](index.html)
1. [Writer](writer.html)
2. [Document Object](document.html)
3. [Cursor Object](cursor.html)
4. [Color Object](color.html)
5. [Tables](#table)
    1. [Constructor](#construct)
    2. [Writing](#writing)
    3. [Formatting](#format)
6. [Cell Formats](cellformat.html)


# <a name="table"></a>Table Object

Tables are created and modeled in memory, and are only fixed into place
on the draw method. You initialize the table with the number of rows and columns
and then a set of blank cells are created with references to their position.

You can set text and formatting by row, column, or individual cells.

You can overwrite text and format. One strategy might be to write with default formats, 
for a row, and then overwrite them with individual cell formats.

## <a name="construct"></a>Constructor

### document.add_table(rows, columns, cursor=None)

** Returns: ** PDFTable object

* ** rows (int): **
    * Requires an integer number of rows

* ** columns (int): **
    * Required an integer number of columns

* ** cursor (PDFCursor): **
    * Cursor for upper left corner of the table
    * Defaults to page cursor

Note: Cells are initialized with a default font equal to the page font, and default
formats. See [Cell Formats](cellformat.html) for reference.

*[top](#top)*

## <a name="writing"></a>Writing

### table.write(row, col, text, format=None)

Writes text to cell, and sets format, if provided.

* ** row (int): **
    * Row number of cell
    * Row numbering starts at 0

* ** column (int): **
    * Column number of cell
    * Column numbering starts at 0

* ** text (string or numbers): **
    * Unless overwritten, columns will re-size to fit text.
    * May use 'text-wrap' attribute in format to allow for wrapping
    * Use '\n' character to specify wrap point.

* ** format (PDFCellFormat): **
    * Get through the document.add_cell_format() method.
    * Will use default cell format.

### table.write_row(row, col_start, data, format)

* ** row (int): **
    * Row number of cell
    * Row numbering starts at 0

* ** column_start (int): **
    * Number of column to start writing (does not need to be 0, you may write only part of a row)
    * Column numbering starts at 0

* ** data [list of strings or numbers]: **
    * Unless overwritten, columns will re-size to fit text.
    * May use 'text-wrap' attribute in format to allow for wrapping
    * Use '\n' character to specify wrap point.

* ** format (PDFCellFormat): **
    * Get through the document.add_cell_format() method.
    * Will use default cell format.

### table.write_column(row_start, col, data, format)

* ** row_start (int): **
    * Number of row to start writing, (may write part of a column)
    * Row numbering starts at 0

* ** column (int): **
    * Column number
    * Column numbering starts at 0

* ** data [list of strings or numbers]: **
    * Unless overwritten, columns will re-size to fit text.
    * May use 'text-wrap' attribute in format to allow for wrapping
    * Use '\n' character to specify wrap point.

* ** format (PDFCellFormat): **
    * Get through the document.add_cell_format() method.
    * Will use default cell format.

*[top](#top)*

## <a name="format"></a>Setting Format

### table.set_format(row, col, format)

Sets format of cell.

* ** row (int): **
    * Row number of cell
    * Row numbering starts at 0

* ** column (int): **
    * Column number of cell
    * Column numbering starts at 0

* ** format (PDFCellFormat): **
    * Get through the document.add_cell_format() method.


### table.set_format_row(row, col_start, format)

* ** row (int): **
    * Row number of cell
    * Row numbering starts at 0

* ** column_start (int): **
    * Number of column to start setting format (may set only part of a row)
    * Column numbering starts at 0

* ** format (PDFCellFormat): **
    * Get through the document.add_cell_format() method.


### table.set_format_column(row_start, col, format)

* ** row_start (int): **
    * Number of row to start setting format, (may set part of a column)
    * Row numbering starts at 0

* ** column (int): **
    * Column number
    * Column numbering starts at 0

* ** format (PDFCellFormat): **
    * Get through the document.add_cell_format() method.

### table.set_column_width(column, width)

* ** column (int): **
    * Column number
    * Column numbering starts at 0

* ** width (int): **
    * May set the width of the column in pixels. 
    * Be careful: If the width is less then the largest text, there will be overlap on the page
    * If the width is too large, the table may run off the edge of the page.

### table.set_row_height(row, height)

* ** row (int): **
    * Row number of cell
    * Row numbering starts at 0

* ** height (int): **
    * May set the height of the row in pixels.
    * Use 'valign' in cell format to change vertical alignment

*[top](#top)*
