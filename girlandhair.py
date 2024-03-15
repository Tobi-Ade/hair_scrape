"""
importing necessary libraries
"""
# import pandas as pd
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc 
import time
from selenium.webdriver.common.action_chains import ActionChains 

def scrape():
    url = "https://www.girlandhair.com/collections/g-h-system"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')  # to bypass os security
    options.add_argument("--start-maximized") # setting the width for the browser
    # to overcome limited resources
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    browser = uc.Chrome(options=options,detach=True)
    browser.get(url)
    time.sleep(10)

    product_list = []
    data_list = {}
    i = 0
    while i < 3:
        items = browser.find_elements(By.XPATH, '//div[@class="grid-view-item--desc-wrapper"]//p[@class="product-grid-title"]/a')
        last_item = items[-1]
        browser.execute_script("arguments[0].scrollIntoView();", last_item)
        wait = WebDriverWait(browser, 10)      
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//h4[@class="card-title"]/a')))
        time.sleep(10)
        [product_list.append(item) for item in items if item not in product_list]        
        i+=1
    print(len(product_list))
