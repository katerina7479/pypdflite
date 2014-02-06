pypdflite
=========

A lightweight utility for creating PDF files, written in Python

My intention is to use this to generate reports and set up automatice templates.
Decisions have a default, so it should be easy to get a report up
and running quickly.

The _test.py files in the bin folder show how the library can be implemented
in a program.

Text is flowable, and wrappable. Simply use document.add_text(), and the 
cursor will advance. I believe in most cases, the document will handle 
new pages appropriately, and you should not have to call new page.

Lines can be made with points, or by two cursor locations.

There is a reference list for colors, or you can create new ones, and
name them yourself.

Margins are set by default, or they can be changed. Default orientation is
portrait, 8.5 x 11.5, but the dimensions and orientation can be changed, per 
page or for the whole document.

Tables can be made, required format object (dictionary). Write cells 
individually, or by rows, or columns.

I have gotten PNG's and JPG's working for images. You add them, then use
document.draw_image(image). Add optional cursor, width or height specifications
to place and size.

Plans:
Online documentation

Thanks to: Marc Angelone, Noah Abelson, and John Lockwood for support and input!
Also: @klmitch for loading fonts on linux bug.