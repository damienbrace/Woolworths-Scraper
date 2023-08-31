# Necessary imports
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import requests
import json



# Item we want to search on Woolworths
item_to_search = 'baked beans'
url = 'https://www.woolworths.com.au/shop/search/products?searchTerm=' + item_to_search

driver_path = '/utils/chromedriver.exe'
driver = webdriver.Chrome(ChromeDriverManager().install())


# List to store product links we find
product_links = []

# Function to get and parse the data from a given URL
def getdata(url):
    # Path to your driver executable (this path is not used since you use ChromeDriverManager().install() later)
    driver.get(url)
    sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    productlinks(soup)
    
# Function to find product links from the parsed HTML
def productlinks(soup):
    for link in soup.find_all('a', {'class': 'product-title-link'}):
        sku = (link.get('href').split('details/'))
        sku = (sku[1].split('/')[0])
        print(sku)
        product_links.append(sku)

    # Check if there is a "next page" link
    page_next = soup.find('a',{'class': 'paging-next'})
    if page_next != None:  
        url = 'https://www.woolworths.com.au' + page_next.get('href')
        print(url)
        getdata(url)
    else: 
        print('End of pages!')
        return
    

def loop_through_items(product_links):
    for sku in product_links:
        get_item_info(sku)

def get_item_info(sku):
# fetch html or api data
    url = "https://www.woolworths.com.au/apis/ui/product/detail/" + sku + "?isMobile=false&useVariant=true"

    payload = {}
    headers = {
    'authority': 'www.woolworths.com.au',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'bff_region=syd2; akaalb_woolworths.com.au=~op=www_woolworths_com_au_ZoneA:PROD-ZoneA|www_woolworths_com_au_BFF_SYD_Launch:WOW-BFF-SYD2|~rv=63~m=PROD-ZoneA:0|WOW-BFF-SYD2:0|~os=43eb3391333cc20efbd7f812851447e6~id=96fc23683242148ddfff94804400abcf; rxVisitor=16932172888531TO2ANNM943UA11P10AC056CCJPOJH38; at_check=true; INGRESSCOOKIE=1693217291.902.82.593444|37206e05370eb151ee9f1b6a1c80a538; AMCVS_4353388057AC8D357F000101%40AdobeOrg=1; ai_user=7FCgAky/7XjcPJJ/uXasRb|2023-08-28T10:08:10.301Z; dtCookie=v_4_srv_5_sn_GUV1Q4KUGLPOSLB6BP0RHKDTKUCR8Q2H_app-3Af908d76079915f06_1_ol_0_perc_100000_mul_1_rcs-3Acss_0; fullstoryEnabled=true; s_cc=true; IR_gbd=woolworths.com.au; aam_uuid=54673081338741561694281116979093259714; _fbp=fb.2.1693217295462.296038162; _tt_enable_cookie=1; _ttp=SsdgDsXicY6lwQmgav94fD8cFyA; _gcl_au=1.1.1254404271.1693217296; _gid=GA1.3.987102651.1693217296; mdLogger=false; dtSa=-; BVBRANDID=c22700ea-3bec-4467-8617-3bc81df4e54b; AKA_A2=A; bm_sz=F48CC64C0F9E93E52636C482E983E8D7~YAAQJMfOF4ab8T2KAQAAUm8PQBR8tmlKU/Cnarj/BYMKWVT2AW26lkf2i/8RCGDWg8EtBdmUMwNfXqUUaCci/ZvdyrO8/UgTkdhbW5s8YtEzB/3lEFyCPNQlCxRxRAGSn34DjRPW/0ZjKSk/NtZ1/jOl1R7Gj1MZ+SK9K6KlwTzggrStXTXUVj2GG46KI4D7rpIwqXv+RV0Eg3GlfNtXC8a2ia/hzQcUoM3Pwq97ScUEL/WgAX//lZZZ2Us6meLwrxy02rflr54XCIAonpjmaUD6s9xay1k14XhObFD7LNdjVCzY6Gu9u5Qb~4338482~3355192; w-rctx=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE2OTMyOTE4NjgsImV4cCI6MTY5MzI5NTQ2OCwiaWF0IjoxNjkzMjkxODY4LCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6ImJlYTI3ZjEyLTJkZDEtNDYwMS1hNWY5LTY5MzViMjk5ZjhmOSIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.jzaC-9-YbDP9PYwOhYoVG32BO3qcdQGHbeE2CCBiRwM98CTURL5f44mlNW2d20_2E0UIh2TXDOzG0SEn7Z-i8fn0QzOMAkBYaov6ItwU5GG7ube4ATKIhTFQ-Sn0CRIp32p-wIo-fxM3-l5ffXvic9ExogPUeC3EftWrBlYS2fdtue4ZtyrPiQyGiwmOFpq4WdL35NJRgli4RCBo9PDSJ9nNQn205Mb2x6MaGUXwgWL4tU9M7ACCyStz_zlsC3JCnjGuKwoph8aehNrgiJDt7UZEb80JbUQRr8HURBdIrAHl8-r41HPGwPyAwbzwL1b54bheigqQ7jzOUg9-RF9JVQ; wow-auth-token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE2OTMyOTE4NjgsImV4cCI6MTY5MzI5NTQ2OCwiaWF0IjoxNjkzMjkxODY4LCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6ImJlYTI3ZjEyLTJkZDEtNDYwMS1hNWY5LTY5MzViMjk5ZjhmOSIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.jzaC-9-YbDP9PYwOhYoVG32BO3qcdQGHbeE2CCBiRwM98CTURL5f44mlNW2d20_2E0UIh2TXDOzG0SEn7Z-i8fn0QzOMAkBYaov6ItwU5GG7ube4ATKIhTFQ-Sn0CRIp32p-wIo-fxM3-l5ffXvic9ExogPUeC3EftWrBlYS2fdtue4ZtyrPiQyGiwmOFpq4WdL35NJRgli4RCBo9PDSJ9nNQn205Mb2x6MaGUXwgWL4tU9M7ACCyStz_zlsC3JCnjGuKwoph8aehNrgiJDt7UZEb80JbUQRr8HURBdIrAHl8-r41HPGwPyAwbzwL1b54bheigqQ7jzOUg9-RF9JVQ; prodwow-auth-token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE2OTMyOTE4NjgsImV4cCI6MTY5MzI5NTQ2OCwiaWF0IjoxNjkzMjkxODY4LCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6ImJlYTI3ZjEyLTJkZDEtNDYwMS1hNWY5LTY5MzViMjk5ZjhmOSIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.jzaC-9-YbDP9PYwOhYoVG32BO3qcdQGHbeE2CCBiRwM98CTURL5f44mlNW2d20_2E0UIh2TXDOzG0SEn7Z-i8fn0QzOMAkBYaov6ItwU5GG7ube4ATKIhTFQ-Sn0CRIp32p-wIo-fxM3-l5ffXvic9ExogPUeC3EftWrBlYS2fdtue4ZtyrPiQyGiwmOFpq4WdL35NJRgli4RCBo9PDSJ9nNQn205Mb2x6MaGUXwgWL4tU9M7ACCyStz_zlsC3JCnjGuKwoph8aehNrgiJDt7UZEb80JbUQRr8HURBdIrAHl8-r41HPGwPyAwbzwL1b54bheigqQ7jzOUg9-RF9JVQ; ak_bmsc=96F61D3F1531F9B0F900A604328200A9~000000000000000000000000000000~YAAQJMfOF+yb8T2KAQAAoHUPQBQdLjUQWVZ4PrpbN15jwshWn0/G3jZ96fNbFnX60zHFRUiuldzkV4Fgj/vPQPmpY5VFQ5QLdvZ+8OYyqYFqMQFQTXzZm9kwCNy1IRI1qJTxKIuAjh0aCtG7teblg9DBMXahtYAi6GdFej9n+c+gozeU525dhe0KoqJ7+i+EzIxOltqEIgMV11SJloW27Y+EvfCQql+b25/Tf4ktdbLqhDLXFH4iSVCBzRmL2pWwAoKM+lGLGFKbNIvyRWXZTaxXzh0Ab9lJ+lVy9NgpHaGnEoNGVf3cOAUgvD6RSaoM1LTG1WsHJ9x3dehy+sRCVHjhtVTkn7HZ+4t5dS0a0LFHSo/VfvcWjSnb0YPRJ8Q0qxm514KQYzXGkRCNlS8VjJi1qP1DssS0xJgV20DF3/KArJIgmIn7B6GPq7StfuFBZk6Mux29jq1r4gpFqu8ZmpFjXInALJQ3Hwdmyv8IgUO7HjDyJuitGfjJzUiwBN43/qvhzxBK6w==; _uetsid=cd3b8a80458a11ee8820c1339a0c2e9b; _uetvid=a41b5880eb1811ed85dd2bc3746f9435; kampyleUserSession=1693291872182; kampyleUserSessionsCount=12; kampyleSessionPageCounter=1; kampyleUserPercentile=47.376515857582845; AMCV_4353388057AC8D357F000101%40AdobeOrg=179643557%7CMCIDTS%7C19598%7CMCMID%7C54382959485934252374309636602294463518%7CMCAAMLH-1693896672%7C8%7CMCAAMB-1693896672%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1693299072s%7CNONE%7CvVersion%7C5.5.0; IR_7464=1693291872418%7C0%7C1693291872418%7C%7C; BVBRANDSID=74fcc590-7131-4195-83a5-9123d099d5d5; _ga_YBVRJYN9JL=GS1.1.1693291872.6.1.1693291872.60.0.0; _abck=513C6B67B68BAD436AEF271DD7EA611E~0~YAAQJMfOF4ic8T2KAQAAIYYPQAo+x4x04mWwDFa8cLhlR3UFbHgVZoZuhw4rhnDft3PSxHS0RvqAbsZ32acrKTMP+tzkMqkMFkeED2+D5GWCFs+PZNL8Qk6c1htHwCslNDHjeRzxh0KqU+veS7uQ9F4gPCf+4K/QdriLxeD4GUfKpZEvGDgQ+LgjybZlAX+nTWaMOeuxrx+4T9+e8RzaegLGUX724mWgXf0lVeYrTrlarKbWhL+Yw6jukAxN4fbMrQfTRFuWQ0TmILAlQJAwO3WAi263KsvWdnNHwLq/tEBhF54wisZGEUOTbW+2eKdGrQhhAzfjRpl5WMHoHt2bMqDVAX+2mIdkTVpCBsMmeJtPHxB6mamZ2DsvZcodXx2iMvBdw+U3ejk10JSnq9XHXj5eaHrgHcNWyohGuieiFw==~-1~-1~-1; fs_lua=1.1693291873155; fs_uid=^#o-1A4QVM-na1^#209865f7-3c24-417c-a599-2d2e31056dce:044c5dd0-7ee6-49f2-a215-166d9c4d8f43:1693291873155::1^#/1724753294; _ga=GA1.3.1000879306.1693217295; _gat_gtag_UA_38610140_9=1; ai_session=s9UHTH4zqnHUiXp9KH7nij|1693291868466|1693291874237; utag_main=v_id:018a3b9d87af0047ec373cfb1d680506f001e06700f58^$_n:4^$_e:8^$_s:0^$_t:1693293674951^$vapi_domain:woolworths.com.au^$dc_visit:4^$ses_id:1693291871759%3Bexp-session^$_n:1%3Bexp-session^$dc_event:1%3Bexp-session^$dc_region:ap-southeast-2%3Bexp-session; mbox=PC^#4d43a64863dd416ea058f5cb7a02a17c.36_0^#1756536673|session^#7d3ca8f2aa6d44ebbb5a0e86fd3918cc^#1693293736; RT="z=1&dm=www.woolworths.com.au&si=019057f0-126f-4e84-b188-2a12583ad95e&ss=llvy9a9y&sl=1&tt=1dp&rl=1"; bm_sv=0EAB494B436761BF109F258F80A5319D~YAAQJMfOF+Cc8T2KAQAAnpAPQBTnBllGmaipzJHw3e+2oXcowf/YXzO8yjb6aCbVjDK7fg/8ttTtcxzVduREYt09JNs8hHXT9/Ga/s9SzYU1aD1PILGyCMrmy+X1oxSS7ScIhqBpvoKeIH0+AklWKjjhD+xcVdYb9U97roYCbLDqMbVHPGYpBmla7sKRNbpeSfiK1wL78FS/FRV1BuCbjUGS7YlDLIW8RdNCijMgnm571ehuPsNCKjL8F/3zxLfIgaH04un8wEw=~1; rxvt=1693293675963|1693291867312; dtPC=5^$91875052_524h38vDWMRGUPHIJIBPNQDRVHAIFGBFLUEHKGP-0e0; _abck=513C6B67B68BAD436AEF271DD7EA611E~-1~YAAQC9/aFwlH/zeKAQAAuy8XQAo3tKa2OlWi1tvsiL1REoOUZgi37N9Ya2gn1CpSu/8q9TOnjjAmNYysPxPoA2l8kIc7TaQGCXxpBhS2H9CE3Na8eLRXoGcPH/V5M4tqO5UKM+A1lGXdahYCFUhQG5C6Xx/nDNfj9Jxn5Nd1xWPUTZxayTP4emHPwFobKbaNCLTht64ZT4phQ9+jSJyzE2xemYDRgtWewayl58c3zNCQ7+7+2zNdFNSFjCj9GricCTSudWnSEnBGDamlOm30IpCdUDyfjgMJCJW5lWzU3z4I8oHpAnRxW/Vx87BjL3xCu9t2nRXgNZnXvncrHtSMj53DgoJidgFdvkVLErZ45HaNkhfwx4XhDCUy4nSR2W6E165RhrXYjCxA6ao6MGzdMeMhJ+1ljlSSa4EHOyEEww==~0~-1~-1; akaalb_woolworths.com.au=~op=www_woolworths_com_au_ZoneB:PROD-ZoneB|www_woolworths_com_au_ZoneA:PROD-ZoneA|www_woolworths_com_au_BFF_SYD_Launch:WOW-BFF-SYD2|~rv=63~m=PROD-ZoneB:0|PROD-ZoneA:0|WOW-BFF-SYD2:0|~os=43eb3391333cc20efbd7f812851447e6~id=fafd49f1e39ab09c790e7da02180be29',
    'referer': 'https://www.woolworths.com.au/shop/productdetails/' + sku + '/abe-s-bagels-natural-bagels',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'x-dtpc': '5^$91875052_524h38vDWMRGUPHIJIBPNQDRVHAIFGBFLUEHKGP-0e0'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    try:
        print(data['Product']['Name'])
        print('kJ: ' + data['NutritionalInformation'][0]['Values']['Quantity Per 100g / 100mL'])
        print(data['NutritionalInformation'][1]['Name'] + " " + data['NutritionalInformation'][1]['Values']['Quantity Per 100g / 100mL'])
        print(data['NutritionalInformation'][2]['Name'] + " " + data['NutritionalInformation'][2]['Values']['Quantity Per 100g / 100mL'])
        print(data['NutritionalInformation'][3]['Name'] + " " + data['NutritionalInformation'][3]['Values']['Quantity Per 100g / 100mL'])
        print(data['NutritionalInformation'][4]['Name'] + " " + data['NutritionalInformation'][4]['Values']['Quantity Per 100g / 100mL'])
        print(data['NutritionalInformation'][5]['Name'] + " " + data['NutritionalInformation'][5]['Values']['Quantity Per 100g / 100mL'])
        print(data['NutritionalInformation'][6]['Name'] + " " + data['NutritionalInformation'][6]['Values']['Quantity Per 100g / 100mL'])
        print(data['NutritionalInformation'][7]['Name'] + " " + data['NutritionalInformation'][7]['Values']['Quantity Per 100g / 100mL'])
        print("\n")
        return
    except:
        print("No nutrition data")

    

    #print(data)

# Parse nutrition info

# Print each item name with the nutrition info 



getdata(url)
print(product_links)
loop_through_items(product_links)
#get_item_info()
