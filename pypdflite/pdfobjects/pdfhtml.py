from HTMLParser import HTMLParser


class PDFHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Start Tag: ", tag, " Atts: ", attrs

    def handle_endtag(self, tag):
        print "Endtag: ", tag

    def handle_data(self, data):
        print "Data: ", data


class PDFHtml(object):
    def __init__(self, parent, session, page, htmltext, cursor, formats=None, context=None):
        self.session = session
        self.parent = parent
        self.htmltext = htmltext
        self.context = {}
        if isinstance(context, dict):
            self.context = context
        self.formats = {}
        if isinstance(formats, dict):
            self.formats = formats
        self.parser = PDFHTMLParser()
        self._parsehtml()

    def _parsehtml(self):
        self.parser.feed(self.htmltext)