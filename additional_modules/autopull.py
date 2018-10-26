import requests
from bs4 import BeautifulSoup
import bs4

site = 'http://wired.com'
file = 'headlines.txt'
raw_html = requests.get(site).text
soup = BeautifulSoup(raw_html, 'html.parser')

def wired_magazine(count=10):
	headLines = []
	for a in soup.find_all('h5'):
		string = ''
		for b in a.contents:
			if type(b) ==  bs4.element.Tag:
				string += b.contents[0]
			else:
				string += b
		headLines.append(string)
	return headLines
#TODO: scrape major news networks

