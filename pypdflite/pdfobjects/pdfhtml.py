import re
from HTMLParser import HTMLParser
from pdfcolor import PDFColor
from pdffont import PDFFont
from pdftext import PDFText


class PDFHTMLParser(HTMLParser):
    def __init__(self):
        # HTMLParser is old-style class
        HTMLParser.__init__(self)
        self.commandlist = []
        self.datastring = ''
        self.openlist = False

    def handle_starttag(self, tag, attrs):
        if tag in ["ul", 'ol']:
            self.openlist = True
            self.commandlist.append({'name': tag, 'attributes': attrs, 'elements': []})
        elif tag == 'li':
            self.commandlist[-1]['elements'].append({'name': tag, 'attributes': attrs, 'elements': []})
        elif self.openlist:
            if self.datastring != '' and len(self.commandlist[-1]['elements']) >= 1:
                self.commandlist[-1]['elements'][-1]['data'] = self.strip(self.datastring)
                self.datastring = ''
            self.commandlist[-1]['elements'][-1]['elements'].append({'name': tag, 'attributes': attrs})
        else:
            self.datastring = self.strip(self.datastring)

            if self.datastring != '' and len(self.commandlist) >= 1:
                self.commandlist[-1]['data'] = self.datastring
                self.datastring = ''
            self.commandlist.append({'name': tag, 'attributes': attrs})


    def handle_data(self, data):
        data = self.strip(data)
        if data != '':
            self.datastring += data

    def handle_endtag(self, tag):
        if tag == 'span':
            if not self.openlist:
                last = self.commandlist[-2]
                self.commandlist.append({'name': last['name'], 'attributes': last['attributes']})
                self.datastring = ''

        if tag == 'p':
            self.datastring = self.strip(self.datastring)
            if self.datastring != '' and self.datastring != ' ':
                if not self.openlist:
                    target = self.commandlist
                else:
                    target = self.commandlist[-1]['elements']

                target[-1]['data'] = self.datastring
                self.datastring = ''
                target.append({'name': 'end'})
        if tag == 'li':
            self.datastring = self.strip(self.datastring)
            if self.datastring != '':
                self.commandlist[-1]['elements'][-1]['data'] = self.datastring
                self.datastring = ''
        if tag in ['ul', 'ol']:
            self.openlist = False
        else:
            if self.datastring != '':
                self.commandlist[-1]['data'] = self.datastring
                self.datastring = ''

    def get_commandlist(self):
        return self.commandlist

    def strip(self, mystring):
        return re.sub("\s\s+" , " ", mystring.strip())


class PDFHtml(object):
    def __init__(self, parent, session, page, htmltext, formats=None, context=None):
        self.document = parent
        self.session = session
        self.page = page
        self.htmltext = str(htmltext)
        self.context = {}
        if isinstance(context, dict):
            self.context = context
        self.formats = {}
        if isinstance(formats, dict):
            self.formats = formats
        self._parsehtml()
        self._runlist(self.commandlist)

    def _parsehtml(self):
        parser = PDFHTMLParser()
        parser.feed(self.htmltext)
        self.commandlist = parser.get_commandlist()

    def _runlist(self, mylist):
        for tag in mylist:
            if tag['name'] in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                self.document.set_font(self.formats[tag['name']])
                self.document.add_text('%s' % tag['data'])
                self.document.add_newline()
            elif tag['name'] == 'p':
                if 'data' in tag:
                    self.document.set_font(self.formats['p'])
                    self.document.add_text('%s' % tag['data'])
            elif tag['name'] == 'end' or tag['name'] == 'br':
                self.document.add_newline()
            elif tag['name'] == 'span':
                savefont = self.document.get_font()
                font, color, variable = self.parse_atts(tag['attributes'])
                if variable is not None:
                    PDFText(self.session, self.page, '%s' % variable, font, color, self.page.cursor)
                    self.document.set_font(savefont)
            if tag['name'] in ['ul']:
                self.page.cursor.x_shift_left(10)
                bullet_code = 149
                char = chr(bullet_code)
                if 'ul' in self.formats:
                    self.document.set_font(self.formats['ul'])
                for element in tag['elements']:
                    if element['name'] == 'li':
                        if 'data' in element:
                            self.document.add_text(char +' %s' % element['data'])
                        if element['elements']:
                            self._runlist(element['elements'])
                        self.document.add_newline(1)
                    else:
                        if element['name'] == 'end':
                            pass
                        else:
                            self.document.add_text(char)
                            self._runlist(element)
                self.document.add_newline()
                self.page.cursor.x_shift_left(-10)

    def parse_atts(self, atts):
        formats = []
        font = None
        color = None
        variable = None
        for item in atts:
            if item[0] == 'class':
                formats = item[1].split(' ')
            elif item[0] == 'data-bind':
                variable = self.context[item[1]]

        for key in formats:
            if key in self.formats:
                value = self.formats[key]
                if isinstance(value, PDFFont):
                    font = value
                if isinstance(value, PDFColor):
                    color = value
        return font, color, variable

