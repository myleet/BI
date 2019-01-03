import nltk
from   urllib import urlopen
from   bs4 import BeautifulSoup
# parser html docs
#1. soup = BeautifulSoup(html_doc, 'html.parser')
#2. soup = BeautifulSoup(markup, "xml")
#3. soup = BeautifulSoup(markup, "lxml")
#4. soup = BeautifulSoup(markup, "lxml-xml")
#5. soup = BeautifulSoup(markup, "html5lib)
# apt-get install python-html5lib
# easy_install html5lib
# pip install html5lib
# unicode
# source : 1. xml; 2. lxml; 3.html
# text file: 1.pdf ;  2. word;
url = "https://www.bbc.com/news/world-asia-45255321"

def parse_html(url_addr):
	html_doc = urlopen(url_addr).read()
	soup = BeautifulSoup(html_doc, 'html.parser')
	soup.title
	soup.title.string
	soup.a
	soup.find_all('a')
	soup.find(id="link3")
	for link in soup.find_all('a'):
		print(link.get('href'))
	print(soup.get_text())

from pyPdf import PdfFileWriter, PdfFileReader

def extract_words(input_object):
	text = u""
	content = input_object["/Contents"].getObject()
	if not isinstance(content, ContentStream):
		content = ContentStream(content, input_object.pdf)
	# Note: we check all strings are TextStringObjects.  ByteStringObjects
	# are strings where the byte->string encoding was unknown, so adding
	# them to the text here would be gibberish.
	for operands,operator in content.operations:
		if operator == "Tj":
			_text = operands[0]
			if isinstance(_text, TextStringObject):
				text += _text
		elif operator == "T*":
			text += "\n"
		elif operator == "'":
			text += "\n"
			_text = operands[0]
			if isinstance(_text, TextStringObject):
				text += operands[0]
		elif operator == '"':
			_text = operands[2]
			if isinstance(_text, TextStringObject):
				text += "\n"
				text += _text
		elif operator == "TJ":
			for i in operands[0]:
				if isinstance(i, TextStringObject):
					text += i
	return text

	
'''
parse_html(url)

from bs4.diagnose import diagnose
with open(url) as fp:
    data = fp.read()
diagnose(data)

import feedparser
llog = feedparser.parse("http://languagelog.ldc.upenn.edu/nll/?feed=atom")
llog['feed']['title']
'''

from pyPdf import PdfFileWriter, PdfFileReader
output = PdfFileWriter()
input1 = PdfFileReader(file("basic_unix.pdf", "rb"))
print "title = %s" % (input1.getDocumentInfo().title)
# print how many pages input1 has:
print "document1.pdf has %s pages." % input1.getNumPages()

# add page 1 from input1 to output document, unchanged
output.addPage(input1.getPage(0))

t = extract_characters(input1.getPage(1))
print(t)
exit()
# add page 2 from input1, but rotated clockwise 90 degrees
output.addPage(input1.getPage(1).rotateClockwise(90))

# add page 3 from input1, rotated the other way:
output.addPage(input1.getPage(2).rotateCounterClockwise(90))
# alt: output.addPage(input1.getPage(2).rotateClockwise(270))

# add page 4 from input1, but first add a watermark from another pdf:
page4 = input1.getPage(3)
watermark = PdfFileReader(file("unix1.pdf", "rb"))
page4.mergePage(watermark.getPage(0))

# add page 5 from input1, but crop it to half size:
page5 = input1.getPage(4)

output.addPage(page5)

# finally, write "output" to document-output.pdf
outputStream = file("document-output.pdf", "wb")
output.write(outputStream)
outputStream.close()