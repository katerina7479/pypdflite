from datetime import datetime
from font_loader import Font_Loader
from session import _Session
from .pdfdocument import PDFDocument


class PDFLite(object):

    """ PDF generator, this class creates a document,
        session object, and the PDF outline.

        There are some overall pdf options to set, like
        the meta-data in information (this won't print
        anywhere in the document, but can be seen in
        Properties, in Adobe reader.)

        When using this module, start by creating an
        instance of PDFLite, then request the document
        object with get_document. Make your inputs to that
        object, and finish by closing the PDFLite.

    """

    def __init__(self, filepath, orientation="P", layout="letter", font_list=None, font_dir=None):
        if font_dir is not None:
            Font_Loader.load_from_dir(font_dir)
        elif font_list is not None:
            Font_Loader.load_from_list(font_list)
        else:
            Font_Loader.load_fonts()

        self.filepath = filepath
        self.destination = None

        if hasattr(self.filepath, 'write'):
            self.destination = self.filepath
        elif self.filepath == 'string':
            self.destination = 'string'

        # Create session and document objects
        self.session = _Session(self)
        self.document = PDFDocument(self.session, orientation, layout)

        # Full width display mode default
        self.set_display_mode()
        # Set default PDF version number
        self.pdf_version = '1.7'

        # Initialize PDF information
        self.set_information()
        self.set_compression()

    def set_compression(self, value=False):
        # False is easier to read with a text editor.
        self.session._set_compression(value)

    def get_document(self):
        return self.document

    def set_information(self, title=None, subject=None, author=None,
                        keywords=None, creator=None):
        """ Convenience function to add property info, can set any
            attribute and leave the others blank, it won't over-write
            previously set items, but to delete, you must set the attribute
            directly to None. (It is expected that there should be only
            rare need to delete set data.)

        """
        info_dict = {"title": title, "subject": subject,
                     "author": author, "keywords": keywords,
                     "creator": creator}

        for att, value in info_dict.iteritems():
            if hasattr(self, att):
                if value:
                    setattr(self, att, value)
            else:
                setattr(self, att, None)

    def set_display_mode(self, zoom='fullpage', layout='continuous'):
        """ Set the default viewing options.

        """
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
        """ Prompt the objects to output pdf code, and save to file.

        """
        self.document._set_page_numbers()
        # Places header, pages, page content first.
        self._put_header()
        self._put_pages()
        self._put_resources()
        # Information object
        self._put_information()
        # Catalog object
        self._put_catalog()
        # Cross-reference object
        self._put_cross_reference()
        # Trailer object
        self._put_trailer()

        if hasattr(self.destination, "write"):
            output = self._output_to_io()
        elif self.destination == 'string':
            output = self._output_to_string()
        else:
            self._output_to_file()
            output = None
        return output

    # Font loading helpers
    def load_fonts(self):
        load_fonts.load_fonts()

    def remove_fonts(self):
        load_fonts.remove_fonts()

    # Private Methods for building the PDF
    def _put_header(self):
        " Standard first line in a PDF. "
        self.session._out('%%PDF-%s' % self.pdf_version)

    def _put_pages(self):
        """ First, the Document object does the heavy-lifting for the
            individual page objects and content.

            Then, the overall "Pages" object is generated.

        """
        self.document._get_orientation_changes()
        self.document._output_pages()

        # Pages Object, provides reference to page objects (Kids list).
        self.session._add_object(1)
        self.session._out('<</Type /Pages')
        kids = '/Kids ['
        for i in xrange(0, len(self.document.pages)):
            kids += str(3 + 2 * i) + ' 0 R '
        self.session._out(kids + ']')
        self.session._out('/Count %s' % len(self.document.pages))

        # Overall size of the default PDF page
        self.session._out('/MediaBox [0 0 %.2f %.2f]' %
                          (self.document.page.width,
                           self.document.page.height))
        self.session._out('>>')
        self.session._out('endobj')

    def _put_resources(self):
        """ Resource objects can be used several times throughout the document,
        but the pdf code defining them are all defined here.

        """
        self._put_fonts()
        self._put_images()

        # Resource dictionary
        self._put_resource_dict()

    def _put_fonts(self):
        """ Fonts definitions objects.

        """
        self.document._output_fonts()

    def _put_images(self):
        """ Image definition objects.

        """
        self.document._output_images()

    def _put_resource_dict(self):
        """ Creates PDF reference to resource objects.

        """
        self.session._add_object(2)
        self.session._out('<<')
        self.session._out('/ProcSet [/PDF /Text /ImageB /ImageC /ImageI]')
        self.session._out('/Font <<')
        for font in self.document.fonts:
            self.session._out('/F%s %s 0 R' % (font.index, font.number))
        self.session._out('>>')
        if self.document.images:
            self.session._out('/XObject <<')
            for image in self.document.images:
                self.session._out('/I%s %s 0 R' % (image.index, image.number))
            self.session._out('>>')
        self.session._out('>>')
        self.session._out('endobj')

    def _put_information(self):
        "PDF Information object."
        self.session._add_object()
        self.session._out('<<')
        self.session._out('/Producer ' + self._text_to_string(
            'PDFLite, https://github.com/katerina7479'))
        if self.title:
            self.session._out('/Title ' + self._text_to_string(self.title))
        if self.subject:
            self.session._out('/Subject ' + self._text_to_string(self.subject))
        if self.author:
            self.session._out('/Author ' + self._text_to_string(self.author))
        if self.keywords:
            self.session._out('/Keywords ' +
                              self._text_to_string(self.keywords))
        if self.creator:
            self.session._out('/Creator ' + self._text_to_string(self.creator))
        self.session._out('/CreationDate ' + self._text_to_string(
            'D:' + datetime.now().strftime('%Y%m%d%H%M%S')))
        self.session._out('>>')
        self.session._out('endobj')

    def _put_catalog(self):
        "Catalog object."
        self.session._add_object()
        self.session._out('<<')

        self.session._out('/Type /Catalog')
        self.session._out('/Pages 1 0 R')
        if(self.zoom_mode == 'fullpage'):
            self.session._out('/OpenAction [3 0 R /Fit]')
        elif(self.zoom_mode == 'fullwidth'):
            self.session._out('/OpenAction [3 0 R /FitH null]')
        elif(self.zoom_mode == 'real'):
            self.session._out('/OpenAction [3 0 R /XYZ null null 1]')
        elif(not isinstance(self.zoom_mode, basestring)):
            self.session._out(
                '/OpenAction [3 0 R /XYZ null null ' +
                (self.zoom_mode / 100) + ']')

        if(self.layout_mode == 'single'):
            self.session._out('/PageLayout /SinglePage')
        elif(self.layout_mode == 'continuous'):
            self.session._out('/PageLayout /OneColumn')
        elif(self.layout_mode == 'two'):
            self.session._out('/PageLayout /TwoColumnLeft')
        self.session._out('>>')
        self.session._out('endobj')

    def _put_cross_reference(self):
        """ Cross Reference Object, calculates
            the position in bytes to the start
            (first number) of each object in
            order by number (zero is special)
            from the begining of the file.

        """
        self.session._out('xref')
        self.session._out('0 %s' % len(self.session.objects))
        self.session._out('0000000000 65535 f ')
        for obj in self.session.objects:
            if isinstance(obj, basestring):
                pass
            else:
                self.session._out('%010d 00000 n ' % obj.offset)

    def _put_trailer(self):
        """ Final Trailer calculations, and ebd-of-file
            reference.

        """
        objnum = len(self.session.objects)
        self.session._out('trailer')
        self.session._out('<<')
        self.session._out('/Size %s' % objnum)
        self.session._out('/Root %s 0 R' % (objnum - 1))
        self.session._out('/Info %s 0 R' % (objnum - 2))
        self.session._out('>>')
        self.session._out('startxref')
        self.session._out(len(self.session.buffer))
        self.session._out('%%EOF')

    def _output_to_file(self):
        """ Save to filepath specified on
            init. (Will throw an error if
            the document is already open).

        """
        f = open(self.filepath, 'wb')
        if not f:
            raise Exception('Unable to create output file: ', self.filepath)
        f.write(self.session.buffer)
        f.close()

    def _output_to_string(self):
        return self.session.buffer

    def _output_to_io(self):
        self.destination.write(self.session.buffer)
        return self.destination

    def _text_to_string(self, text):
        """ Provides for escape characters and converting to
            pdf text object (pdf strings are in parantheses).
            Mainly for use in the information block here, this
            functionality is also present in the text object.

        """
        if text:
            for i, j in {"\\": "\\\\", ")": "\\)", "(": "\\("}.iteritems():
                text = text.replace(i, j)
            text = "(%s)" % text
        else:
            text = 'None'
        return text
