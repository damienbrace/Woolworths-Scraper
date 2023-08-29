from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# Path to your driver executable
driver_path = '/utils/chromedriver.exe'

driver = webdriver.Chrome(ChromeDriverManager().install())

item_to_search = 'bread'



last_page = False
page = 'https://www.woolworths.com.au/shop/search/products?searchTerm=' + item_to_search
product_links = []

while last_page != True:
    # Go to the webpage
    driver.get(page)

    # Wait some time for the page to fully load
    sleep(5)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find_all('a', {'class': 'product-title-link'}):
        print(link.get('href'))
        product_links.append(link.get('href'))

    page_next = soup.find('a',{'class': 'paging-next'})
    while page_next != None:
        page = 'https://www.woolworths.com.au' + page_next.get('href')
        print(page)
        break
        

    else: 
        print('End of pages!')
        last_page = True

    print(product_links)















# Wait for some time for the page to fully load
#





#print(meal_elements)

# Get the source of the webpage






# <span _ngcontent-serverapp-c131="" class="cartControls-addCart"> Add to cart </span>