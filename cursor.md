---
layout: default
title: Cursor
---

# PDFCursor

The cursor represents an x, y coordinate point on the pdf page. 

1. [Intro](index.html)
1. [Writer](writer.html)
2. [Document](document.html)
3. [Cursor](cursor.html)
    1. [Object](#cursor)
    1. [Constructor](#construct)
    2. [Comparisons](#compare)
    3. [Cursor Math](#math)
    4. [Change](#change)
4. [Color](color.html)
5. [Table](tables.html)
6. [Cell Formats](cellformat.html)

# <a name="cursor"></a>Object

The origin (0,0) is at the upper left hand corner. The x increases 
horizontally to the right, and y increases going down, 
up to the page size (in pixels).

Page Sizes, portrait in pixels

Name     | x (width) | y (height)
-------- | --------- | ---------
'a3'     | 841.89    | 1190.55
'a4'     | 595.28    | 841.89
'a5'     | 420.94    | 595.28
'letter' | 612       | 792
'legal'  | 612       | 1008
'11x17'  | 792       | 1224

Cursors themselves can be modified, or can return a new cursor object.

##  <a name="construct"></a>Constructor

### PDFCursor(x, y, boundary_flag)

* **x (int):**
    * Defines the x coordinate. 
    * If it is less than the xmin boundary, it will be set to the xmin.
    * If it is greater then x_max, it does not change the value, but drawings 
    will be off the page to the right.

* **y (int):**
    * Defines the y coordinate.
    * If it is less then ymin, it is set to ymin.
    * If it is greater then ymax, it does not change the value, but will
    draw off the page to the bottom.

* **boundary_flag (bool):**
    * Sets the xmin and ymin boundaries to the value of x and y.
    * Defaults to false

```
    cursor = PDFCursor(150, 30, True)
    document.set_cursor(cursor)
```


##  <a name="compare"></a>Comparison Methods

### cursor1 > cursor2

* Compares two PDFCursor objects by x and y coordinates, prioritizing the y coordinate.
* The cursor with the higher y coordinate is considered greater. If they have the same
y coordinate, then x coordinates are compared.

```
    cursor1 = PDFCursor(20, 100)
    cursor2 = PDFCursor(25, 30)
    cursor1 > cursor2  # Returns True

```

### cursor1 < cursor2

* Compares two PDFCursor object by x and y coordinates, proritizing the y coordinate.
* The cursor with the higher y coordinate is considered greater. If they have the same
y coordinate, then x coordinates are compared.

```
    cursor1 = PDFCursor(21, 250)
    cursor2 = PDFCursor(22, 250)

    cursor1 < cursor2  # Returns True

```

### cursor1 == cursor2

* Tests for equality. Cursors must have equal x, y coordinates 
* Does not check boundaries.

```
    cursor1 = PDFCursor(100, 100)
    cursor2 = PDFCursor(100, 100, True)

    cursor1 == cursor2  # Returns True
    cursor2.xmin  # 100
    cursor1.xmin  # 0
```

##  <a name="math"></a>Cursor Math methods

### cursor.copy()

**Returns:** PDFCursor object

* Coordinates, boundaries are set equal.
* cursor1 remains unchanged.

```
    cursor2 = cursor1.copy()
    cursor1.x == cursor2.x  # True
    cursor1.xmin == cursor2.xmin  # True
    # etc.

```

### cursor1 + cursor2

**Returns:** PDFCursor object

* x's are added, and y's are added.
* Cursors remain unchanged.

```
    cursor1 = PDFCursor(30, 30)
    cursor2 = PDFCursor(20, 20)
    cursor3 = cursor1 + cursor2

    cursor3.x, cursor3.y  # 50, 50

```

### cursor1 - cursor2

**Returns:** PDFCursor object

* x's are added, and y's are added.
* Cursors remain unchanged.
* Be careful of boundaries

```
    cursor1 = PDFCursor(100, 100)
    cursor2 = PDFCursor(5, 5, True)
    cursor3 = cursor1 - cursor2

    cursor3.x, cursor3.y  # 95, 95
```

### cursor * number

**Returns:** PDFCursor object

* x's and y's are scaled by the number. May result in non-integer coordinates.
* Cursors remain unchanged.

```
    cursor1 = PDCursor(100, 100)
    cursor2 = cursor1 * 0.5
    cursor2.x, cursor2.y  # 50, 50
```

##  <a name="change"></a>Changes the existing cursor

### cursor.x_plus(dx)

* **dx (number):**
    * Adds dx to x coordinate.
    * number may be negative for subtraction
    * If no number is supplied, defaults to 2 px.

### cursor.y_plus(dy)

* **dy (number):**
    * Adds dy to y coordinate. 
    * number may be negative for subtraction
    * If no number is supplied, defaults to 2 px.

### cursor.x_reset()

* Resets x to x_min

### cursor.y_reset()

* Resets y to y_min

