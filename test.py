from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from dataclasses import dataclass
from time import sleep

@dataclass
class Item:
    asin: str
    title: str
    price: str
    
links = []
skus = []

def get_html(page, url):
    page.goto(url)
    sleep(5)
    html = HTMLParser(page.content())
    parse_html(html, page)

def parse_html(html, page):
    
    for a_tag in html.css('a.product-title-link'):
        if 'href' in a_tag.attributes:
            links.append(a_tag.attributes['href'])
    
    check_for_more_pages(html, page)
    
    
def check_for_more_pages(html, page):
    a_tag = html.css_first('a.paging-next')
    if a_tag and 'href' in a_tag.attributes:
        href_value = a_tag.attributes['href']
        print("Moving on to next page")
        url = f'https://www.woolworths.com.au{href_value}'
        get_html(page, url)
    else:
        print("No more pages")
        return

def parse_sku():
    for link in links:
        sku = (link.split('details/'))
        sku = (sku[1].split('/')[0])
        print(sku)
        skus.append(sku)

def get_cookies():
    pass


def get_nutrition_data():
    pass

def run():
    search_term = 'bbq sauce'
    url = f"https://www.woolworths.com.au/shop/search/products?searchTerm={search_term}"    
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    get_html(page, url)
    print(links)
    parse_sku()
    get_nutrition_data()
    

def main():
    run()

if __name__ == "__main__":
    main()

