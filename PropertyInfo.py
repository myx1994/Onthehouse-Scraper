import pandas as pd
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options




def propertyinfo(url,address):
    # path of chrome driver
    path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'

    # use option to run in headless mode
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    # load drive, cook soup and wait
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.implicitly_wait(0.5)

    # library to store the data
    result = {'Link':[url],
              'address':[address]}

    # find the information of Bedrooms, bathroom, car space, floor are, and land area
    level2info = soup.find_all('div', class_='d-flex align-items-center')
    for info in level2info:
        try:
            roomtype = info['title']
            roomnumber = info.find_all('div')[1].text
            result[roomtype] = roomnumber
        except:
            print('Not find')

    # Find the low/high selling price
    pricesell = soup.find_all('div', class_='d-flex justify-content-between bold600')
    for a in pricesell:
        sell_low = a.find_all('div')[0].text
        sell_high = a.find_all('div')[3].text
        result['sell_low'] = sell_low
        result['sell_high'] = sell_high

    # Find the estimate rent tab and click it
    button = driver.find_element_by_id('rentalEstimateTab')
    #button.click()
    driver.execute_script("arguments[0].click();", button)

    # wait for the page to reload
    driver.implicitly_wait(0.3)

    # Re cook the soup and parse HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the low/high rent price
    pricerent = soup.find_all('div', class_='d-flex justify-content-between bold600')
    for b in pricerent:
        rent_low = b.find_all('div')[0].text
        rent_high = b.find_all('div')[3].text
        result['rent_low'] = rent_low
        result['rent_high'] = rent_high

    # Find the property type and year build
    infomore = soup.find_all('span', class_ = 'text-secondary w-50')
    year_type = ''
    for aa in infomore:
        year_type = year_type + aa.text + ' '
    result['year_type'] = year_type

    # Find the historical sell information
    inforhis = soup.find_all('div', class_ = 'd-flex flex-column')
    count = 1
    for bb in inforhis:
        resulttitle = 'Sold_History' + str(count)
        historypart1 = bb.find_all('div')[0].text
        historypart2 = bb.find_all('div')[1].text
        result[resulttitle] = historypart1 + ' ' + historypart2
        count = count + 1
    
    driver.close()
    
    return result

#reslib = propertyinfo('https://www.onthehouse.com.au/property/nsw/castle-hill-2154/16-orleans-way-castle-hill-nsw-2154-4340757','address')
#df = pd.DataFrame(reslib)
#df.to_csv('aaaaa.csv')
