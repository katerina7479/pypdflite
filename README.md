pypdflite
=========

A lightweight utility for creating PDF files, written in Python

My intention was to use this to generate reports, and set up templates.
Most decisions have a default, so it should be easy to get a report up
and running.

The _test.py files in the top folder show how the library in
the pypdflite folder might be implemented in a program.

Text is flowable, wrappable. Simply use document.add_text(), and the 
cursor will advance. I believe in most cases, the document will handle 
new pages appropriately, and you should not have to call new page.

Lines can be made with points, or by two cursor locations.

There is a reference list for colors, but you can create new ones, and
name them yourself.

Margins are set by default, but can be changed. Default orientation is portrait,
and 8.5 x 11.5, but the dimensions and orientation can be changed.

Tables can be made. Assumes a list of lists, where each list is a row. There
is a flag for if it's columns.

I have gotten PNG's working for images.

There are also lists with bullets

It will require a one time setup to load font files.
There is a load_fonts.py script that should be run. You can specify a
different font folder, or it will try to search for system fonts.
