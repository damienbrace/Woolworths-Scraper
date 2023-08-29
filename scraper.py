# Necessary imports
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# Path to your driver executable (this path is not used since you use ChromeDriverManager().install() later)
driver_path = '/utils/chromedriver.exe'

# Setting up the Chrome driver for Selenium
driver = webdriver.Chrome(ChromeDriverManager().install())

# Item we want to search on Woolworths
item_to_search = 'soup'

# Global flag to know when we have reached the last page. Not used in this code, but might be useful for future implementations.
last_page = False

# URL constructed with the search term
url = 'https://www.woolworths.com.au/shop/search/products?searchTerm=' + item_to_search

# List to store product links we find
product_links = []

# Function to get and parse the data from a given URL
def getdata(url):
    # Go to the provided URL
    driver.get(url)
    
    # Wait for a few seconds for the page to fully load
    sleep(5)
    
    # Get the page source HTML
    html = driver.page_source
    
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Get product links from the parsed HTML
    productlinks(soup)
    
# Function to find product links from the parsed HTML
def productlinks(soup):
    # Find all links with the class 'product-title-link' and iterate through them
    for link in soup.find_all('a', {'class': 'product-title-link'}):
        # Print the link's href attribute (the URL)
        print(link.get('href'))
        # Append the link to our global list
        product_links.append(link.get('href'))

    # Check if there is a "next page" link
    page_next = soup.find('a',{'class': 'paging-next'})
    if page_next != None:  # If a next page exists
        # Build the next page's URL and print it
        url = 'https://www.woolworths.com.au' + page_next.get('href')
        print(url)
        
        # Fetch data from the next page
        getdata(url)
    else: 
        # If no more pages, print the end message
        print('End of pages!')
        return

# Start the process by fetching data from the initial URL
getdata(url)

# Print all the product links we've found
print(product_links)
