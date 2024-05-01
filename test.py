from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'\
# change this address for different surburb
url = 'https://www.onthehouse.com.au/property/nsw/castle-hill-2154/31-16--20-mercer-st-castle-hill-nsw-2154-14263432'
# Add this with the find link to find the address of that property
baseurl = 'https://www.onthehouse.com.au'
# Add number to the end to change page
nextpage = '?page='

driver = webdriver.Chrome(path)
driver.get(url)
driver.implicitly_wait(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')

# find the information of Bedrooms, bathroom, car space, floor are, and land area
level2info = soup.find_all('div', class_='d-flex align-items-center')
for info in level2info:
    try:
        print(info['title'])
        print(info.find_all('div')[1].text)
    except:
        print('Not find')

# Find the estimate rent tab and click it
button = driver.find_element_by_id('rentalEstimateTab')
button.click()
# wait for the page to reload
driver.implicitly_wait(5)
WebDriverWait(driver, 10)
# Re cook the updated page
soup = BeautifulSoup(driver.page_source, 'html.parser')
price1 = soup.find_all('div', class_ = 'mdText')
for price in price1:
    try:
        print(price.find_all('div'))
    except:
        print('--------')
