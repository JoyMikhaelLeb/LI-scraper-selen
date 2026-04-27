#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 11:06:34 2024

@author: joy
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from advanced_search_ppl import get_advanced_search_people_profile

import re
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
import os
#from selenium.webdriver.common.action_chains import ActionChains
from loop_create_html_task import create_html_task
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
import random

from selenium.webdriver.common.keys import Keys
from advanced_search_ppl import sales_search
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector
#
from bs4 import BeautifulSoup as bs
from selenium.common.exceptions import TimeoutException
from utils import get_numericalID
import numpy as np
import random
from google.cloud import storage
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

    chrome_options.add_argument("--incognito")

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

def create_target_folder(bucket_name, target):
    
   
    # Initialize a storage client
    client = storage.Client()
    
    # Get the bucket
    bucket = client.bucket(bucket_name)
    
    # Define the folder path
    folder_path = "entities_all_employees_history/entities/"
    target_folder_path = f"{folder_path}{target}/"
    
    # Check if the target folder exists by listing blobs with the folder prefix
    blobs = list(client.list_blobs(bucket_name, prefix=target_folder_path, delimiter='/'))
    
    # Check if the target folder exists within the "entities" folder
    target_exists = any(blob.name == target_folder_path for blob in blobs)
    
    if not target_exists:
        # Create the target folder
        target_folder_blob = bucket.blob(target_folder_path)
        target_folder_blob.upload_from_string('')
        print(f"Target folder '{target}' created within the 'entities' folder.")
    else:
        print(f"Target folder '{target}' already exists within the 'entities' folder.")
    
    return target_folder_path



def upload_dict_to_gcs_entities(bucket_name, folder_name, file_name, dictionary):
    # Initialize a storage client
    client = storage.Client()
    
    # Get the bucket
    bucket = client.bucket(bucket_name)
    
    # Convert the dictionary to a JSON string
    json_str = json.dumps(dictionary)
    
    # Define the blob (file) path
    blob_path = f"{folder_name}/{file_name}"
    
    # Create a blob
    blob = bucket.blob(blob_path)
    
    # Upload the JSON string to the blob
    blob.upload_from_string(json_str, content_type='application/json')
    
    print(f'File {file_name} uploaded to folder {folder_name} in bucket {bucket_name}.')

def upload_dict_to_gcs_employees(bucket_name, folder_name, file_name,dictionary):
    client = storage.Client()
    
    # Get the bucket
    bucket = client.bucket(bucket_name)
    
    # Convert the dictionary to a JSON string
    json_str = json.dumps(dictionary)
    
    # Define the blob (file) path
    blob_path = f"{folder_name}/{file_name}"
    
    # Create a blob
    blob = bucket.blob(blob_path)
    
    # Upload the JSON string to the blob
    blob.upload_from_string(json_str, content_type='application/json')
    
    print(f'File {file_name} uploaded to folder {folder_name} in bucket {bucket_name}.')

    
    
    
    

def extract_identifier(url):
    # Use regex to match the identifier part of the URL
    match = re.search(r'lead/([^,]+),', url)
    return match.group(1) if match else None

def moveToElement(driver, target_xpath):
    
    try:
        target = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
        ActionChains(driver).move_to_element(target).perform()
        return True
    except:
        return False
    
def get_linkedin_link(driver,sales_url):
        query = db.collection_group('ppl_search_advanced').where('profile_link', '==', sales_url)
        docs_ref = query.stream()
        linkedin_profile_link = None  # Initialize with None if no matching document is found
        linkedin_to_return = ""
        for doc in docs_ref:
            data = doc.to_dict()
            profile_linkedin = data.get('processed', {}).get('result_main', {}).get('result', [{}])[0].get('person_linkedin_url')
            if profile_linkedin:
                linkedin_profile_link = profile_linkedin
                # print(profile_linkedin)
                break  
            
                if linkedin_profile_link is None:
                    linkedin_to_return = ""
                    
                else:
                    linkedin_to_return = linkedin_profile_link
            
            
        return linkedin_to_return
            
            
            
    
    
        
