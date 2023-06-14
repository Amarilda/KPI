import pandas as pd
import datetime
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from credentials import USER, PASSWORD

def fitness():
    
    full_months = {
    'januar' : '01',
    'februar' : '02',
    'mars' : '03',
    'april' : '04',
    'mai' : '05',
    'juni' : '06',
    'juli' : '07',
    'august' : '08',
    'september' : '09',
    'oktober' : '10',
    'november' : '11',
    'desember' : '12',
    }

    ChromeOptions = webdriver.ChromeOptions()
    ChromeOptions.add_argument("--headless")

    logging.getLogger('WDM').setLevel(logging.NOTSET)
    
    wd = webdriver.Chrome(ChromeDriverManager().install(), options=ChromeOptions)
  
    url = 'https://www.freshfitness.no/treningsdagbok'
    wd.get(url)

    wait = WebDriverWait(wd, 10)

    xxpath = "/html/body/div[3]/div[3]/div/div/div[2]/div/div/button"
    wait.until(EC.element_to_be_clickable((By.XPATH, xxpath)))
    wd.find_element(By.XPATH, xxpath).click()

    wd.find_element(By.NAME,"user").send_keys(USER)
    #time.sleep(0.2)
    wd.find_element(By.NAME,"password").send_keys(PASSWORD)
    #time.sleep(0.4)

    xxpath = "/html/body/div[1]/div/main/div[2]/form/button/div"
    wait.until(EC.element_to_be_clickable((By.XPATH, xxpath)))
    wd.find_element(By.XPATH, xxpath).click()
    print('Fresh logged in')

    if datetime.datetime.today().strftime("%m") == full_months[wd.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div/div/div[2]/div/div[2]/div/button/div[1]').text]:
        df = pd.read_csv('fitness.csv')
        last_training = max(df.date)

        # Expand current month
        xxpath = "/html/body/div[1]/div/main/div/div/div/div[2]/div/div[2]/div/button/div[1]"
        wait.until(EC.element_to_be_clickable((By.XPATH, xxpath)))
        wd.find_element(By.XPATH,xxpath).click()

        # current month
        last_training = max(df.date)

        class_ele = wd.find_element(By.XPATH,'/html/body/div[1]/div/main/div/div/div/div[2]/div/div[2]/div/div/div/div/ol')
        for ol in class_ele.find_elements(By.CLASS_NAME, 'participation-group__item'):            
            if str(ol.text.split('\n')[1:2])[2:-2] > last_training:
                try:
                    df.loc[len(df)] = ol.text.split('\n')                    
                except: pass

            df.sort_values(by = ["date", 'time'], inplace = True)
            df.reset_index(drop = True, inplace = True)
            df.to_csv('fitness.csv', index = False)

        # until Fresh fix their Bloody check in system
        new_maximum = max(df.date)

        if str(datetime.date.today()) == new_maximum:
            new_entries = list(df['class'][df.date == new_maximum])
            print(len(new_entries))
            print(new_entries)