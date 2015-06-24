from html.parser import HTMLParser

f = open('test.html')
s = f.read()
parser=HTMLParser()
parser.feed(s)