def get_past_and_current_advanced(driver, db,target):
    temp=get_numericalID(driver,db,target)
    current_search_link = "https://www.linkedin.com/sales/search/people?query=(recentSearchParam%3A(doLogHistory%3Atrue)%2Cfilters%3AList((type%3ACURRENT_COMPANY%2Cvalues%3AList((id%3Aurn%253Ali%253Aorganization%253A"+temp+"%2Ctext%3A"+target+"n%2CselectionType%3AINCLUDED)))))&sessionId=ECH5dv%2BUSj%2BZsA5l32tr2Q%3D%3D"
    current_result = sales_search(driver, current_search_link, False, 100)
    
    employeescurrent = current_result[0]
    formatted_employees_current = []
    
    for emp_current in employeescurrent:
        sales_url_current = emp_current['person_sales_url']
        
        sales_linkedin_current = get_linkedin_link(driver, sales_url_current)
        
        if sales_linkedin_current != "" :
            person_id_current = sales_linkedin_current.split("/in/")[1]
            sales_linkedin_current = sales_linkedin_current
        else:
            person_id_current = ""
            sales_url_current = sales_url_current
        formatted_employees_current.append({
            "id": person_id_current,
            "sn_ID": sales_url_current
        })
    
        current_employees_dict = {"current_employees": formatted_employees_current}
        
    past_result_link = "https://www.linkedin.com/sales/search/people?query=(recentSearchParam%3A(doLogHistory%3Atrue)%2Cfilters%3AList((type%3APAST_COMPANY%2Cvalues%3AList((id%3Aurn%253Ali%253Aorganization%253A"+temp+"%2Ctext%3A"+target+"n%2CselectionType%3AINCLUDED)))))&sessionId=ECH5dv%2BUSj%2BZsA5l32tr2Q%3D%3D"
    past_result = sales_search(driver, past_result_link, False, 100)
    employeespast = past_result[0]
    formatted_employees_past = []
    
    for emp_past in employeespast:
        sales_url_past = emp_past['person_sales_url']
        sales_linkedin_past = get_linkedin_link(driver, sales_url_past)
        if sales_linkedin_past != "" :
            person_id_past = sales_linkedin_past.split("/in/")[1]
            sales_url_past = sales_url_past
        else:
            person_id_past = ""
            sales_linkedin_past=sales_linkedin_past
        formatted_employees_past.append({
            "id": person_id_past,
            "sn_ID": sales_url_past
        })
    
        past_employees_dict = {"past_employees": formatted_employees_past}
        
            
        
    combined_result_to_return = {**current_employees_dict, **past_employees_dict}
    return combined_result_to_return
        
        
def get_sn_employees_movements(driver, target):
    
    bucket_name = 'data-processing-html'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'spherical-list-284723-216944ab15f1.json'
    
    create_target_folder(bucket_name, target)
    
    
    
    
    # Define the variables
    bucket_name = 'data-processing-html'
    folder_name = 'entities_all_employees_history/entities/'+target  
    file_name = target + '.json'
    
    result_of_advanced_search = get_past_and_current_advanced(driver, db, target)
    data = result_of_advanced_search
    base_url = 'https://www.linkedin.com/sales/lead/'
    for category in data:
        for employee in data[category]:
            employee['sn_ID'] = employee['sn_ID'].replace(base_url, '')

    result_of_advanced_search_to_bucket = data
    upload_dict_to_gcs_entities(bucket_name, folder_name, file_name, result_of_advanced_search_to_bucket)
    
    
        
    for one_result in result_of_advanced_search_to_bucket['current_employees']:
        # print(one_result)
        # break
        if one_result['id'] == '':
            create_html_task("sn", one_result["sn_ID"])
            
        else:
            bucket_name = 'data-processing-html'
            folder_name = 'entities_all_employees_history/employees'
            file_name = one_result['id'] + '.json'
            upload_dict_to_gcs_employees(bucket_name, folder_name, file_name,one_result)
            
            
    for one_result in result_of_advanced_search_to_bucket['past_employees']:
        # print(one_result)
    
        if one_result['id'] == '':
            create_html_task("sn", one_result["sn_ID"])
            
        else:
            bucket_name = 'data-processing-html'
            folder_name = 'entities_all_employees_history/employees'
            file_name = one_result['id'] + '.json'
            upload_dict_to_gcs_employees(bucket_name, folder_name, file_name,one_result)
    
# if __name__ == '__main__':
    
# # # # # # # # # #         time_Start = time.asctime()
        
#         username="luciekhodeir@gmail.com"
#         password="louss76139135"                       
#         driver=login(username, password) 
#         target_full = "perplexity-ai__****__30"
#         target = target_full.split("__****__")[0]
