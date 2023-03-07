import pandas as pd

import requests
from bs4 import BeautifulSoup

import datetime
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import logging

def pension():

    df = pd.read_csv('daily_price.csv')

    urls = ['https://www.hl.co.uk/funds/fund-discounts,-prices--and--factsheets/search-results/h/hl-multi-manager-balanced-managed-trust-accumulation',
    'https://www.hl.co.uk/funds/fund-discounts,-prices--and--factsheets/search-results/h/hl-multi-manager-special-situations-trust-accumulation',
    'https://www.hl.co.uk/funds/fund-discounts,-prices--and--factsheets/search-results/h/hl-multi-manager-strategic-bond-trust-accumulation',
    'https://www.hl.co.uk/funds/fund-discounts,-prices--and--factsheets/search-results/b/blackrock-consensus-85-class-i-accumulation',
    'https://www.hl.co.uk/funds/fund-discounts,-prices--and--factsheets/search-results/c/ct-ftse-all-share-tracker-class-2-accumulation',
    'https://www.hl.co.uk/funds/fund-discounts,-prices--and--factsheets/search-results/v/vanguard-esg-developed-world-all-cap-equity-accumulation',
    'https://www.hl.co.uk/funds/fund-discounts,-prices--and--factsheets/search-results/v/vanguard-ftse-uk-equity-income-index-income',
    'https://www.hl.co.uk/funds/fund-discounts,-prices--and--factsheets/search-results/v/vanguard-ftse-uk-all-share-index-income',
    'https://www.hl.co.uk/funds/fund-discounts,-prices--and--factsheets/search-results/l/legal-and-general-european-index-class-c-income',
    'https://www.hl.co.uk/funds/fund-discounts,-prices--and--factsheets/search-results/l/legal-and-general-us-index-class-c-income']


    for url in urls[1:]:
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, features="lxml")
        atbilde = []

        atbilde= [str(datetime.date.today())]

        text = soup.find('h1').text.strip()
        atbilde.append(text[:text.find('\r')])
        for link in soup.find(class_="ask price-divide"):
            atbilde.append(float(link[:-1].replace(",","")))
        time.sleep(5)

        df.loc[len(df)] = atbilde

    df.to_csv('daily_price.csv', index = False)
    print('HL appended')

    pension = pd.read_csv('pension.csv', usecols = ['Name','Units', 'Cost'])[:3]
    df = pd.read_csv('daily_price.csv')
    new = df[df.name.str.contains('HL')][-3:].merge(pension, left_on='name', right_on='Name')

    percent = sum(new.price*new.Units/100 -new.Cost)/sum(new.Cost)

    print('{:.2%} : current return '.format(percent))
    print('{:.2%} : % to go until sale '.format(.2-percent))  


    ## Schroder
    df = pd.read_csv('daily_price.csv')

    the_last_Shroder_date = max(df.date[df.name == 'Schroder Managed Balanced'])
    
    ChromeOptions = webdriver.ChromeOptions()
    ChromeOptions.add_argument("--headless")

    logging.getLogger('WDM').setLevel(logging.NOTSET)
    url = 'https://finance.yahoo.com/quote/0P0000JWBZ.L/history?p=0P0000JWBZ.L'

    wd = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=ChromeOptions)
    wd.get(url)

    xxpath = "/html/body/div/div/div/div/form/div[2]/div[2]/button"
    wait = WebDriverWait(wd, 5)
    wait.until(EC.element_to_be_clickable((By.XPATH, xxpath)))
    wd.find_element(By.XPATH,xxpath).click()

    yahoo = wd.find_element(By.CSS_SELECTOR, 'div')
    line = yahoo.find_elements(By.TAG_NAME, 'tr') # return a list


    for cell in line[1:3]:
        if cell.get_attribute('innerText').split('\t')[2] == '-':
            pass
        elif str(pd.to_datetime(cell.get_attribute('innerText').split('\t')[0]).strftime('%Y-%m-%d'))  > the_last_Shroder_date:
            df.loc[len(df)] = [str(pd.to_datetime(cell.get_attribute('innerText').split('\t')[0]).strftime('%Y-%m-%d')), 'Schroder Managed Balanced', float(cell.get_attribute('innerText').split('\t')[4])]
            df.sort_values(by = 'date').to_csv('daily_price.csv', index = False)
        else:
            break