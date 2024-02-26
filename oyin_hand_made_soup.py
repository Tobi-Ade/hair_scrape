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
    browser = uc.Chrome(options=options,detach=True)
    browser.get(url)
    time.sleep(10)

    try:
        browser.execute_script("let element = getElementByClassName('page-sidebar mobileSidebar-panel');element.remove()")
        browser.execute_script("let element = getElementByClassName('launcher-container background-primary smile-launcher-font-color-light smile-launcher-border-radius-circular launcher-closed');element.remove()")
    except JavascriptException:
        pass

    product_list = []
    reviews = []
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
    product_brand = "oyin_hand_made"
    product = product_list[0]
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
    product.send_keys(Keys.CONTROL + Keys.RETURN)
    time.sleep(10)
    browser.switch_to.window(browser.window_handles[1])
    product_name = browser.find_element(By.XPATH,'//h1[@class="productView-title"]').text.strip()
    product_ingredients = browser.find_element(By.XPATH, '//dd[@class="productView-info-value productView-info-value--cfKeyIngredients"]').text.strip()
    product_function = browser.find_element(By.XPATH, '//dd[@class="productView-info-value productView-info-value--cfWhatItDoes"]').text.strip()
    
    reviews_list = []
    reviews = browser.find_elements(By.XPATH,'//li[@class="productReview"]/article')
    if len(reviews) > 0:
            for review in reviews:
                reviewer_name = review.find_element(By.XPATH, '//header//p[@class="productReview-author"]//span[@itemprop="name"]').get_attribute('outerHTML')
                # review_topic = review.find_element(By.XPATH, '//h5[@class="productReview-title"]').text
                review_comment = review.find_element(By.XPATH, '//p[@itemprop="reviewBody"]').get_attribute('outerHTML')
                # review_date = review.find_element(By.CLASS_NAME, "productReview-author").get_attribute('outerHTML')
                review_rating = review.find_element(By.XPATH, '//header//span[@class="productReview-rating rating--small"]//span[@itemprop="ratingValue"]').get_attribute('outerHTML')
                
                data = {
                    'product_brand': product_brand,
                    'product_name': product_name,
                    'product_ingredients': product_ingredients,
                    'product_function': product_function,
                    # 'review_topic': review_topic,
                    'reviewer_name': reviewer_name,
                    'review_comment': review_comment,
                    # 'review_date': review_date,
                    'review_rating': review_rating 

                } 
                break
        

    print(data)        
    #        
    # # reviews_list.append(reviews)
    # print(browser.current_url)
    # next_page = browser.find_element(By.XPATH, '//a[@class="pagination-link"]')

    
    # time.sleep(10)
    # while next_page:
    #     next_page.send_keys(Keys.CONTROL + Keys.RETURN)
    #     time.sleep(5)
    #     browser.switch_to.window(browser.window_handles[-1])
    #     print(browser.current_url)
    #     time.sleep(10)
    #     reviews = browser.find_elements(By.XPATH,'//article[@itemprop="review"]')
    #     # [reviews_list.append(review) for review in reviews if review not in reviews_list]
    #     break
    # print(f"last review count: {len(reviews)}")


    #     try:
    #         browser.execute_script("let element = getElementByClassName('page-sidebar mobileSidebar-panel');element.remove()")
    #     except JavascriptException:
    #         pass
    #     time.sleep(2)
    #     try:
    #         browser.execute_script("let element = getElementByClassName('launcher-container background-primary smile-launcher-font-color-light smile-launcher-border-radius-circular launcher-closed');element.remove()")
    #     except JavascriptException:
    #         pass
    #     wait = WebDriverWait(browser, 10)
    #     wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="pagination-link"]')))
    #     time.sleep(5)
    #     reviews = browser.find_elements(By.XPATH,'//article[@itemprop="review"]')
    #     [reviews_list.append(review) for review in reviews if review not in reviews_list]
    
    # print(len(reviews_list))


    
    

    



    

    #comment, name, rating, date
    browser.close()


scrape()


