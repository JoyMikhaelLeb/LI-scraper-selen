"""
Created on Tue Jun 18 21:40:58 2023

@author: joy
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 22:20:10 2023

@author: joy
"""
import emoji

import json
import time
import datetime
from random import randint
import collections
# import pandas as pd
import re
import csv
from selenium.webdriver.support import expected_conditions as EC
#import json

#from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
import random

from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector
#
from bs4 import BeautifulSoup as bs
from selenium.common.exceptions import TimeoutException


from google.cloud import storage
import os

import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

if not firebase_admin._apps:
    cred = credentials.Certificate('spherical-list-284723-216944ab15f1.json')
    default_app = firebase_admin.initialize_app(cred)

db = firestore.client()



def login(username, password):

    url = 'https://www.linkedin.com/login'



    chrome_options = webdriver.ChromeOptions()

    prefs = {"profile.default_content_setting_values.notifications": 2}

    chrome_options.add_experimental_option("prefs", prefs)

    # chrome_options.add_argument("--incognito")

    chrome_options.add_argument("--start-maximized")
    # driver = webdriver.Chrome(executable_path='/home/dev/Downloads/chrome/chromedriver',chrome_options=chrome_options)
    try:

        driver = webdriver.Chrome(executable_path='/home/joy/Downloads/chromedriver_linux64/chromedriver',chrome_options=chrome_options)
    except:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

#    driver = webdriver.Chrome(chrome_options=chrome_options)
#    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)





    driver.get(url)



    driver.find_element_by_id('username').send_keys(username)

    driver.find_element_by_id('password').send_keys(password)

    driver.find_element_by_xpath("//*[contains(@aria-label, 'Sign in')]").click()


    time.sleep(2 + randint(1, 3))

    return driver


def moveToElement(driver, target):
    """
    Scroll to an element using either its XPath or WebElement.
    
    Parameters:
    driver: WebDriver object
    target: str or WebElement - Either an XPath string or WebElement object
    
    Returns:
    bool: True if successful, False otherwise
    """
    try:
        # If target is already a WebElement, use it directly
        if isinstance(target, webdriver.remote.webelement.WebElement):
            element = target
        # If target is a string (XPath), find the element
        else:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, target))
            )
        
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        return True
    except Exception as e:
        print(f"Error moving to element: {e}")
        return False
    


def scrollAndClickButtons(driver):
    """
    Scroll through the page and click all show more/show all buttons.
    """
    try:
        # Initial scroll to bottom and back to top
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, 0);")
        print("Scrolled to bottom and back to top.")

        # Find all show more/show all buttons
        button_xpath = "//button[contains(@class, 'show-all-button')]//span[contains(text(), ' ')]"
        button_elements = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.XPATH, button_xpath))
        )
        
        print(f"Found {len(button_elements)} button elements.")

        for i, button_element in enumerate(button_elements, 1):
            print(f"Processing button {i}/{len(button_elements)}")
            
            # Scroll button into view
            driver.execute_script("arguments[0].scrollIntoView(true);", button_element)
            
            # Ensure button is visible
            WebDriverWait(driver, 3).until(EC.visibility_of(button_element))
            
            # Use the updated moveToElement function
            if moveToElement(driver, button_element):
                # Click using JavaScript for reliability
                driver.execute_script("arguments[0].click();", button_element)
                print(f"Clicked button {i}/{len(button_elements)}")
            else:
                print(f"Failed to move to button {i}")

    except Exception as e:
        print(f"Error in scrollAndClickButtons: {e}")


def remove_emojis(s):
    
    return ''.join(c for c in s if c not in emoji.UNICODE_EMOJI['en']).strip()

remove_list=['MBA', 'PhD', 'CFO', 'CFA', 'MD', 'Ph.D', 'CPA', 'CTE', 'PMP', 'CSM', 'MCIPD','DR', 'SSM', 'HE','SHE','HIM','HER','HIS', 'HERS']
replace_by_space_list=['/','.','(',')']
custom_replace_list=['Dipl.-Math.']

def clean_name(name_in):
    #remove non-ascii
    # name_out=re.sub(r'[^\x00-\x7F]+','', name_in)
    name_out = remove_emojis(name_in)
    #custom_replace
    for custom_replace_item in  custom_replace_list:
        name_out=name_out.replace(custom_replace_item,"")
    name_out=name_out.strip()
    
    
    
    #basic replacements
    for replace_by_space_item in replace_by_space_list:
        
        name_out= name_out.replace(replace_by_space_item," ")
    name_out=name_out.title().split(",")[0]
    
    remove_list_title = [x.title() for x in remove_list]
    
    name_out_array_temp=name_out.split()
    name_out_array=[x.strip() for x in name_out_array_temp if x not in remove_list_title]
    
    
    name_out=" ".join(name_out_array)
    
    return name_out






