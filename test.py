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
import traceback
from selenium.webdriver.common.action_chains import ActionChains 


def scrape():
    url = "https://tginatural.com/product/sweet-honey-hair-milk-8oz/"
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
    product_name = browser.find_element(By.XPATH, '//div[@class="pro-detail-tgin-text"]//h1').text
    print(f"getting data for {product_name}...")
    while product_name:


        info = browser.find_element(By.XPATH, '//div[@class="product-info-content-column"]//div[@class="inner"]')
        product_desc = browser.find_element(By.XPATH, '//div[@class="pro-detail-tgin-text"]//p').text
        try:
            product_directions = info.find_elements(By.TAG_NAME, 'p')[2].text.split("Directions:")[1]
        except IndexError:
            product_directions = info.find_elements(By.TAG_NAME, 'p')[2].text.split("Instructions:")[1]
        product_ingredients = info.find_elements(By.TAG_NAME, 'p')[3].text.split("Ingredients:")[1]
        reviews_button = browser.find_element(By.XPATH, '//button[@id="tab-3"]')
        reviews_button.click()
        time.sleep(5)
        reviews = browser.find_elements(By.XPATH, './/div[@class="stamped-reviews"]//div[@class="stamped-review"]')
        final_data = []
        print(f"rev count: {len(reviews)}")

        for review in reviews:
            header = review.find_element(By.XPATH, '//div[@class="stamped-review-header"]')
            content = review.find_element(By.XPATH, './/div[@class="stamped-review-content"]')
            review_topic = content.find_element(By.XPATH, './/h3').get_attribute('innerHTML')
            reviewer_name = review.find_element(By.XPATH, './/div[@class="stamped-review-header"]//strong[@class="author"]').get_attribute('innerHTML')
            review_content = content.find_element(By.XPATH, './/p[@class="stamped-review-content-body"]').get_attribute('innerHTML')
            review_date = header.find_element(By.XPATH, './/div[@class="created"]').get_attribute('innerHTML')
            review_rating = str(content.find_element(By.XPATH, './/span').get_attribute("outerHTML").split(" ")[4]).split("=")[-1].split('"')[1].split('"')[0]
            
            data = {
                    'product_name': product_name,
                    'product_ingredients': product_ingredients,
                    'product_desc': product_desc,
                    'product_directions': product_directions,
                    'reviewer_name': reviewer_name,
                    'review_topic': review_topic,
                    'review_comment': review_content,
                    'review_date': review_date,
                    'review_rating': review_rating 

                    } 
            print(data)
            print()
            if data not in final_data:
                final_data.append(data)
        wait = WebDriverWait(browser, 10, ignored_exceptions=(NoSuchElementException, StaleElementReferenceException))      
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li[@class="next"]/a')))
        next_rev_page = browser.find_element(By.XPATH, '//li[@class="next"]/a')
        print(next_rev_page.get_attribute('outerHTML'))
        wait = WebDriverWait(browser, 30)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@class="next"]/a')))
        next_rev_page.send_keys(Keys.CONTROL + Keys.RETURN)
        print()
        time.sleep(5)
        

scrape()