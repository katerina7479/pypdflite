# <a name="top"></a>Pypdflite Documentation

1. [Intro](index.html)
1. [Writer](writer.html)
2. [Document Object](document.html)
3. [Cursor Object](cursor.html)
4. [Color Object](#color)
    1. [Constructor](#construct)
    2. [Setters](#set)
    3. [Copy](#copy)
    4. [Color Reference](#ref)
5. [Tables](tables.html)
6. [Cell Formats](cellformat.html)

## <a name="color"></a>Color Object

PDF colors are stored by rbg. A generic PDFColor defaults to black if no
rbg value is entered.

There are 3 types of colors you can set in a document. Type, draw and fill. 
You should not have to worry about the types when working through the document
and writer.

## <a name="construct"></a>Constructor

### PDFColor(red=0, green=0, blue=0, name=None)

** Returns: ** PDFColor object

* **red (int): ** 
    * Must be between 0 - 255


* **green (int): ** 
    * Must be between 0 - 255


* **blue (int): ** 
    * Must be between 0 - 255

* **name (string): **
    * Set color from color reference.

*[top](#top)*

## <a name="set"></a>Setters

### color.set_color_by_name(name)

* **name (string): **
    * Must be a color from the color reference.

### color.set_color_by_number(red, green, blue)

* **red (int): ** 
    * Must be between 0 - 255


* **green (int): ** 
    * Must be between 0 - 255


* **blue (int): ** 
    * Must be between 0 - 255

## <a name="copy"></a>Copy Method

*[top](#top)*

### color.copy()

** Returns: ** PDFColor object

* Copies the color object.

*[top](#top)*

## <a name="ref"></a>Color Name Chart

Colors included for reference by name.

Name             | (r, g, b)
---------------- | --------------- 
'black'          | (0, 0, 0)
'red'            | (255, 0, 0)
'crimson'        | (220, 20, 60)
'pink'           | (255, 192, 203)
'plum'           | (205, 250, 205)
'purple'         | (128, 0, 128)
'violet'         | (148, 0, 211)
'indigo'         | (75, 0, 130)
'slateblue'      | (106, 90, 205)
'blue'           | (0, 0, 255)
'navy'           | (0, 0, 128)
'royalblue'      | (65, 105, 255)
'lightblue'      | (100, 149, 237)
'cornflowerblue' | (100, 149, 237)
'skyblue'        | (135, 206, 255)
'turquoise'      | (0, 245, 255)
'cyan'           | (0, 255, 255)
'green'          | (0, 255, 0)
'emerald'        | (0, 201, 87)
'cobalt'         | (61, 145, 64)
'darkgreen'      | (0, 100, 0)
'forestgreen'    | (34, 139, 34)
'darkolive'      | (85, 107, 47)
'ivory'          | (255, 255, 240)
'white'          | (255, 255, 255)
'beige'          | (245, 245, 220)
'olive'          | (128, 128, 0)
'yellow'         | (255, 255, 0)
'gold'           | (255, 215, 0)
'goldenrod'      | (218, 165, 32)
'orange'         | (255, 128, 0)
'eggshell'       | (252, 230, 201)
'tan'            | (210, 180, 140)
'peach'          | (255, 218, 185)
'chocolate'      | (139, 69, 19)
'burntsienna'    | (138, 54, 15)
'brown'          | (165, 42, 42)
'salmon'         | (255, 140, 105)
'gray'           | (128, 128, 128)
'lightgray'      | (211, 211, 211)
'darkgray'       | (105, 105, 105)
'maroon'         | (128, 0, 0)

*[top](#top)*
