"""
importing necessary libraries
"""
"""
importing necessary libraries
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import traceback
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

def scrape():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')
    options.add_argument("--start-maximized")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    service = Service(executable_path='./chromedriver-win64/chromedriver.exe')
    browser = webdriver.Chrome(service=service, options=options)
    try:
        try:
            products = []
            for i in range(1, 4):
                url = requests.get(f"https://thedoux.com/collections/hair-care?page={i}#collection-root")
                soup = BeautifulSoup(url.text,'html.parser')
                products_links = soup.find_all('div',{"class":"product--root"})
                links = [product.find('a', ) for product in products_links]
                [products.append(str(link).split('href="')[1].split('"')[0]) for link in links]
            print(len(products))
        except Exception as e:
                print(e)
        data_list = []
        home_page = browser.current_window_handle
        product_brand = "The Doux"
        main_page = "https://thedoux.com"
        for product_link in products:
            final_data = []
            link = main_page + product_link
            browser.execute_script("window.open(arguments[0], '_blank');",link)
            browser.switch_to.window(browser.window_handles[1])
            print(browser.current_url)
            product_name = browser.find_element(By.XPATH, './/div[@class="product-page--block"]//h2').get_attribute("innerHTML").strip()
            print(f"getting data for {product_name}...")
            info = browser.find_elements(By.XPATH, '//div[@class="easyslider-content-wrapper"]')
            # product_desc = browser.find_element(By.XPATH, '//div[@class="easyslider-content"]/div[0]')
            product_desc = browser.execute_script("return arguments[0].textContent;", info[0])
            # product_directions = browser.find_element(By.XPATH, '//div[@class="easyslider-content"]/div[2]')
            product_directions = browser.execute_script("return arguments[0].textContent;", info[2])
            # product_ingredients = browser.find_element(By.XPATH, '//div[@class="easyslider-content"]/div[3]')
            product_ingredients = browser.execute_script("return arguments[0].textContent;", info[3])

            reviews = browser.find_element(By.XPATH, '//div[@data-bv-show="reviews"]')
            print(reviews)
            break
            for review in reviews:
                data = {}
                review_topic = review.find_element(By.XPATH, './/h3[@class="spr-review-header-title"]').get_attribute('innerHTML')
                reviewer_name = review.find_element(By.XPATH, './/span[@class="spr-review-header-byline"]//strong').get_attribute('innerHTML')
                review_content = review.find_element(By.XPATH, './/p[@class="spr-review-content-body"]').get_attribute('innerHTML')
                review_date = review.find_elements(By.XPATH, './/span[@class="spr-review-header-byline"]//strong')[1].get_attribute('innerHTML')
                rating_count = review.find_elements(By.XPATH, './/div[@class="spr-review-header"]//i[@class="spr-icon spr-icon-star"]')
                review_rating = (len(rating_count))


            browser.switch_to.default_content()
            browser.close()
            browser.switch_to.window(home_page)
            # break







    except Exception as e:
        print(e)
        traceback.print_exc()


scrape()