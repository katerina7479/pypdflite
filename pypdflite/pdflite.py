from datetime import datetime

from session import _Session
from pdfdocument import PDFDocument


class PDFLite(object):
    """ PDF Generator, this class creates a document,
        session object, and creates the PDF outline.

        Has some overall pdf options to set, like
        the meta-data in Information (it won't print
        anywhere in the document, but can be seen in
        Properties, in Adobe reader.)

        When using this module, start by creating an
        instance of PDFLite, then request the document
        object with getDocument. Make your inputs to that
        object, and finish by closing through PDFLite.

    """

    def __init__(self, filepath):
        self.filepath = filepath

        self.session = _Session(self)
        self.document = PDFDocument(self.session)

        # Full width display mode default
        self.setDisplayMode()
        # Set default PDF version number
        self.pdf_version = '1.3'

        #Initialize PDF information
        self.set_information()
        self.set_compression()

    def set_compression(self, value=False):
        # False is easier to read with a text editor.
        self.session._set_compression(value)

    def getDocument(self):
        return self.document

    def set_information(self, title=None, subject=None, author=None, keywords=None, creator=None):
        """ Convinence function to add property info, can set any
            attribute and leave the others blank, it won't over-write
            previously set items, but to delete, you must set the attribute
            directly to None. (Since it is expected this will be in a generating
            program the likely-hood of such usage would be minimal.)

        """
        testdict = {"title": title, "subject": subject, "author": author, "keywords": keywords, "creator": creator}

        for att, value in testdict.iteritems():
            if hasattr(self, att):
                if value is not None:
                    setattr(self, att, value)
                elif value is None:
                    pass
            else:
                setattr(self, att, None)

    def setDisplayMode(self, zoom='fullpage', layout='continuous'):
        "Set display mode in viewer"
        self.zoom_options = ["fullpage", "fullwidth", "real", "default"]
        self.layout_options = ["single", "continuous", "two", "default"]

        if zoom in self.zoom_options:
            self.zoom_mode = zoom
        else:
            raise Exception('Incorrect zoom display mode: ' + zoom)

        if layout in self.layout_options:
            self.layout_mode = layout
        else:
            raise Exception('Incorrect layout display mode: ' + layout)

    def close(self):
        "Generate the document"
        # Places header, pages, page content first.
        self._putHeader()
        self._putPages()
        self._putResources()
        # Information object
        self._putInformation()
        # Catalog object
        self._putCatalog()
        # Cross-reference object
        self._putCrossReference()
        # Trailer object
        self._putTrailer()
        self._outputToFile()

    def _putHeader(self):
        "Standard first line"
        self.session._out('%%PDF-%s' % self.pdf_version)

    def _putPages(self):
        """ First, the Document object does the heavy-lifting for the
            individual page objects and content.

            Then, the overall "Pages" object is generated.

        """
        self.document._getOrientationChanges()
        self.document._outputPages()

        # Pages Object, provides reference to page objects (Kids list).
        self.session._addObject(1)
        self.session._out('<</Type /Pages')
        kids = '/Kids ['
        for i in xrange(0, len(self.document.pages)):
            kids += str(3 + 2*i) + ' 0 R '
        self.session._out(kids + ']')
        self.session._out('/Count %s' % len(self.document.pages))
        self.session._out('/MediaBox [0 0 %.2f %.2f]' % (self.document.page.width, self.document.page.height))  # Overal size of the default PDF page
        self.session._out('>>')
        self.SS._out('endobj')

    def _putResources(self):
        "Resource objects can be used several times, but are defined here."
        self._putFonts()
        self._putImages()

        #Resource dictionary
        self._putResourceDict()

    def _putFonts(self):
        "Fonts definitions objects."
        self.document._outputFonts()

    def _putImages(self):
        pass

    def _putResourceDict(self):
        "PDF reference to resource objects."
        self.SS._addObject(2)
        self.SS._out('<<')
        self.SS._out('/ProcSet [/PDF /Text /ImageB /ImageC /ImageI]')
        self.SS._out('/Font <<')
        for font in self.document.fonts:
            self.SS._out('/F' + str(font.index) + ' ' + str(font.number) + ' 0 R')
        self.SS._out('>>')
        self.SS._out('>>')
        self.SS._out('endobj')

    def _putInformation(self):
        "PDF Information object."
        self.SS._addObject()
        self.SS._out('<<')
        self.SS._out('/Producer '+self._textstring('PDFLite, https://github.com/katerina7479'))
        if self.title is not None:
            self.SS._out('/Title '+self._textstring(self.title))
        if self.subject is not None:
            self.SS._out('/Subject '+self._textstring(self.subject))
        if self.author is not None:
            self.SS._out('/Author '+self._textstring(self.author))
        if self.keywords is not None:
            self.SS._out('/Keywords '+self._textstring(self.keywords))
        if self.creator is not None:
            self.SS._out('/Creator '+self._textstring(self.creator))
        self.SS._out('/CreationDate '+self._textstring('D:'+datetime.now().strftime('%Y%m%d%H%M%S')))
        self.SS._out('>>')
        self.SS._out('endobj')

    def _putCatalog(self):
        "Catalog object."
        self.SS._addObject()
        self.SS._out('<<')

        self.SS._out('/Type /Catalog')
        self.SS._out('/Pages 1 0 R')
        if(self.zoom_mode == 'fullpage'):
            self.SS._out('/OpenAction [3 0 R /Fit]')
        elif(self.zoom_mode == 'fullwidth'):
            self.SS._out('/OpenAction [3 0 R /FitH null]')
        elif(self.zoom_mode == 'real'):
            self.SS._out('/OpenAction [3 0 R /XYZ null null 1]')
        elif(not isinstance(self.zoom_mode, basestring)):
            self.SS._out('/OpenAction [3 0 R /XYZ null null '+(self.zoom_mode/100)+']')

        if(self.layout_mode == 'single'):
            self.SS._out('/PageLayout /SinglePage')
        elif(self.layout_mode == 'continuous'):
            self.SS._out('/PageLayout /OneColumn')
        elif(self.layout_mode == 'two'):
            self.SS._out('/PageLayout /TwoColumnLeft')
        self.SS._out('>>')
        self.SS._out('endobj')

    def _putCrossReference(self):
        """ Cross Reference Object, calculates
            the position in bytes to the start
            (first number) of each object in
            order by number (zero is special)
            from the begining of the file.

        """
        self.SS._out('xref')
        self.SS._out('0 %s' % len(self.SS.objects))
        self.SS._out('0000000000 65535 f ')
        for obj in self.SS.objects:
            if isinstance(obj, basestring):
                pass
            else:
                self.SS._out('%010d 00000 n ' % obj.offset)

    def _putTrailer(self):
        """ Final Trailer calculations, and EOF
            reference.

        """
        objnum = len(self.SS.objects)
        self.SS._out('trailer')
        self.SS._out('<<')
        self.SS._out('/Size %s' % objnum)
        self.SS._out('/Root %s 0 R' % (objnum-1))
        self.SS._out('/Info %s 0 R' % (objnum-2))
        self.SS._out('>>')
        self.SS._out('startxref')
        self.SS._out(len(self.SS.buffer))
        self.SS._out('%%EOF')

    def _outputToFile(self):
        """ Save to filepath specified on
            init. (Will throw an error if
            the document is already open).

        """
        f = open(self.filepath, 'wb')
        if(not f):
            raise Exception('Unable to create output file: ', self.filepath)
        f.write(self.SS.buffer)
        f.close()

    def _textstring(self, text):
        """ Provides for escape characters and converting to
            pdf text object (pdf strings are in parantheses).
            Mainly for use in the information block here, this
            functionality is replicated elsewhere.

        """
        if text is not None:
            for i, j in {"\\": "\\\\", ")": "\\)", "(": "\\("}.iteritems():
                text = text.replace(i, j)
            text = "(%s)" % text
        else:
            text = 'None'
        return text