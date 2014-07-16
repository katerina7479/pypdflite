import re
from HTMLParser import HTMLParser
from pdfcolor import PDFColor
from pdffont import PDFFont
from pdftext import PDFText


class Element(object):
    def __init__(self):
        pass

    def save_data(self, value):
        if hasattr(self, 'data'):
            self.data.append(value)

    def add_element(self, obj):
        if hasattr(self, 'element'):
            self.element.append(obj)

    def set_dependancies(self, session, document, formats, context):
        self.session = session
        self.document = document
        self.formats = formats
        self.context = context

    def output(self):
        pass

    def _parse_atts(self, atts):
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

    def _set_attr(self, font, color):
        if font is not None:
            self.document.set_font(font=font)
        if color is not None:
            self.document.set_text_color(color)


class Header(Element):
    def __init__(self, name, attr=None):
        super(Header, self).__init__()
        self.name = name
        self.attributes = attr
        self.data = []

    def output(self):
        save_font = self.document.get_font()
        self.document.set_font(self.formats[self.name])
        if self.attributes is not None:
            font, color, variable = self._parse_atts(self.attributes)
            self._set_attr(font, color)
        for text in self.data:
            self.document.add_text('%s' % text)
        self.document.add_newline()
        self.document.set_font(font=save_font)


class Paragraph(Element):
    def __init__(self, attr=None):
        super(Paragraph, self).__init__()
        self.name = 'p'
        self.attributes = attr
        self.data = []
        self.elements = []

    def output(self):
        self.document.set_font(self.formats['p'])
        if self.attributes is not None:
            font, color, variable = self._parse_atts(self.attributes)
            self._set_attr(font, color)
        span_index = 0
        for text in self.data:
            if text == '%span%':
                span = self.elements[span_index]
                span.set_dependancies(self.session, self.document, self.formats, self.context)
                span.output()
                span_index += 1
            else:
                self.document.add_text('%s' % text)
        self.document.add_newline(1)


class Break(Element):
    def __init__(self):
        super(Break, self).__init__()
        self.name = 'br'

    def output(self):
        self.document.add_newline()


class UnorderedList(Element):
    def __init__(self, attr=None):
        super(UnorderedList, self).__init__()
        self.name = 'ul'
        self.attributes = attr
        self.elements = []
        self.primary_list = True

    def set_bullet_format(self):
        self.char = chr(149)
        if self.attributes is not None:
            for atts in self.attributes:
                if atts[0] == 'style':
                    if "list-style: none" in atts[1]:
                        self.char = ''
                    if "list-style-type: circle" in atts[1]:
                        self.char = chr(186)
                    if "list-style-type: square" in atts[1]:
                        self.char = chr(150)

    def _output_element(self, item):
        item.set_dependancies(self.session, self.document, self.formats, self.context)
        item.output(self.char)

    def output(self):
        self.set_bullet_format()
        self.document.page.cursor.x_shift_left(10)
        if 'ul' in self.formats:
            self.document.set_font(self.formats['ul'])
        if self.attributes is not None:
            font, color, variable = self._parse_atts(self.attributes)
            self._set_attr(font, color)
        for item in self.elements[:-1]:
            self._output_element(item)
            self.document.add_newline()
        self._output_element(self.elements[-1])
        if self.primary_list:
            self.document.add_newline()
        self.document.page.cursor.x_shift_left(-10)


class OrderedList(Element):
    def __init__(self, attr=None):
        super(OrderedList, self).__init__()
        self.name = 'ol'
        self.attributes = attr
        self.elements = []
        self.primary_list = True

    def set_bullet_format(self):
        self.charlist = (n + 1 for n in range(0, 50))
        if self.attributes is not None:
            for att in self.attributes:
                if att[0] == 'type':
                    if att[1] == 'a':
                        self.charlist = (chr(n) for n in range(97, 123))
                    if att[1] == 'A':
                        self.charlist = (chr(n) for n in range(65, 90))
                    if att[1] == 'I':
                        self.charlist = (self._to_Roman(n) for n in range(1, 50))
                    if att[1] == 'i':
                        self.charlist = (self._to_Roman(n).lower() for n in range(1, 50))

    def _output_element(self, item, char):
        if char is None:
            char = '%s. ' % self.charlist.next()
        item.set_dependancies(self.session, self.document, self.formats, self.context)
        char = item.output(char)
        return char

    def output(self):
        self.document.page.cursor.x_shift_left(10)
        if 'ol' in self.formats:
            self.document.set_font(self.formats['ol'])
        if self.attributes is not None:
            font, color, variable = self._parse_atts(self.attributes)
            self._set_attr(font, color)
        self.set_bullet_format()

        self.elements[-1].last = True
        char = None
        for item in self.elements[:-1]:
            char = self._output_element(item, char)
            self.document.add_newline()
        self._output_element(self.elements[-1], char)
        if self.primary_list:
            self.document.add_newline()
        self.document.page.cursor.x_shift_left(-10)

    def _to_Roman(self, n):
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


