import requests
from bs4 import BeautifulSoup

url = 'https://www.woolworths.com.au/shop/search/products?searchTerm=bread'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

print(soup)