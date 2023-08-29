from requests_html import HTMLSession
from bs4 import BeautifulSoup
import time

s = HTMLSession()
url = 'https://www.woolworths.com.au/shop/productdetails/270580/abe-s-bagels-natural-bagels'
# url = 'https://www.woolworths.com.au/shop/search/products?searchTerm=bread'


def getdata(url):
    r = s.get(url)
    #r.html.render(timeout=20)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def getnextpage(soup):
    # page = soup.findAll('a')
    page = soup.findAll('div', {'class': 'nutrition-table'})
    return page

soup = getdata(url)
print(getnextpage(soup))