import os
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import xlsxwriter
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


def PropertyLink(sourceurl):
    # This function will read the page given and out put an df
    # with all links and address
    path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'\
    # change this address for different surburb
    url = sourceurl
    # Add this with the find link to find the address of that property
    baseurl = 'https://www.onthehouse.com.au'

    # create a dataframe to store the result
    initial = {'Link':[],
                'address':[]}
    df = pd.DataFrame(initial)

    # option to run in headless mode
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    # run the script in driver
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.get(url)

    # wait for page to load
    driver.implicitly_wait(0.5)

    # cook the soup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # find the address and url link for each property listed in this page
    souplevel1 = soup.find_all('div', class_='PropertySearch__resultSlot--1YH_u')
    for levelsoups in souplevel1:
        addressSoup = levelsoups.find('div', class_ = 'card-text d-flex align-items-center PropertyCardSearch__propertyCardText--101wp')
        try:
            nextpage = levelsoups.div.a['href']
            nextpagelink = baseurl + nextpage
            address = addressSoup.div.text
            tostore = {'Link': [nextpagelink],
                       'address': [address]}
            dfnew = pd.DataFrame(tostore)
            df = pd.concat([df,dfnew])
        except:
            continue
    driver.close()

    return df


def Propertyinfo(url, address):
    # This function take a url link and address, then generate a library contain all the information
    # then you need to parse it into dataframe and then concat it, good luck
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
    result = {'Link': [url],
              'address': [address]}

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
    # button.click()
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
    infomore = soup.find_all('span', class_='text-secondary w-50')
    year_type = ''
    for aa in infomore:
        year_type = year_type + aa.text + ' '
    result['year_type'] = year_type

    # Find the historical sell information
    inforhis = soup.find_all('div', class_='d-flex flex-column')
    count = 1
    for bb in inforhis:
        resulttitle = 'Sold_History' + str(count)
        historypart1 = bb.find_all('div')[0].text
        historypart2 = bb.find_all('div')[1].text
        result[resulttitle] = historypart1 + ' ' + historypart2
        count = count + 1

    driver.close()

    return result
