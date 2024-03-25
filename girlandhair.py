"""
importing necessary libraries
"""
# import pandas as pd
from bs4 import BeautifulSoup
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
from selenium.webdriver.chrome.service import Service
import pandas as pd

try:
        
    url = "https://www.girlandhair.com/collections/g-h-system"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')  # to bypass os security
    options.add_argument("--start-maximized") # setting the width for the browser
    # to overcome limited resources
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    #     browser = uc.Chrome(options=options,detach=True)
    service = Service(executable_path='./chromedriver-win64/chromedriver.exe')
    browser = webdriver.Chrome(service=service,options=options)
    browser.get(url)
    print(browser.current_url)
    time.sleep(3)
    main_browser = browser.current_window_handle
    all_item = browser.find_elements(By.XPATH,'//div[@class="grid-view-item--desc-wrapper"]')
    print(len(all_item))
    total_data = []
    brand = "Girl + Hair"
    for item in all_item:
        href = item.find_element(By.XPATH,'.//p[@class="product-grid--title"]/a').get_attribute('href')
        browser.execute_script("window.open(arguments[0], '_blank');",href)
        time.sleep(2)
        browser.switch_to.window(browser.window_handles[1])
        product_name = browser.find_element(By.XPATH,'//h1[@class="product-details-product-title"]').text
        product_details = browser.find_element(By.XPATH,'//div[@id="accordion"]/div[1]')
        product_details = browser.execute_script("return arguments[0].textContent;", product_details)
        product_ingredient = browser.find_element(By.XPATH,'//div[@id="accordion"]/div[2]')
        product_ingredient = browser.execute_script("return arguments[0].textContent;", product_ingredient)
        product_use = browser.find_element(By.XPATH,'//div[@id="accordion"]/div[3]')
        product_use = browser.execute_script("return arguments[0].textContent;", product_use)
        
        print('product_name',product_name)
        
        browser.switch_to.frame('looxReviewsFrame')
        load_more = browser.find_elements(By.XPATH,'//button[@id="loadMore"]')
        while len(load_more) > 0:
            browser.execute_script("arguments[0].click()", load_more[-1])
            time.sleep(1)
            load_more = browser.find_elements(By.XPATH,'//button[@id="loadMore"]')
            if "display: none" in load_more[-1].get_attribute('style'):
                break
        all_reviews = browser.find_elements(By.XPATH,'//div[@class="grid-item-wrap no-img"]')
        if len(all_reviews) > 0:
            for rev in all_reviews:
                review_author = rev.find_element(By.XPATH,'.//div[@class="block title"]').text
                rating = rev.find_element(By.XPATH,'.//div[@class="block stars"]').get_attribute('aria-label')
                review_post = rev.find_element(By.XPATH,'.//div[@class="pre-wrap main-text"]').text
                date = rev.find_element(By.XPATH,'.//div[@class="block time"]').text
                data = {
                    'brand':brand,
                    'product_name':product_name,
                    "review":review_post,
                    "reviewer_name":review_author,
                    "ratings":rating,
                    "ingredient":product_ingredient.strip(),
                    "product_function":product_use,
                    "date":date,
                    "description":product_details
                }
                total_data.append(data)
            df = pd.DataFrame(total_data)
            df.to_csv("data.csv")
        browser.switch_to.default_content()
        browser.close()
        browser.switch_to.window(main_browser)
except Exception as e:
    print(e)