import pandas as pd
from ScrapeTest import *
import os
import time
import datetime



def run1(firstpage,surburb):
    # enter first page link in sting
    # enter surburb name in string
    # this will return a csv file with link and address in two coloumns
    baseurl = firstpage
    nextpage = '&page='
    url = baseurl
    result = pd.DataFrame({'Link':[],
                           'address':[]})
    for i in range(60):
        try:
            df = PropertyLink(url)
            i = str(i + 2)
            url = baseurl + nextpage + i
            result = pd.concat([result,df])
            print(i)
        except:
            break

    result.to_csv(surburb + '_link.csv')

def run2(sourcecsv):
    # enter the csv file generated from run1
    # this will parse that and scrape all the house info included
    dflink = pd.read_csv(sourcecsv)
    result = pd.DataFrame({})
    for i in range(len(dflink['Link'])):
        link = dflink['Link'][i]
        address = dflink['address'][i]
        try:
            a = Propertyinfo(link, address)
            df = pd.DataFrame(a)
            result = pd.concat([result,df])
            print(i)
        except:
            print(str(i) + 'error')
            continue

    pos = sourcecsv.find('_')
    result.to_csv(sourcecsv[:pos]+'.csv')

def run3():
    # run multiple run2 and store the run time as result
    # can not be bothered to comment out each time
    with open('Timer.txt' , 'w') as f:
        # process the first csv file
        time1 = time.time()
        run2('Bella Vista_link.csv')
        time2 = time.time()
        f.write('The first csv processing time is : ' + str(time2-time1) + '\n')
        os.remove('Bella Vista_link.csv')

        time1 = time.time()
        run2('Kings Langley_link.csv')
        time2 = time.time()
        f.write('The second csv processing time is : ' + str(time2-time1) + '\n')
        os.remove('Kings Langley_link.csv')

        time1 = time.time()
        run2('Quakers Hill_link.csv')
        time2 = time.time()
        f.write('The third csv processing time is : ' + str(time2-time1) + '\n')
        os.remove('Quakers Hill_link.csv')

run3()

