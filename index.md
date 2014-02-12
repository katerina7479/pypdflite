---
layout: default

---
# <a name="intro"></a>PyPDFlite
PyPDFlite is a simple PDF writer, written in Python, to help generate PDF files
in your code.

No more messing with cursors, colors, and fonts for a simple report. Customize 
only when you need to, in Python!


1. [Intro](#intro)
    1. [Install](#install)
    2. [Getting Started](#hello)
    3. [Further](#further)
    4. [About](#about)
    5. [Contact](#support)
1. [Writer](writer.html)
2. [Document Object](document.html)
3. [Cursor Object](cursor.html)
4. [Color Object](color.html)
5. [Tables](tables.html)
6. [Cell Formats](cellformat.html)


# <a name="install"></a>Installing

## Install with pip

```
$ pip install pypdflite

```

## Get from github

Checkout the [github repository](https://github.com/katerina7479/pypdflite).

# <a name="hello"></a>Getting Started
All you need installed is Python (2.7), and pypdflite, and you can get started
making great reports. Here's a "Hello World" example. Just open a new file
in your favorite text editor, and save it as "hello.py".

*hello.py*

```
from pypdflite import PDFLite

def main():
    writer = PDFLite("hello.pdf")
    writer.set_information(title="Hello World!")
    document = writer.get_document()
    document.add_text("Hello World!")
    writer.close()

if __name__ == '__main__':
    main()
```
Then in your console, go to the folder with hello.py and run:

```
my_folder$ python hello.py
```
Your hello.pdf file will be generated!


# <a name="further"></a>Ready to Dive in further?
Browse the [Documentation](writer.html). 


# <a name="about"></a>Authors and Contributors
I'm @katerina7479. I started programming in python to help me with my job,
and ended up becoming a full-fledged software engineer! I do want to thank
@johnlockwood, and the people at ShareRoot for their help and support!


# <a name="contact"></a>Support or Contact
Having trouble with PyPDFlite?

It's still a work in progress, and there are frequent updates. 

*Try:*

```
$ pip install -U pypdflite
```

Or, add an issue on [github/issues](https://github.com/katerina7479/pypdflite/issues).
