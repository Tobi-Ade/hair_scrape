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
    url = "https://tginatural.com/product-category/hair/"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox') 
    options.add_argument("--start-maximized") 
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    browser = uc.Chrome(options=options,detach=True)
    browser.get(url)
    time.sleep(15)
    print(browser.current_url)

    try:
        home_page = browser.current_window_handle
        products_links = browser.find_elements(By.XPATH, '//div[@class="nr-details"]')
        page_products = [product.find_element(By.TAG_NAME, 'a') for product in products_links]
        next_page = browser.find_element(By.XPATH, '//li//a[@class="next page-numbers"]')
        time.sleep(10)
        # wait = WebDriverWait(browser, 10)
        # wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li//a[@class="next page-numbers"]')))
        product_brand = "tgin"
        for product in page_products:
            data = {}
            time.sleep(5)
            product.send_keys(Keys.CONTROL + Keys.RETURN)
            time.sleep(5)
            browser.switch_to.window(browser.window_handles[-1])
            print(browser.current_url)
            product_page = browser.current_window_handle
            product_name = browser.find_element(By.XPATH, '//div[@class="pro-detail-tgin-text"]//h1').text
            info = browser.find_element(By.XPATH, '//div[@class="product-info-content-column"]//div[@class="inner"]')
            product_desc = browser.find_element(By.XPATH, '//div[@class="pro-detail-tgin-text"]//p').text
            length = len(info.find_elements(By.TAG_NAME, 'p'))
            product_ingredients = info.find_elements(By.TAG_NAME, 'p')[3]
            data["product_name"] = product_name
            data["product_desc"] = product_desc
            data["product_ingredients"] = product_ingredients

            print(product_ingredients.text)
            break
        

       
    except Exception as e:
        print(e)


scrape()