def scrollDown1(driver, scrollNb=1):
    actions = ActionChains(driver)


    

    scrollCount = 0
    while True:
        
        pageFooterElement = driver.find_elements_by_xpath("//li[@class='artdeco-list__item pl3 pv3 ']")[0]
        actions.move_to_element(pageFooterElement).perform()

        
       
        
        pageFooterElement = driver.find_elements_by_xpath("//li[@class='artdeco-list__item pl3 pv3 ']")[5]
        actions.move_to_element(pageFooterElement).perform()

        
        
        pageFooterElement = driver.find_elements_by_xpath("//li[@class='artdeco-list__item pl3 pv3 ']")[10]
        actions.move_to_element(pageFooterElement).perform()

        
        pageFooterElement = driver.find_elements_by_xpath("//li[@class='artdeco-list__item pl3 pv3 ']")[15]
        actions.move_to_element(pageFooterElement).perform()

        
        
        pageFooterElement = driver.find_elements_by_xpath("//li[@class='artdeco-list__item pl3 pv3 ']")[20]
        actions.move_to_element(pageFooterElement).perform()

        
        
        pageFooterElement = driver.find_elements_by_xpath("//li[@class='artdeco-list__item pl3 pv3 ']")[24]
        actions.move_to_element(pageFooterElement).perform()

        
        scrollCount += 1
        if(scrollCount >= scrollNb):
            break
        
def scroll_to_element(driver):
    
    timeout=10
    element_xpath = "//section[@id='about-section']"
    # Wait for the element to be present on the page
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, element_xpath))
    )
    
    # Scroll to the element using JavaScript
    driver.execute_script("arguments[0].scrollIntoView();", element)

def scrollDown2(driver, scrollNb=1):
    actions = ActionChains(driver)


    

    scrollCount = 0
    while True:
        
        pageFooterElement = driver.find_elements_by_xpath("//li[@class='artdeco-list__item pl3 pv3 ']")[0]
        actions.move_to_element(pageFooterElement).perform()

        
       
        
        pageFooterElement = driver.find_elements_by_xpath("//li[@class='artdeco-list__item pl3 pv3 ']")[5]
        actions.move_to_element(pageFooterElement).perform()

        
        
        scrollCount += 1
        if(scrollCount >= scrollNb):
            break
        

def scrollDown3(driver, scrollNb=1):
    actions = ActionChains(driver)


    

    scrollCount = 0
    while True:
        
        pageFooterElement = driver.find_elements_by_xpath("//li[@class='artdeco-list__item pl3 pv3 ']")[3]
        actions.move_to_element(pageFooterElement).perform()

        
        
        scrollCount += 1
        if(scrollCount >= scrollNb):
            break

def check_navigator(driver):
    if moveToElement(driver, "//div[@class='artdeco-pagination ember-view']")==True:
            return True
    elif moveToElement(driver, "//div[@class='artdeco-pagination artdeco-pagination--has-controls ember-view']")==True:
        return True
    else:
        return False
    
def upload_to_gcs(bucket_name, folder_name, file_name, content, content_type):
    """
    Uploads a file to a specific folder in a Google Cloud Storage (GCS) bucket.
    
    Parameters:
    bucket_name (str): Name of the GCS bucket
    folder_name (str): Name of the folder within the bucket
    file_name (str): Name of the file to be uploaded
    content (str): The content to be uploaded (either HTML or JSON)
    content_type (str): The MIME type of the content ('text/html' or 'application/json')
    """
    # Initialize a storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Define the blob (file) path
    blob_path = f"{folder_name}/{file_name}"

    # Create a blob
    blob = bucket.blob(blob_path)

    # Upload the content to the blob
    blob.upload_from_string(content, content_type=content_type)

    print(f'File {file_name} uploaded to folder {folder_name} in bucket {bucket_name}.')

def upload_html_and_json(bucket_name, sr_id, html_content, data_to_save):
    """
    Uploads HTML and JSON files to a specific folder in a GCS bucket.
    
    Parameters:
    bucket_name (str): Name of the GCS bucket
    sr_id (str): The SrID to be used as the folder name
    html_content (str): The HTML content to be uploaded
    data_to_save (dict): The data to be saved as a JSON file
    """
    # Upload HTML file
    html_file_name = f"{sr_id}.html"
    upload_to_gcs(bucket_name, f"profile_advanced/{sr_id}", html_file_name, html_content, "text/html")

    # Upload JSON file
    json_file_name = f"{sr_id}.json"
    upload_to_gcs(bucket_name, f"profile_advanced/{sr_id}", json_file_name, json.dumps(data_to_save), "application/json")

    print("Files uploaded successfully.")
    
    
