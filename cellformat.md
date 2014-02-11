# <a name="top"></a>Pypdflite Documentation

1. [Intro](index.html)
1. [Writer](writer.html)
2. [Document Object](document.html)
3. [Cursor Object](cursor.html)
4. [Color Object](color.html)
5. [Tables](tables.html)
6. [Cell Formats](#cellformat)
    1. [Constructor](#construct)
    2. [Dictionary Keys](#keys)
    3. [Number Format](#numformat)
    4. [Borders](#borders)
    5. [Use Case](#example)

# <a name='cellformt'></a>Cell Format Object

Cell formats should be set throug the document.add_cell_format method.
They contain dictionary settings for fonts, text alignment, number formatting,
borders, fill colors, and cell padding.

Each cell holds a reference to the specified format object. They may be over-
written after the cell has been set without over-writing the text, using
the table.set_format methods.

## <a name="construct"></a>Constructor

### document.add_cell_format(data=None, font=None)

* **data (dictionary):**
    Dictionary of key value pairs specifing a cell format.

* **font (PDFFont):**
    Sets font for cell. Defaults to page font.

*[top](#top)*

## <a name="keys"></a>Data Dictionary Keys

Key              | Type                | Default            | Options
---------------- | ------------------- | ------------------ | ---------------
'font'           | PDFFont             | page font          | PDFFont objects
'num_format'     | Tuple (string, int) | None               | See [Number Format](#numformat)
'align'          | string              | 'left'             | 'left', 'right' 'center'
'valign'         | string              | 'center'           | 'top' 'center' 'bottom'
'text_wrap'      | bool                | False              | True, False
'fill_color'     | PDFColor            | None               | PDFColor
'text_color'     | PDFColor            | PDFColor('black')  | PDFColor
'border'         | Tuple (int, int)    | (0, 1)             | (type, weight), * [Borders](#borders)
'bottom'         | Tuple (int, int)    | (None, None)       | (type, weight)
'top'            | Tuple (int, int)    | (None, None)       | (type, weight)
'left'           | Tuple (int, int)    | (None, None)       | (type, weight)
'right'          | Tuple (int, int)    | (None, None)       | (type, weight)
'border_color'   | PDFColor            | None               | PDFColor, *
'bottom_color'   | PDFColor            | None               | PDFColor
'top_color'      | PDFColor            | None               | PDFColor
'left_color'     | PDFColor            | None               | PDFColor
'right_color'    | PDFColor            | None               | PDFColor
'padding'        | integer             | False              | Integer, *
'padding_top'    | integer             | 1                  | Integer
'padding_bottom' | integer             | 1                  | Integer
'padding_left'   | integer             | 2                  | Integer
'padding_right'  | integer             | 2                  | Integer

*If set, this value will be applied to all sides of cell

*[top](#top)*

## <a name="numformat"></a>Number Format

If the cell contains a number (int, float), num_format allows you to change
how that number is formatted by keyword, and number of decimals.

* Tuples:
    * ('percent', int)
    * ('decimal', int)
    * ('money', int) or ('$', int)  *US$ only*
    * ('comma', int)  *adds commas for thousands, millions..*
    * ('money_comma', int) or ('$comma', int)

```
    # Shows numbers with two places after the decimal
    # 123.45
    format_dict = {'num_format': ('decimal', 2)}  

    # Shows with percent, no decimals
    # 123 %
    percent_dict = {'num_format': ('percent', 0)}

    document.add_cell_format()
```

*[top](#top)*

## <a name="borders"></a>Borders

Borders are set with an a tuple. The first integer number represents the type of line,
the second is the line weight.

Int | border style
--- | ------------
0   | solid
1   | dashed
2   | dots

```
    # All borders, dashed, weight 1
    border_dict = {'border': (1, 1)}

    # Only bottom border, solid, weight 2
    bottom_border_dict = {'bottom': (0, 2)}

    # No borders
    no_borders_dict = {'borders': (None, None)}

```

Border colors may be set, or it will default to the current page draw_text value,
(typically black).

*[top](#top)*

## <a name='example'></a> Use case

```
    myfont = document.get_font()
    border_center_dict = {'font': myfont, 'border': (0,1), 'align': 'center'}

    border_center_format = document.add_cell_format(border_center_dict)

    #.... Later in the table declarations
    mytable.write_row(1, 0, row_data, border_center_format)
```

*[top](#top)*