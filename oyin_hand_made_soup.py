"""
importing necessary libraries
"""
import requests
# import pandas as pd
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc 
import time
from selenium.webdriver.common.action_chains import ActionChains 

def scrape():
    url = "https://oyinhandmade.com/hair/"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')  # to bypass os security
    options.add_argument("--start-maximized") # setting the width for the browser
    # to overcome limited resources
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    browser = uc.Chrome(options=options,detach=True, version_main=120)
    browser.get(url)
    time.sleep(10)

    try:
        browser.execute_script("let element = getElementByClassName('page-sidebar mobileSidebar-panel');element.remove()")
        browser.execute_script("let element = getElementByClassName('launcher-container background-primary smile-launcher-font-color-light smile-launcher-border-radius-circular launcher-closed');element.remove()")
    except JavascriptException:
        pass

    product_list = []
    i = 0
    while i < 4:
        items = browser.find_elements(By.XPATH, '//h4[@class="card-title"]/a')
        last_item = items[-1]
        browser.execute_script("arguments[0].scrollIntoView();", last_item)
        wait = WebDriverWait(browser, 10)      
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//h4[@class="card-title"]/a')))
        time.sleep(20)
        [product_list.append(item) for item in items if item not in product_list]        
        i+=1

    home = browser.current_window_handle
    action = ActionChains(browser)
    product = product_list[0]
    product_brand = "oyin_hand_made"

    # for product in product_list:
    try:
        browser.execute_script("let element = getElementByClassName('page-sidebar mobileSidebar-panel');element.remove()")
    except JavascriptException:
        pass
    time.sleep(2)
    try:
        browser.execute_script("let element = getElementByClassName('launcher-container background-primary smile-launcher-font-color-light smile-launcher-border-radius-circular launcher-closed');element.remove()")
    except JavascriptException:
        pass
    time.sleep(5)
    # action.move_to_element(product).key_down(Keys.CONTROL).click().key_up(Keys.CONTROL).perform()
    product.send_keys(Keys.CONTROL + Keys.RETURN)
    time.sleep(10)
    browser.switch_to.window(browser.window_handles[1])
    product_name = browser.find_element(By.XPATH,'//h1[@class="productView-title"]').text.strip()
    prodcut_ingredients = browser.find_element(By.XPATH, '//dd[@class="productView-info-value productView-info-value--cfKeyIngredients"]').text.strip()
    product_function = browser.find_element(By.XPATH, '//dd[@class="productView-info-value productView-info-value--cfWhatItDoes"]').text.strip()


    browser.close()
    product_data = {'brand_name': product_brand,
                    'product_name': product_name,
                    'prodcut_ingredients': prodcut_ingredients,
                    'product_function': product_function
                }
    print(product_data)

scrape()


