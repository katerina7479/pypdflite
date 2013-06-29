from datetime import datetime

from session import Session
from pdfdocument import PDFDocument


class PDFLite(object):
    "PDF Generation class"

    def __init__(self, filepath):
        self.filename = filepath

        self.SS = Session(self)
        self.D = PDFDocument(self.SS)

        # Full width display mode default
        self.set_display_mode()
        # Set default PDF version number
        self.pdf_version = '1.3'

        #Initialize PDF information
        self.setInformation()
        self.setCompression()

    def setCompression(self, value=False):
        self.SS.setCompression(value)

    def getDocument(self):
        return self.D

    def setInformation(self, title=None, subject=None, author=None, keywords=None, creator=None):
        testdict = {"title": title, "subject": subject, "author": author, "keywords": keywords, "creator": creator}

        for att, value in testdict.iteritems():
            if hasattr(self, att):
                if value is not None:
                    setattr(self, att, value)
                elif value is None:
                    pass
            else:
                setattr(self, att, None)

    def set_display_mode(self, zoom='fullwidth', layout='continuous'):
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
        #close document
        self._putheader()
        self._putpages()
        self._putresources()
        #Info
        self._putinfo()
        #Catalog
        self._putcatalog()
        #Cross-ref
        self._putcrossref()
        #Trailer
        self._puttrailer()
        self.output()

    def _putheader(self):
        self.SS.out('%%PDF-%s' % self.pdf_version)

    def _putpages(self):
        self.D._getOrientationChanges()
        self.D.outputPages()

        w = self.D.page.w
        h = self.D.page.h

        #Pages root
        self.SS.newobj(1)
        self.SS.out('<</Type /Pages')
        kids = '/Kids ['
        for i in xrange(0, len(self.D.pages)):
            kids += str(3 + 2*i) + ' 0 R '
        self.SS.out(kids + ']')
        self.SS.out('/Count %s' % len(self.D.pages))
        self.SS.out('/MediaBox [0 0 %.2f %.2f]' % (w, h))
        self.SS.out('>>')
        self.SS.out('endobj')

    def _putresources(self):
        self._putfonts()
        self._putimages()

        #Resource dictionary

        self._putresourcedict()

    def _putfonts(self):
        self.D.outputFonts()

    def _putimages(self):
        pass

    def _putresourcedict(self):
        self.SS.newobj(2)
        self.SS.out('<<')
        self.SS.out('/ProcSet [/PDF /Text /ImageB /ImageC /ImageI]')
        self.SS.out('/Font <<')
        for font in self.D.fonts:
            self.SS.out('/F' + str(font.index) + ' ' + str(font.number) + ' 0 R')
        self.SS.out('>>')
        self.SS.out('>>')
        self.SS.out('endobj')

    def _putinfo(self):
        self.SS.newobj()
        self.SS.out('<<')
        self.SS.out('/Producer '+self._textstring('PDFLite, https://github.com/katerina7479'))
        if self.title is not None:
            self.SS.out('/Title '+self._textstring(self.title))
        if self.subject is not None:
            self.SS.out('/Subject '+self._textstring(self.subject))
        if self.author is not None:
            self.SS.out('/Author '+self._textstring(self.author))
        if self.keywords is not None:
            self.SS.out('/Keywords '+self._textstring(self.keywords))
        if self.creator is not None:
            self.SS.out('/Creator '+self._textstring(self.creator))
        self.SS.out('/CreationDate '+self._textstring('D:'+datetime.now().strftime('%Y%m%d%H%M%S')))
        self.SS.out('>>')
        self.SS.out('endobj')

    def _putcatalog(self):
        self.SS.newobj()
        self.SS.out('<<')

        self.SS.out('/Type /Catalog')
        self.SS.out('/Pages 1 0 R')
        if(self.zoom_mode == 'fullpage'):
            self.SS.out('/OpenAction [3 0 R /Fit]')
        elif(self.zoom_mode == 'fullwidth'):
            self.SS.out('/OpenAction [3 0 R /FitH null]')
        elif(self.zoom_mode == 'real'):
            self.SS.out('/OpenAction [3 0 R /XYZ null null 1]')
        elif(not isinstance(self.zoom_mode, basestring)):
            self.SS.out('/OpenAction [3 0 R /XYZ null null '+(self.zoom_mode/100)+']')

        if(self.layout_mode == 'single'):
            self.SS.out('/PageLayout /SinglePage')
        elif(self.layout_mode == 'continuous'):
            self.SS.out('/PageLayout /OneColumn')
        elif(self.layout_mode == 'two'):
            self.SS.out('/PageLayout /TwoColumnLeft')
        self.SS.out('>>')
        self.SS.out('endobj')

    def _putcrossref(self):
        self.SS.out('xref')
        self.SS.out('0 %s' % len(self.SS.objects))
        self.SS.out('0000000000 65535 f ')
        for obj in self.SS.objects:
            if type(obj) == str:
                pass
            else:
                self.SS.out('%010d 00000 n ' % obj.offset)

    def _puttrailer(self):
        objnum = len(self.SS.objects)
        self.SS.out('trailer')
        self.SS.out('<<')
        self.SS.out('/Size %s' % objnum)
        self.SS.out('/Root %s 0 R' % (objnum-1))
        self.SS.out('/Info %s 0 R' % (objnum-2))
        self.SS.out('>>')
        self.SS.out('startxref')
        self.SS.out(len(self.SS.buffer))
        self.SS.out('%%EOF')

    def output(self):
        #Save to local file
        f = open(self.filename, 'wb')
        if(not f):
            raise Exception('Unable to create output file: ', self.filename)
        f.write(self.SS.buffer)
        f.close()

    def _textstring(self, text):
        if text is not None:
            for i, j in {"\\": "\\\\", ")": "\\)", "(": "\\("}.iteritems():
                text = text.replace(i, j)
            text = "(%s)" % text
        else:
            text = 'None'
        return text