class ListElement(Element):
    def __init__(self, attr=None):
        super(ListElement, self).__init__()
        self.name = 'li'
        self.attributes = attr
        self.elements = []
        self.data = []
        self.spans = []

    def set_spans(self):
        for item in self.elements:
            if item.name == 'span':
                self.spans.append(item)

    def output(self, char):
        if 'li' in self.formats:
            self.document.set_font(self.formats['li'])
        if self.attributes is not None:
            font, color, variable = self._parse_atts(self.attributes)
            self._set_attr(font, color)
        self.set_spans()
        span_index = 0
        for text in self.data:
            if text == '%span%':
                span = self.spans[span_index]
                span.set_dependancies(self.session, self.document, self.formats, self.context)
                span.output()
                span_index += 1
            else:
                if char is not None:
                    self.document.add_text('%s' % char)
                self.document.add_text(' %s' % text)
                char = None
        for element in self.elements:
            if element.name != 'span':
                if element.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    if char is not None:
                        self.document.add_text(char)
                        char = None
                if element.name in ['ul', 'ol']:
                    element.primary_list = False
                element.set_dependancies(self.session, self.document, self.formats, self.context)
                element.output()
        return char


class Span(Element):
    def __init__(self, attr=None):
        super(Span, self).__init__()
        self.name = 'span'
        self.attributes = attr

    def output(self):
        savefont = self.document.get_font()
        font, color, variable = self._parse_atts(self.attributes)
        if variable is not None:
            PDFText(self.session, self.document.page, '%s' % variable, font, color, self.document.page.cursor)
        self.document.set_font(font=savefont)


class Blockquote(Element):
    def __init__(self):
        super(Blockquote, self).__init__()
        self.name = 'blockquote'
        self.data = []

    def output(self):
        self.document.add_newline(2)
        self.document.page.cursor.x_shift_left(20)
        if 'blockquote' in self.formats:
            self.document.set_font(self.formats['blockquote'])
        else:
            self.document.set_font(self.formats['p'])
        for text in self.data:
            self.document.add_text('%s' % text)
        self.document.page.cursor.x_shift_left(-20)
        self.document.add_newline()


class Link(Element):
    def __init__(self, attr=None):
        super(Link, self).__init__()
        self.name = 'a'
        self.attributes = attr


class PDFHTMLParser(HTMLParser):
    def __init__(self):
        # HTMLParser is old-style class
        HTMLParser.__init__(self)
        self.commandlist = []
        self.target = self.commandlist
        self.last_target = []
        self.data_target = None
        self.datastring = ''

    def save_target(self):
        self.last_target.append(self.target)

    def handle_starttag(self, tag, attrs):
        if attrs == '' or attrs == []:
            attrs = None
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.reset_data()
            header = Header(tag, attrs)
            self.target.append(header)
            self.data_target = header
        if tag == 'br':
            br = Break()
            self.target.append(br)
        if tag == 'p':
            para = Paragraph(attrs)
            self.target.append(para)
            self.data_target = para
            self.save_target()
            self.target = para.elements
        if tag == 'span':
            span = Span(attrs)
            self.target.append(span)
            self.data_target.save_data('%span%')
        if tag == 'ul':
            unlist = UnorderedList(attrs)
            self.target.append(unlist)
            self.save_target()
            self.target = unlist.elements
        if tag == 'ol':
            orlist = OrderedList(attrs)
            self.target.append(orlist)
            self.save_target()
            self.target = orlist.elements
        if tag == 'li':
            listel = ListElement(attrs)
            self.target.append(listel)
            self.data_target = listel
            self.save_target()
            self.target = listel.elements
        if tag == 'blockquote':
            block = Blockquote()
            self.target.append(block)
            self.data_target = block
        if tag == 'a':
            link = Link()
            self.last_data_target = self.data_target
            self.data_target = link

    def handle_data(self, data):
        data = self.strip(data)
        if data != '':
            if self.data_target is not None:
                self.data_target.save_data(data)

    def reset_data(self):
        self.datastring = ''

    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.data_target = None
        if tag == 'p':
            self.target = self.last_target.pop()
            self.data_target = None
        if tag == 'ul' or tag == 'ol':
            self.target = self.last_target.pop()
            self.data_target = None
        if tag == 'li':
            self.target = self.last_target.pop()
            self.data_target = None
        if tag == 'blockquote':
            self.data_target = None
        if tag == 'a':
            self.data_target = self.last_data_target
            self.last_data_target = None

    def get_commandlist(self):
        return self.commandlist

    def strip(self, mystring):
        return re.sub("\s\s+" , " ", mystring.strip())


class PDFHtml(object):
    def __init__(self, parent, session, htmltext, formats=None, context=None):
        self.document = parent
        self.session = session
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
        for item in mylist:
            item.set_dependancies(self.session, self.document, self.formats, self.context)
            item.output()
