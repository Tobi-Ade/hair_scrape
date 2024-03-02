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
    browser = uc.Chrome(options=options,detach=True, version_main=120)
    browser.get(url)
    time.sleep(15)
    print(browser.current_url)

    try:
        # products_links = browser.find_elements(By.XPATH, '//div[@class="nr-details"]')
        products = []
        next_page = browser.find_element(By.XPATH, '//li//a[@class="next page-numbers"]')
        time.sleep(5)
        home_page = browser.current_window_handle
        while next_page:
            try:
                time.sleep(5)
                print(browser.current_url)
                # wait = WebDriverWait(browser, 10)
                # wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li//a[@class="next page-numbers"]')))
                products_links = browser.find_elements(By.XPATH, '//div[@class="nr-details"]')
                page_products = [product.find_element(By.TAG_NAME, 'a') for product in products_links]
                [products.append(product) for product in page_products]
                print(len(products))
                print()
                next_page = browser.find_element(By.XPATH, '//li//a[@class="next page-numbers"]')
                next_page.send_keys(Keys.CONTROL + Keys.RETURN)
                time.sleep(5)
                browser.switch_to.window(browser.window_handles[-1])
            except NoSuchElementException:
                next_page = False
                products_links = browser.find_elements(By.XPATH, '//div[@class="nr-details"]')
                page_products = [product.find_element(By.TAG_NAME, 'a') for product in products_links]
                [products.append(product) for product in page_products if product not in products]
                browser.switch_to.window(home_page)

        time.sleep(5)
        check = [product.get_attribute('outerHTML') for product in products]
        print(check)



        # product = products[0]
        # home = browser.current_window_handle
        # action = ActionChains(browser)
        # product_brand = "tginatural"
        # time.sleep(5)
        # product.send_keys(Keys.CONTROL + Keys.RETURN)
        # time.sleep(10)
        # browser.switch_to.window(browser.window_handles[1])
        # time.sleep(10)
        # print(browser.current_url)
        # product_page = browser.current_window_handle

        # product_name = browser.find_element(By.XPATH,'//h1[@class="productView-title"]').text.strip()
        # product_ingredients = browser.find_element(By.XPATH, '//dd[@class="productView-info-value productView-info-value--cfKeyIngredients"]').text.strip()
        # product_function = browser.find_element(By.XPATH, '//dd[@class="productView-info-value productView-info-value--cfWhatItDoes"]').text.strip()
        # time.sleep(5)



        
    except Exception as e:
        print(e)


scrape()