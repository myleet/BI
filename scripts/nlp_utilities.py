def get_webtxt(url_address):
	import nltk
	from bs4 import BeautifulSoup
	from urllib import urlopen
	html   = urlopen(url_address).read()
	soup   = BeautifulSoup(html)
	print(soup.head)
	t = soup.title
	print(t)
url_address='https://www.bbc.com/news/world-us-canada-44999364'
keyword = 'Sulzberger'
get_webtxt(url_address)
