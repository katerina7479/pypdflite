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
        self.target = self.commandlist
        self.datastring = ''
        self.openlist = False

    def handle_starttag(self, tag, attrs):
        self.datastring = self.strip(self.datastring)
        if tag in ['ul', 'ol']:
            self.target.append({'name': tag, 'attributes': attrs, 'elements': []})
            self.openlist = True
            self.target = self.target[-1]['elements']
        elif tag == 'li':
            self.target.append({'name': tag, 'attributes': attrs, 'elements': []})
        else:
            if self.datastring != '' and len(self.target) >= 1:
                self.target[-1]['data'] = self.datastring
                self.datastring = ''
            if self.openlist:
                self.target[-1]['elements'].append({'name': tag, 'attributes': attrs})
            else:
                self.target.append({'name': tag, 'attributes': attrs})

    def handle_data(self, data):
        data = self.strip(data)
        if data != '':
            self.datastring += data

    def handle_endtag(self, tag):
        if tag in ['span', 'a']:
            if not self.openlist:
                last = self.target[-2]
                self.target.append({'name': last['name'], 'attributes': last['attributes']})
                self.datastring = ''
        elif tag == 'p':
            self.datastring = self.strip(self.datastring)
            if self.datastring != '' and self.datastring != ' ':
                self.target[-1]['data'] = self.datastring
                self.datastring = ''
                self.target.append({'name': 'end'})
        elif tag == 'li':
            self.datastring = self.strip(self.datastring)
            if self.datastring != '':
                self.target[-1]['data'] = self.datastring
                self.datastring = ''
        elif tag in ['ul', 'ol']:
            self.openlist = False
            self.target = self.commandlist
        else:
            if self.datastring != '':
                self.target[-1]['data'] = self.datastring
                self.datastring = ''

    def get_commandlist(self):
        #for tag in self.commandlist:
        #    print tag
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
            if tag['name'] == 'ul':
                self.page.cursor.x_shift_left(10)
                if 'ul' in self.formats:
                    self.document.set_font(self.formats['ul'])

                char = chr(149)
                for atts in tag['attributes']:
                    if atts[0] == 'style':
                        if "list-style: none" in atts[1]:
                            char = ''
                        if "list-style-type: circle" in atts[1]:
                            char = chr(186)
                        if "list-style-type: square" in atts[1]:
                            char = chr(150)

                for element in tag['elements']:
                    self.set_list_element(element, char)

                self.document.add_newline()
                self.page.cursor.x_shift_left(-10)
            if tag['name'] == 'ol':
                self.page.cursor.x_shift_left(10)
                if 'ol' in self.formats:
                    self.document.set_font(self.formats['ol'])

                charlist = (n + 1 for n in range(0, 50))
                for att in tag['attributes']:
                    if att[0] == 'type':
                        if att[1] == 'a':
                            charlist = (chr(n) for n in range(97, 123))
                        if att[1] == 'A':
                            charlist = (chr(n) for n in range(65, 90))
                        if att[1] == 'I':
                            charlist = (self.to_Roman(n) for n in range(1, 50))
                        if att[1] == 'i':
                            charlist = (self.to_Roman(n).lower() for n in range(1, 50))

                for element in tag['elements']:
                    char = ''
                    if element['name'] == 'li':
                        char = charlist.next()
                        char = "%s. " % char
                    self.set_list_element(element, char)

                self.document.add_newline()
                self.page.cursor.x_shift_left(-10)

    def set_list_element(self, element, char):
        if element['name'] == 'li':
            if 'data' in element:
                self.document.add_text(char +' %s' % element['data'])
            if element['elements']:
                self._runlist(element['elements'])
            if 'data' in element:
                self.document.add_newline()
        else:
            if element['name'] != 'end':
                self.document.add_text(char)
                if isinstance(element, list):
                    self._runlist(element)
                elif isinstance(element, dict):
                    self._runlist([element])
                else:
                    pass

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

    def to_Roman(self, n):
        digits = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD' ),
            (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
            (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]

        result = ""
        while len(digits) > 0:
            (val, romn) = digits[0] # Unpacks the first pair in the list
            if n < val:
                digits.pop(0) # Removes first element
            else:
                n -= val
                result += romn
        return result