def advanced_search_people_profile_html(driver,saleID,SrID):
    
    driver.get("https://www.linkedin.com/sales/index")
    print("we are working in : ",SrID)
    driver.get(saleID)
    time.sleep(random.uniform(5,7))
    
    updated_Link = driver.current_url
    if (
        "/checkpoint/challenges" in updated_Link
        or "login?session_redirect" in updated_Link
        or "authwall?trk" in updated_Link
        or updated_Link == "https://www.linkedin.com/"
    ):
        return "security_check"
    # time.sleep(random.uniform(5, 7))
    # print("here")
    # experience = []
    if moveToElement(driver, "//div[@role='dialog']")==True:
        
        try:
            driver.find_elements_by_xpath("//div[@role='dialog']/div")[0].click()
        
        except:
            try:
                driver.find_element_by_xpath("//div[@role='dialog']/button").click()
            except:    
                pass
        
        
    retry_count = 3
    while retry_count > 0:
        try:
            WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//section[@id='profile-card-section']")))
            break  # Break the loop if the element is found
        except:
            retry_count -= 1
            if retry_count > 0:
                print("Retrying... attempts left: ", retry_count)
                driver.get(saleID)
                time.sleep(random.uniform(5, 10))
            else:
                print("Failed to load profile card section after multiple attempts")
                return "FAILED"
   
    time.sleep(1)
    
    try:
        # name = driver.find_element_by_xpath("//div[@class='name-title-container']/h1").text
        name = driver.find_element_by_xpath("//h1[@data-anonymize='person-name']").text
    except Exception as e:
        try:
            name = driver.find_element_by_xpath("//div[@class='_name-title-container_sqh8tm']/h1").text
            
        except:
            try:
                name = driver.find_element_by_xpath("//div[contains(@class,'name-title-container')]/h1").text
            except:
                name = ""
        
    if name == "":
        driver.refresh()
        time.sleep(random.uniform(3,10))
        name = driver.find_element_by_xpath("//div[@class='_name-title-container_sqh8tm']/h1").text
    
    elif name == "LinkedIn Member" and moveToElement(driver, "//span[text()='Unlock full profile']/parent::button")==True:
       
        try:
            # Locate the span with text "Unlock full profile"
            unlock_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='Unlock full profile']/parent::button"))
            )
        
            # Scroll to the button
            actions = ActionChains(driver)
            actions.move_to_element(unlock_button).perform()
        
            # Wait a little before interacting with it
            time.sleep(2)
        
            # Click the button
            unlock_button.click()
        
            print("Button clicked!")
        except Exception as e:
            print(f"An error occurred: {e}")
        # driver.find_element_by_xpath("//button[@class='ember-view _button_ps32ck _small_ps32ck _primary_ps32ck _left_ps32ck _container_iq15dg _cta_1xow7n _medium-cta_1xow7n']").click()
        # time.sleep(15)
        try:
            name = driver.find_element_by_xpath("//h1[@data-anonymize='person-name']").text
        except:
            name = "LI_MEMBER"
    elif name == "LinkedIn Member" and moveToElement(driver, "//span[contains(text(), 'Unlock')]")==False:
        print("Linkedin Member")
        name = "LI_MEMBER"
    
    elif name == "LinkedIn Member" and moveToElement(driver, "//span[text()='Unlock full profile']/parent::button")==False:
        print("Linkedin Member")
        name = "LI_MEMBER"
    else:
        name=name
        
    if name !="":
        try:
                moveToElement(driver, "//section[@class='_card_yg4u9b _container_iq15dg _lined_1aegh9']")    
                time.sleep(random.uniform(4, 7))
                try:
                    profile_butn = driver.find_element_by_xpath("//button[@class='ember-view _button_ps32ck _small_ps32ck _tertiary_ps32ck _circle_ps32ck _container_iq15dg _flat_1aegh9 _overflow-menu--trigger_1xow7n']")
                    profile_butn.click()    
                except:
                    try:
                        time.sleep(7)        
                        try:
                            profile_butn = driver.find_element_by_xpath("//button[@class='ember-view _button_ps32ck _small_ps32ck _tertiary_ps32ck _circle_ps32ck _container_iq15dg _flat_1aegh9 _overflow-menu--trigger_1xow7n']")
                            profile_butn.click()  
                        except:
                            profile_butn = driver.find_element_by_xpath("//button[@class='ember-view _button_ps32ck _small_ps32ck _tertiary_ps32ck _circle_ps32ck _container_iq15dg _overflow-menu--trigger_1xow7n']")
                            profile_butn.click()  
                    except:
                        linkedin_id = ""
                
                # linkedin_prof = driver.find_elements_by_xpath("//div[@class='_text_1xnv7i']")[0]
                # linkedin_prof.click()
                person_linkedin_id = driver.find_element_by_xpath("//a[@class='ember-view _item_1xnv7i']").get_attribute("href")
    
                 
    
        except:
                person_linkedin_id = ""
    else:
        name = "LI_MEMBER"
        person_linkedin_id = ""
    
    if person_linkedin_id!="":
        id_pers = person_linkedin_id.split("/in/")[1]
    
    if person_linkedin_id == "":
        # data_to_save = {"saleID": saleID, "profile_li_id":"","prof_id":SrID}

        # bucket_name = 'data-processing-html'
        # folder_name = 'profile_advanced/profiles_ids'
        # file_name = "LI_MEMBER" + '.json'
        # upload_dict_to_gcs_employees(bucket_name, folder_name, file_name,data_to_save)
                
        status = "FAILED"
        print("status :: ", status)
            
        
        return status
        
    if moveToElement(driver, "//section[@id='about-section']//button")==True:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)
            try:
                # Wait for and click the "Show more" button
                button = WebDriverWait(driver, 7).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Show more')]"))
                )
                button.click()
                print("About section clicked")
            except Exception as e:
                print(f"Failed to click 'Show more' initially: {e}")
                # Scroll down to retry
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
                try:
                    # Try to click the button again
                    button = WebDriverWait(driver, 25).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Show more')]"))
                    )
                    button.click()
                    print("About section clicked after retry")
                except Exception as e:
                    print(f"Retry to click 'Show more' failed: {e}")
                
            
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, 0);")
    
        print("Scrolled to bottom and back to top.")
    
        button_xpath = "//button[contains(@class, 'show-all-button')]//span[contains(text(), ' ')]"
    
        WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.XPATH, button_xpath))
        )
    
        button_elements = driver.find_elements(By.XPATH, button_xpath)
        print(f"Found {len(button_elements)} button elements.")
    
        for i, button_element in enumerate(button_elements):
            print(f"Processing button {i+1}/{len(button_elements)}")
            driver.execute_script("arguments[0].scrollIntoView(true);", button_element)
            WebDriverWait(driver, 3).until(
                EC.visibility_of(button_element)
            )
            moveToElement(driver, button_element)
            driver.execute_script("arguments[0].click();", button_element)
            print(f"Clicked button {i+1}/{len(button_elements)}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
    show_more_btn = "//span[contains(text(),'Show more')]"
    show_more_btns_elements = driver.find_elements(By.XPATH, show_more_btn)
    
    # time.sleep(1)
    for smbtnel in show_more_btns_elements:
        moveToElement(driver, smbtnel)  # Pass WebElement directly
        # time.sleep(1)
        try:
            smbtnel.click()
        except:
            pass
    driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
    
    try:
        # Scroll to the bottom of the page
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(random.uniform(2, 4))

    except:
        print("No 'Show all positions' button found.")
    
    driver.execute_script("window.scrollTo(0, 0);")
    # time.sleep(0.5)
    
        
        
        
        
    html_content = driver.page_source
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'spherical-list-284723-216944ab15f1.json'

    # Define the variables
    bucket_name = 'data-processing-html'
    # html_content = driver.page_source
    # file_name = id_pers + '.html'  # Specify the desired file name

    # Call the upload function
    # bucket_name = 'data-processing-html'
    # sr_id = 'ABC123'
    html_content = driver.page_source
    data_to_save = {"saleID": saleID, "profile_li_id":person_linkedin_id,"prof_id":SrID}
    
    upload_html_and_json(bucket_name, SrID, html_content, data_to_save)
            
    status = "worked"
    print("status :: ", status)
        
    
    return status
    
    
        

# if __name__ == '__main__':
#     username = "ramichoucair@yahoo.com"
#     password = "C@P!tlogistics"
#     driver = login(username, password)
#     saleID = "https://www.linkedin.com/sales/lead/ACoAAEjxOjIBf46cVEwN58r5NvZ38zrW3a-l2fY,name,3us_"
#     srID = "DRTWENTY21+ALUMNI_NINA_TURKEY____useinsider_all__current__ACwAAEjxOjIBssOosfjRycgkKW_ozsJls49K-fY,OUT_OF_NETWORK,9nBr+03032025+39410794"
#     result = advanced_search_people_profile_html(driver, saleID, srID)
