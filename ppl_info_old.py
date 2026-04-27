#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 2022 16:03:38 2022

@author: joy
"""
import json
# import pandas as pd
import numpy as np
from utils import clean_name,remove_more_emoji
import time
import datetime
from random import randint
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.selector import Selector
from bs4 import BeautifulSoup as bs
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

if not firebase_admin._apps:
    cred = credentials.Certificate('key.json')
    default_app = firebase_admin.initialize_app(cred)

db = firestore.client()



#Not used. Can be removed

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

    driver.find_element_by_xpath("//div[contains(@class,'login__form_action_container')]//*[contains(@aria-label, 'Sign in')]").click()


    time.sleep(2 + randint(1, 3))

    return driver

def moveToElement(driver, target_xpath):

    try:
        target = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
        ActionChains(driver).move_to_element(target).perform()
        return True
    except TimeoutException:
        return False



def get_updated_Link_and_Website(numerical_linkedin_id):

    coll_ref = db.collection("entities")
    docs = [
        snapshot
        for snapshot in coll_ref.limit(250)
        .where( "about.numericLink", "==", numerical_linkedin_id
            ).stream()

        ]

    if len(docs) !=0:
        if len(docs) > 1:
            print("Duplicates!!!! duplicated docs for 'numericLink'="+numerical_linkedin_id)
        for doc in docs:
            docum_out = doc.to_dict()
            break

            try:
                #if there is updated_link
                company_linkedin_url = docum_out['about']['updated_Link']
                try:
                     company_url = docum_out['about']['Website']
                except :
                    return company_linkedin_url, ""
            except :
                return "",""


        return company_url, company_linkedin_url


def getWebsite(driver,company_linkedin_url):
    try:
        driver.get(company_linkedin_url)
        time.sleep(random.uniform(1,5))
    except TimeoutException:
        print("Here's the timeout in experience. Refreshing...")
        driver.refresh()
        driver.get(company_linkedin_url)
        time.sleep(random.uniform(1,5))
    
    
    
    try:
        try:
            target_xpath = "//section[@class='org-top-card artdeco-card']"
            target = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
            ActionChains(driver).move_to_element(target).perform()
        except:
            target_xpath = "//section[@class='org-top-card-listing artdeco-card']"
            target = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
            ActionChains(driver).move_to_element(target).perform()
            
        
    except TimeoutException:
        print("## Org page didnt load")    
        return None
    
    
    try:
        website_found = driver.find_element_by_xpath("//a[@class='ember-view org-top-card-primary-actions__action']").get_attribute("href")    
        try:
            website_found = website_found.rstrip("/")
        except:
            website_found = website_found
    except:
        website_found = ""
    
    
    driver.execute_script("window.history.go(-1)")
    # time.sleep(1 + randint(1, 2))
        
    return website_found




def getURL(driver, linktoClick):
     
    
    try:
        driver.get(linktoClick)
        time.sleep(random.uniform(1, 5))
    except TimeoutException:
        print("Here's the timeout in experience. Refreshing...")
        driver.refresh()
        
        driver.get(linktoClick)
        time.sleep(random.uniform(1, 5))
        
    
    try:
        try:
            target_xpath = "//section[@class='org-top-card artdeco-card']"
            target = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
            ActionChains(driver).move_to_element(target).perform()
        except:
            target_xpath = "//section[@class='org-top-card-listing artdeco-card']"
            target = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
            ActionChains(driver).move_to_element(target).perform()
        
    except:
        if '/unavailable/' in driver.current_url:
            company_not_numerical = driver.current_url
            
        else:        
            print("## Org page didnt load")    
            return None
    
    
  
    # driver.execute_script("window.open('"+linktoClick+"', 'new_window')")

    # driver.switch_to.window(driver.window_handles[-1])
    company_not_numerical = driver.current_url
    if '/about/' in company_not_numerical:
        company_not_numerical = company_not_numerical.split("/about/")[0]
    else:
        company_not_numerical = company_not_numerical.rstrip("/")
    print("### company_not_numerical:", company_not_numerical)
    # driver.close()
    driver.execute_script("window.history.go(-1)")
    time.sleep(random.uniform(1, 3))
   
    return company_not_numerical




def extract_exp_model1(driver, soup, company_name):
    transliteration_mapping = {
    'С': 'C',
    'Е': 'E'
    }


    company_description = ""

    list_of_employements = ['Full-time','Part-time','Self-employed','Freelance','Contract','Internship','Apprenticeship','Seasonal']
    
    title = soup.find("div",{"class":"display-flex flex-wrap align-items-center full-height"})
    # print(title)
    
    if title is None:
        title = None
    
    elif len(title.findChildren("span"))==0:
        title= None
    elif title.findChildren("span")[1].text == " ":
        title2 = soup.select('.display-flex.align-items-center.mr1.t-bold')
        for ttle in title2:
            # print(ttle)
            title = ttle.findChildren("span")[0].text 
            if title == ' ':
                title = None
        
        
    else:
        try:
            title = title.findChildren("span")[1].text 
        except :
            
            title = None
        
        if title is not None:
            if any(char >= '\u4e00' and char <= '\u9fff' for char in title):
                # Check for Chinese characters (Unicode range for Chinese)
                title = title
            elif any(char >= '\uac00' and char <= '\ud7af' for char in title):
            # Check for Korean characters (Unicode range for Hangul)
                title = title
            elif any(char >= '\u0E00' and char <= '\u0E7F' for char in title):
                # Check for Thai characters (Unicode range for Thai)
                title = title
                
            elif any('\u4E00' <= char <= '\u9FBF' for char in title):
                title = title
                
            elif any('\u30A0' <= char <= '\u30FF' or '\uFF65' <= char <= '\uFF9F' for char in title):
                title = title
            
           
            elif any(char.isalpha() for char in title) == True:
                re.sub(r'[^A-Za-z0-9 ]+', ' ', title)
            
            elif any(char.isalpha() for char in title) == False  :
                if all(char.isdigit() for char in title):
                    title = title
                else:
                    title = None
            if title is not None :
                title = title.replace("  "," ")
            
           
            if title is not None :
                title = title.lower()
                
                if 'stealth company' in title or 'stealth' in title:
                    if 'stealth company' in title:
                        title = title.replace("stealth company","")
                    else:
                        title = title.replace("stealth","")
                
    
    company_url = "-"   

    period = soup.find("span",{"class":"t-14 t-normal t-black--light"})
    if period is not None:
        period = period.findChildren("span")[0]
        period = period.text
    else:
        period = ""
 
    
    if period is not None:
        # period = period.split("\nDates Employed\n")[1].replace("\n","")

        period_split = period.split("- ")
        period_start = period_split[0]
        if '\n' in period_start:
            period_start = period_start.replace("\n","")
        
        if '·' in period_start:
            period_start = period_start.split("·")[0]
            
        try:
            period_end = period_split[1]
            if ' · ' in period_end:
                period_end = period_end.split(" · ")[0]
            
        except :
            period_end = ""
            
        

    else:
        period_start = ""
        period_end = ""

    
    
    employment_type = soup.find("span",{"class":"t-14 t-normal"})
    if employment_type is None:
        employment_type = None
                
                
    else:
        employment_type= employment_type.findChildren("span")[1].text
    
    
    if employment_type is not None and ' · ' in employment_type:
        employment_type = employment_type.split(" · ")[1]
    else:
        employment_type = None
    
    if employment_type in list_of_employements:
        employment_type = employment_type
        
    else:
        employment_type = None
        
    
    
    try:
        company_description_elements = soup.find('div', class_='display-flex align-items-center t-14 t-normal t-black')
        if company_description_elements :
            try:
                company_description = company_description_elements.find('span', {'aria-hidden': 'true'}).get_text(strip=True)
            except:
                company_description = ""
     
    except :
        company_description = ""
         
    try:
        media = soup.find("img",{"class":"pvs-thumbnail__image lazy-image ember-view"})['src']
    except :
        media = ""
    
    company_logo_link = ""
    try:
        for EachPart in soup.select('img[class*="EntityPhoto-square"]'):
             company_logo_link = EachPart['src']
        # company_logo_link = soup.find("img",{"class":"ivm-view-attr__img--centered EntityPhoto-square-3   evi-image lazy-image ember-view"})['src']
       
    except :
        company_logo_link = ""
        
    
    try:
            for link in soup.find_all('a', href=True):
            
                numerical_linkedin_id = link['href']
                numerical_linkedin_id = numerical_linkedin_id.rstrip("/")
                
            if '/search/results/all' in numerical_linkedin_id:
                numerical_linkedin_id = ''
            
            elif '/details/experience/' in numerical_linkedin_id:
                numerical_linkedin_id = soup.find("a",{"class":"optional-action-target-wrapper"})['href']
                numerical_linkedin_id = numerical_linkedin_id.rstrip("/")

            elif '/linkedin' not in numerical_linkedin_id:
                try:
                    numerical_linkedin_id = soup.find("a",{"class":"optional-action-target-wrapper"})['href']
                    numerical_linkedin_id = numerical_linkedin_id.rstrip("/")
                except :
                    numerical_linkedin_id = ""
                    
            else:
                print("problem in numerical_linkedin_id ")
            
                
    
    
    except :
        
        numerical_linkedin_id = ""   
        
    # print(numerical_linkedin_id)
    # print("           ",numerical_linkedin_id)
    try:
        experience_location = soup.find_all('span', class_="t-14 t-normal t-black--light")[1].find_next('span').get_text()
    except :
        experience_location = ""
        
    page_size = 250
    coll_ref = db.collection("entities")
    if numerical_linkedin_id =="":
        company_linkedin_url = ""
        # return [title,company_name,period_start,period_end,company_description,company_logo_link,company_linkedin_url,company_url]
    elif numerical_linkedin_id != "":
            # type(coll_ref)
            #direct search
            docs = [
                snapshot
                for snapshot in coll_ref.limit(page_size)
                .where( "about.numericLink", "==", numerical_linkedin_id
                    ).stream()
                
                ]
            
            
            if len(docs) !=0:
                if len(docs) > 1:
                    print("Duplicates!!!! duplicated docs for 'numericLink'="+numerical_linkedin_id)
                for doc in docs:
                    # print(doc.to_dict())
                    docum_out = doc.to_dict()
                    
                    
                    try:
                        #if there is updated_link
                        company_linkedin_url = docum_out['about']['updated_Link']
                        try:
                            company_url = docum_out['about']['Website']
                        except :
                            company_url = "-"
                        
                    
                    except :
                        #if there is no updated_Link
                        company_linkedin_url = getURL(driver, numerical_linkedin_id)
                        if company_linkedin_url == None   :
                            print("company_linkedin_url==None")
                            continue
                        print("company_linkedin_url: ",company_linkedin_url)
                        try:
                            target_xpath = "//div[@class='pvs-list__container']"
                            target = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
                            ActionChains(driver).move_to_element(target).perform()
                        except TimeoutException :
                            print("education URL clicked but education page didnt load again")
                            
                        if company_linkedin_url !="https://www.linkedin.com/company/unavailable/" or company_linkedin_url!=None:
                            try:
                                company_db_id = company_linkedin_url.split("/company/")[1].rstrip("/")
                            except :
                                try:
                                    company_db_id = company_linkedin_url.split("/school/")[1].rstrip("/")
                                except :
                                    company_db_id = company_linkedin_url.split("/showcase/")[1].rstrip("/")
                                
                                    
                            about = {
                                    'about': {'updated_Link':company_linkedin_url,'date_collected':datetime.date.today().strftime("%d-%b-%y")}
                                    }
                            db.collection(u'entities').document(company_db_id).set(about,merge=True)
                        
            else:          
                
                #if there is no numericLink at all
                numericLink = numerical_linkedin_id
                company_linkedin_url = getURL(driver, numerical_linkedin_id)
                if company_linkedin_url == "https://www.linkedin.com/company/unavailable":
                    company_linkedin_url = None
                if company_linkedin_url != None:
                        
                    try:
                        target_xpath = "//div[@class='pvs-list__container']"
                        target = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
                        ActionChains(driver).move_to_element(target).perform()
                    except TimeoutException :
                        print("expe. URL clicked but education page didnt load again")
                    
                    
                    if company_linkedin_url !="https://www.linkedin.com/company/unavailable":

                        try:
                            company_db_id = company_linkedin_url.split("/company/")[1].rstrip("/")
                        except :
                            try:
                                company_db_id = company_linkedin_url.split("/school/")[1].rstrip("/")
                            except :
                                company_db_id = company_linkedin_url.split("/showcase/")[1].rstrip("/")
                            
                
                        if '/about' in company_db_id:
                            company_db_id = company_db_id.replace("/about","")
                        about = {
                            'about': {'date_collected':datetime.date.today().strftime("%d-%b-%y"),'numericLink':numericLink,'updated_Link':company_linkedin_url},'last_updated':datetime.datetime.utcnow(),'id':company_db_id
                                        }
                        db.collection(u'entities').document(company_db_id).set(about,merge=True)  
                
            
        
    else:
        print("check numerical_id")            
    # print("    ",numerical_linkedin_id)
    if 'resent' in period_end and numerical_linkedin_id!= "" and company_linkedin_url !=None:
       
        page_size = 250
        coll_ref = db.collection("entities")
        docs = [
                snapshot
                for snapshot in coll_ref.limit(page_size)
                .where( "about.numericLink", "==", numerical_linkedin_id
                    ).stream()
                
                ]
                
                
        if len(docs) !=0:
            if len(docs) > 1:
                print("Duplicates!!!! duplicated docs for 'numericLink'="+numerical_linkedin_id)
            for doc in docs:
                docum_out = doc.to_dict()
                try:
                    #if there is website in doc_out
                    company_url = docum_out['about']['Website']
                    
                except:
                    #if there is no website in doc_out
                    company_url = getWebsite(driver,numerical_linkedin_id)
                    if company_url!="" or company_url!=None :
                    
                        try:
                            company_db_id = company_linkedin_url.split("/company/")[1].rstrip("/")
                        except :
                            try:
                                company_db_id = company_linkedin_url.split("/school/")[1].rstrip("/")
                            except :
                                company_db_id = company_linkedin_url.split("/showcase/")[1].rstrip("/")
                            
                    
                        if 'about' in company_db_id:
                            company_db_id = company_db_id.replace("/about","")
                        about = {
                            'about': {'Website':company_url,'date_collected':datetime.date.today().strftime("%d-%b-%y")},'last_updated':datetime.datetime.utcnow(),'id':company_db_id
                                        }
                        db.collection(u'entities').document(company_db_id).set(about,merge=True)
                    # return [title,company_name,period_start,period_end,company_description,company_logo_link,company_linkedin_url,company_url,media,experience_location,company_url]
                    
        else:
            company_url = getWebsite(driver,numerical_linkedin_id)
            if company_linkedin_url == "https://www.linkedin.com/company/unavailable":
                company_linkedin_url = None
            if company_linkedin_url != None:
                try:
                    target_xpath = "//div[@class='pvs-list__container']"
                    target = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
                    ActionChains(driver).move_to_element(target).perform()
                except TimeoutException:
                    print("exp URL clicked but education page didnt load again")
                try:
                    company_db_id = company_linkedin_url.split("/company/")[1].rstrip("/")
                except :
                    try:
                        company_db_id = company_linkedin_url.split("/school/")[1].rstrip("/")
                    except :
                        company_db_id = company_linkedin_url.split("/showcase/")[1].rstrip("/")
                    
                    
                
                if 'about' in company_db_id:
                    company_db_id = company_db_id.replace("/about","")
                
                    
                
                    
                        
                about = {
                        'about': {'updated_Link':company_linkedin_url,'date_collected':datetime.date.today().strftime("%d-%b-%y")}
                        }
                db.collection(u'entities').document(company_db_id).set(about,merge=True)
                
            # return [title,company_name,period_start,period_end,company_description,company_logo_link,company_linkedin_url,company_url,media,experience_location,company_url]
        
    
    else:
        company_url = ''
        # return [title,company_name,period_start,period_end,company_description,company_logo_link,company_linkedin_url,company_url,media,experience_location]
           
        
            
            
 
    return [title,company_name,period_start,period_end,company_description,company_logo_link,company_linkedin_url,company_url,media,experience_location,employment_type]





def extract_exp_model2(driver, soup, company_name):
    list_of_employements = ['Full-time','Part-time','Self-employed','Freelance','Contract','Internship','Apprenticeship','Seasonal']
    my_list=[]
    company_url = '-'
    company_description = ""
    roles=soup.find_all("li",class_="pvs-list__paged-list-item")
    
    for role in roles:

        title = role.find("div",{"class":"display-flex flex-wrap align-items-center full-height"})
        
    
        if title is None:
            title = None
        
        elif len(title.findChildren("span"))==0:
            title= None
        elif title.findChildren("span")[1].text == " ":
            title2 = role.select('.display-flex.align-items-center.mr1.t-bold')
            for ttle in title2:
                # print(ttle)
                title = ttle.findChildren("span")[0].text 
                if title == ' ':
                    title = None
        else:
            try:
                title = title.findChildren("span")[1].text
            except :
                title= None
            
            if title is not None:
                if any(char >= '\u4e00' and char <= '\u9fff' for char in title):
                    # Check for Chinese characters (Unicode range for Chinese)
                    title = title
                elif any(char >= '\uac00' and char <= '\ud7af' for char in title):
                # Check for Korean characters (Unicode range for Hangul)
                    title = title
                elif any(char >= '\u0E00' and char <= '\u0E7F' for char in title):
                    # Check for Thai characters (Unicode range for Thai)
                    title = title
                    
                elif any('\u4E00' <= char <= '\u9FBF' for char in title):
                    title = title
                    
                elif any('\u30A0' <= char <= '\u30FF' or '\uFF65' <= char <= '\uFF9F' for char in title):
                    title = title
                
               
                elif any(char.isalpha() for char in title) == True:
                    re.sub(r'[^A-Za-z0-9 ]+', ' ', title)
                
                elif any(char.isalpha() for char in title) == False  :
                    if all(char.isdigit() for char in title):
                        title = title
                    else:
                        title = None
                if title is not None :
                    title = title.replace("  "," ")
           
            if title is not None:
                title = title.lower()
                
                if 'stealth company' in title or 'stealth' in title:
                    if 'stealth company' in title:
                        title = title.replace("stealth company","")
                    else:
                        title = title.replace("stealth","")
                    
        if title == " ":
            title = None
        period = role.find('span',{"class":"t-14 t-normal t-black--light"}).findChildren("span")[1].text
         
        
    
        if period is not None:
            
            period_split = period.split(" to ")
            period_start = period_split[0]
            if '·' in period_start:
                period_start = period_start.split("·")[0]
            try:
                period_end = period_split[1].split("·")[0]
            except :
                period_end = ""
    
        else:
            period_start = ""
            period_end = ""
    
        try:
            employment_type = role.find('span',{"class":"t-14 t-normal"}).findChildren("span")[0].text
            
        
        except:
            employment_type = None
            
        if employment_type == None:
            try:
                employment_type = soup.find("span",{"class":"t-14 t-normal"}).findChildren("span")[0].text
                try:
                    employment_type = employment_type.split(" · ")[0]
                except:
                    employment_type = employment_type
            except:
                employment_type = None
        
        if employment_type in list_of_employements:
            employment_type = employment_type
        else:
            employment_type = None
        
        
        company_description_elements = role.find('div', class_='display-flex align-items-center t-14 t-normal t-black')
        if company_description_elements:
            try:
                company_description = company_description_elements.find('span', {'aria-hidden': 'true'}).get_text(strip=True)
            except:
                company_description = ""
     
             
        company_logo_link = ""   
        try:
            for EachPart in soup.select('img[class*="EntityPhoto-square"]'):
                 company_logo_link = EachPart['src']
            # company_logo_link = soup.find("img",{"class":"ivm-view-attr__img--centered EntityPhoto-square-3   evi-image lazy-image ember-view"})['src']
           
        except :
            company_logo_link = ""
        
    
        try:
             media = soup.find("img",{"class":"pvs-thumbnail__image lazy-image ember-view"})['src']
        except :
             media = ""
        try:
            for link in soup.find_all('a', href=True):
            
                numerical_linkedin_id = link['href']
                numerical_linkedin_id = numerical_linkedin_id.rstrip("/")
                
            if '/search/results/all' in numerical_linkedin_id:
                numerical_linkedin_id = ''
            
            elif '/details/experience/' in numerical_linkedin_id:
                numerical_linkedin_id = soup.find("a",{"class":"optional-action-target-wrapper"})['href']
                numerical_linkedin_id = numerical_linkedin_id.rstrip("/")

            elif '/linkedin' not in numerical_linkedin_id:
                try:
                    numerical_linkedin_id = soup.find("a",{"class":"optional-action-target-wrapper"})['href']
                    numerical_linkedin_id = numerical_linkedin_id.rstrip("/")
                except :
                    numerical_linkedin_id = ""
    
        except:
            numerical_linkedin_id = ""   
            
            
        # print("           ",numerical_linkedin_id) 
        try:
            experience_location = soup.find_all('span', class_="t-14 t-normal t-black--light")[1].find_next('span').get_text()
            if "- " in experience_location:
                experience_location = ""
        
        except :
            experience_location = ""
            
            
        print(numerical_linkedin_id)   
        page_size = 250
        coll_ref = db.collection("entities")
        if numerical_linkedin_id =="":
            company_linkedin_url = ""
            # return [title,company_name,period_start,period_end,company_description,company_logo_link,company_linkedin_url,company_url]
        elif numerical_linkedin_id != "":
               
                #direct search
                docs = [
                    snapshot
                    for snapshot in coll_ref.limit(page_size)
                    .where( "about.numericLink", "==", numerical_linkedin_id
                        ).stream()
                    
                    ]
                if len(docs) !=0:
                    
                    for doc in docs:
                        docum_out = doc.to_dict()
                        
                        
                        try:
                            #if there is updated_link
                            company_linkedin_url = docum_out['about']['updated_Link'].split("/about/")[0]
                            try:
                                company_url = docum_out['about']['Website']
                            except :
                                company_url = "-"
                        except :
                            #if there is no updated_Link
                            company_linkedin_url = getURL(driver, numerical_linkedin_id)
                            if company_linkedin_url == "https://www.linkedin.com/company/unavailable":
                                company_linkedin_url = None
                            if company_linkedin_url != None:
                                try:
                                    target_xpath = "//div[@class='pvs-list__container']"
                                    target = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
                                    ActionChains(driver).move_to_element(target).perform()
                                except TimeoutException:
                                    print("exp URL clicked but education page didnt load again")
                                try:
                                    company_db_id = company_linkedin_url.split("/company/")[1].rstrip("/")
                                except :
                                    try:
                                        company_db_id = company_linkedin_url.split("/school/")[1].rstrip("/")
                                    except :
                                        company_db_id = company_linkedin_url.split("/showcase/")[1].rstrip("/")
                                    
                                    
                                
                                if 'about' in company_db_id:
                                    company_db_id = company_db_id.replace("/about","")
                                
                                    
                                
                                    
                                        
                                about = {
                                        'about': {'updated_Link':company_linkedin_url,'date_collected':datetime.date.today().strftime("%d-%b-%y")}
                                        }
                                db.collection(u'entities').document(company_db_id).set(about,merge=True)
                                
                else:          
                    
                    #if there is no numericLink at all
                    numericLink = numerical_linkedin_id
                    company_linkedin_url = getURL(driver, numerical_linkedin_id)
                    if company_linkedin_url == "https://www.linkedin.com/company/unavailable":
                                company_linkedin_url = None
                    if company_linkedin_url != None:
                        try:
                            target_xpath = "//div[@class='pvs-list__container']"
                            target = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
                            ActionChains(driver).move_to_element(target).perform()
                        except TimeoutException:
                            print("exp URL clicked but education page didnt load again")
                        try:
                            company_db_id = company_linkedin_url.split("/company/")[1].rstrip("/")
                        except :
                            try:
                                company_db_id = company_linkedin_url.split("/school/")[1].rstrip("/")
                            except :
                                company_db_id = company_linkedin_url.split("/showcase/")[1].rstrip("/")
                            
                            
                        
                        if 'about' in company_db_id:
                            company_db_id = company_db_id.replace("/about","")
                        
                            
                        
                            
                                
                        about = {
                                'about': {'updated_Link':company_linkedin_url,'date_collected':datetime.date.today().strftime("%d-%b-%y")}
                                }
                        db.collection(u'entities').document(company_db_id).set(about,merge=True)
                        
            
            
    
        else:
            print("check numerical_id")  
            
        # print("    ",numerical_linkedin_id)
        if 'resent' in period_end and numerical_linkedin_id!= "" and company_linkedin_url !=None:
            page_size = 250
            coll_ref = db.collection("entities")
            docs = [
                    snapshot
                    for snapshot in coll_ref.limit(page_size)
                    .where( "about.numericLink", "==", numerical_linkedin_id
                        ).stream()
                    
                    ]
                    
                    
            if len(docs) !=0:
                if len(docs) > 1:
                    print("Duplicates!!!! duplicated docs for 'numericLink'="+numerical_linkedin_id)
                for doc in docs:
                    docum_out = doc.to_dict()
                    try:
                        #if there is website in doc_out
                        company_url = docum_out['about']['Website']
                    except:
                        #if there is no website in doc_out
                        company_url = getWebsite(driver,company_linkedin_url)
                        if company_url!="" or company_url!=None:
                            try:
                                company_db_id = company_linkedin_url.split("/company/")[1].rstrip("/")
                            except :
                                try:
                                    company_db_id = company_linkedin_url.split("/school/")[1].rstrip("/")
                                except :
                                    company_db_id = company_linkedin_url.split("/showcase/")[1].rstrip("/")
                                
                            
                            if 'about' in company_db_id:
                                company_db_id = company_db_id.replace("/about","")
                            about = {
                                'about': {'Website':company_url,'date_collected':datetime.date.today().strftime("%d-%b-%y")},'last_updated':datetime.datetime.utcnow(),'id':company_db_id
                                            }
                            db.collection(u'entities').document(company_db_id).set(about,merge=True)
                        
            else:
                company_url = getWebsite(driver,company_linkedin_url)
                if company_url!="" or company_url!=None:
                    try:
                        company_db_id = company_linkedin_url.split("/company/")[1].rstrip("/")
                    except :
                        try:
                            company_db_id = company_linkedin_url.split("/school/")[1].rstrip("/")
                        except :
                            company_db_id = company_linkedin_url.split("/showcase/")[1].rstrip("/")
                        
                    
                    if 'about' in company_db_id:
                        company_db_id = company_db_id.replace("/about","")
                    about = {
                        'about': {'Website':company_url,'date_collected':datetime.date.today().strftime("%d-%b-%y")},'last_updated':datetime.datetime.utcnow(),'id':company_db_id
                                    }
                    db.collection(u'entities').document(company_db_id).set(about,merge=True)
                      
        else: #if not current company
            company_url = ""
                                       
        
        
        
        
        
        
        
        
        
        my_list.append([title,company_name,period_start,period_end,company_description,company_logo_link,company_linkedin_url,company_url,media,experience_location,employment_type])
        if my_list[0][1] is not None and my_list[0][1]!="":
            list_test_extra = re.sub(r'[^A-Za-z0-9 ]+', ' ', my_list[0][1].lower())
            
            if '  ' in list_test_extra:
                list_test_extra = list_test_extra.replace("  "," ")
           
            if my_list[0][1] is not None:
                if my_list[0][0] is not None:
                    if my_list[0][0].lower() ==list_test_extra:
                        del my_list[0]
            try:
                
                my_list = [entry for entry in my_list if entry[0].strip().lower() != entry[1].strip().lower()]
        
            except:
                my_list = [entry for entry in my_list if entry[0] != entry[1]]
        
    
    
        
    return my_list
     











def getExperience(driver, current_link):

    #print("current_link1:",current_link)
    try:
        driver.get(current_link + "details/experience/")
        time.sleep(random.uniform(5, 10))
    except TimeoutException:
        print("Here's the timeout in experience. Refreshing...")
        driver.refresh()
        time.sleep(random.uniform(5,9))
        driver.get(current_link + "details/experience/")
        time.sleep(random.uniform(5, 9))
    # try:
    #     target_xpath = "//h2[@class='artdeco-empty-state__headline artdeco-empty-state__headline--mercado-empty-room-large artdeco-empty-state__headline--mercado-spots-large']"
    #     if moveToElement(driver, target_xpath):
    #         experience = []
    #         experience_dict = {"experience":[]}

    #         #for ex in experience:
    #         #    experience_dict['experience'].append({"title":"", "company_name": "", "period_start": "", "period_end": "", "company_description": "","company_logo_link":"","company_linkedin_url":"","company_url":"","media":""})
    #         return experience_dict
    # except TimeoutException :
    #      experience_dict = {"experience":[]}

    #      return experience_dict
    try:
        # target_xpath = "//main[contains(@class,'scaffold-layout__main')]"
        target_xpath = "//main[@aria-label='Experience']"
        target = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
        ActionChains(driver).move_to_element(target).perform()
    
    except TimeoutException:
        print("experience didnt load")
        experience_dict = {"experience":[]}

    # try:
    #     target_xpath = "//ul[contains(@class,'pvs-list')]"
    #     target = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
    #     ActionChains(driver).move_to_element(target).perform()

    # except TimeoutException:
    #     print("experience didnt load, trying another path")
    #     experience_dict = {"experience":[]}
        # return experience_dict

    #print("current_link2:",current_link)

    
  
        
    showmore = "//button[@class='artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button']"
    while True and moveToElement(driver, showmore ) == True:
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    # driver.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button']").click()
        time.sleep(2 + randint(1, 3))
        print("clicked on more experiences")
    
        
    
    experience = []
    # driver.get(current_link + "details/experience/")
    selector = Selector(text=driver.page_source)
    try:
        experience_listcontainer = selector.xpath("//ul[contains(@class,'pvs-list')]")[0]
    # experience_listcontainer = selector.xpath("//ul[@class='pvs-list ']")[0]
    except:
        experience_listcontainer = selector.xpath("//main[contains(@aria-label,'Experience')]")
    experience_container = experience_listcontainer.xpath("//li[@class='pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated ']")
    if len(experience_container)==0:
        experience_container = experience_listcontainer.xpath("//li[contains(@class,'pvs-list__paged-list-item artdeco-list__item')]")
        
    
    
    model=1
    # count = 0
    for i in experience_container.extract():
        
        soup = bs(i, features="lxml")
        
        # count+=1
        # if count ==2:
        #     break
            
        # many_experiences = soup.find("span",{"class":"pvs-entity__path-node"})
        many_exp_css_selector = 'li.pvs-list__paged-list-item.pvs-list__item--one-column > div > span'
        
        # Find all matching elements
        many_experiences = soup.select(many_exp_css_selector)
        
        # Print out the found elements
        
        if len (many_experiences) !=0:
            company_name = soup.find("div",{"class":"display-flex flex-wrap align-items-center full-height"})
            if company_name is None:
                company_name = ""
                
            else:
                try:
                    company_name = company_name.findChildren("span")[1].text
                except:
                    company_name = ""
                
            if ' · ' in company_name:
                company_name = company_name.split(" · ")[0]

            model = 2
            
        else:
            
            company_name = soup.find("span",{"class":"t-14 t-normal"})
            
            if company_name is None:
                company_name = ""
                
                
            else:
                company_name= company_name.findChildren("span")[1].text
                
            if ' · ' in company_name:
                company_name = company_name.split(" · ")[0]
            # print(company_name)
            model =1
                
            # print(company_name)
                
                
                
            


        # print(company_name)
        try:
            if model==1:
                
                extracted_list=extract_exp_model1(driver, soup, company_name)
                
                experience.append([ extracted_list[0],extracted_list[1],extracted_list[2],extracted_list[3] ,extracted_list[4],extracted_list[5], extracted_list[6], extracted_list[7], extracted_list[8], extracted_list[9],extracted_list[10]])
                    
            elif model==2:
                
                extracted_lists=extract_exp_model2(driver, soup, company_name)
                for extracted_list in extracted_lists:
                    experience.append([ extracted_list[0],extracted_list[1],extracted_list[2],extracted_list[3] ,extracted_list[4],extracted_list[5], extracted_list[6], extracted_list[7], extracted_list[8], extracted_list[9],extracted_list[10]])
            elif model==3:
                
                extracted_list=extract_exp_model1(driver, soup, company_name)
                experience.append([ extracted_list[0],extracted_list[1],extracted_list[2],extracted_list[3] ,extracted_list[4],extracted_list[5], extracted_list[6], extracted_list[7], extracted_list[8], extracted_list[9],extracted_list[10]])
            else:
                print("no module defined, no experience extracted")
                

        except Exception as f:

            print("failure in extract_exp_model")
            # return -1
            print ("error in extracting model at line 743 ~",f)
            raise

    experience_dict = {"experience":[]}
    
    for ex in experience:
        experience_dict['experience'].append({"title":ex[0], "company_name": ex[1], "period_start": ex[2], "period_end": ex[3], "company_description": ex[4],"company_logo_link":ex[5],"company_linkedin_url":ex[6],"company_url":ex[7],"media":ex[8],"company_experience_location":ex[9],"employment_type":ex[10]})
        
    # for one_dict in experience_dict['experience']:
    #     print(one_dict)
    #     if 'resent' not in one_dict['period_end']:
    #         del one_dict["Website"]
            
    
    return experience_dict





def getEducation(driver,current_link):

    
    try:
        driver.get(current_link + "details/education/")
        time.sleep(random.uniform(5, 15))
    except TimeoutException :
        print("here's the timout in education,refreshing the page....")
        driver.refresh()
        time.sleep(random.uniform(5, 15))
        driver.get(current_link + "details/education/")
        time.sleep(random.uniform(5, 15))
        
    try:
        target_xpath = "//main[contains(@aria-label,'Education')]"
        target = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
        ActionChains(driver).move_to_element(target).perform()
    
    except TimeoutException:
        print("education didnt load")
        
        education = []
        educDict = {"education":[]}
        for ed in education:
            educDict['education'].append({"institution_name":"", "degree": "", "major": "", "education_start_year": "", "education_end_year": "","institution_linkedin_url": "","institution_logo_link":"","institution_url":""})
        return educDict
    # try:
    #     target_xpath = "//ul[contains(@class,'pvs-list')]"
    #     target = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
    #     ActionChains(driver).move_to_element(target).perform()
    # except TimeoutException:
    #     print("education didnt load, trying another path")
    #     experience_dict = {"experience":[]}
    #     # return experience_dict

    # #print("current_link2:",current_link)

   

    

    selector = Selector(text=driver.page_source)
    education = []
    educDict = {"education":[]}
    
    try:
        education_listcontainer = selector.xpath("//ul[contains(@class,'pvs-list')]")[0]
    # experience_listcontainer = selector.xpath("//ul[@class='pvs-list ']")[0]
    except:
        education_listcontainer = selector.xpath("//main[contains(@aria-label,'Education')]")
    education_container = education_listcontainer.xpath("//li[@class='pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated ']")
    if len(education_container)==0:
        education_container = education_listcontainer.xpath("//li[contains(@class,'pvs-list__paged-list-item artdeco-list__item')]")
        
    
    
    
    # education_listcontainer = selector.xpath("//ul[contains(@class,'pvs-list')]")[0]
    # //div[@class="pvs-list__container"]
    # if len(education_listcontainer) == 0:
    #     education_listcontainer = selector.xpath("//section[@class='artdeco-card pb3']")
    #     if len(education_listcontainer) == 0:
    #         educDict = {"education":[]}
    #         return educDict
    
    # education_container = education_listcontainer.xpath("//li[@class='pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated ']")
    # if len(education_container)==0:
    #     education_container = education_listcontainer.xpath("//li[@class='pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column']")
        
    
    
    
    for i in education_container.extract():

            soup = bs(i, features="lxml")
            institution_name = soup.find("div",{"class":"display-flex flex-wrap align-items-center full-height"})
            try:
                institution_name= institution_name.findChildren("span")[1].text
            except :
                institution_name=""
            major = ""
            edu_major = soup.find("span",{"class":"t-14 t-normal"})
            if edu_major != None:
                edu_major= edu_major.findChildren("span")[1].text
                edu_major = edu_major.split(",")
                degree = edu_major [0]

                if len(edu_major) > 1:
                    major = ','.join(edu_major [1:])
            else:
                major = ""
                degree = ""
           
            edu_year = soup.find("span",{"class":"t-14 t-normal t-black--light"})
                
                
            if edu_year is not None:
                edu_year= edu_year.findChildren("span")[1].text
                years = []
                years = edu_year.split(" - ")
#                     ys = edu_year.findAll("time")
#                     for i in ys:
# #                                print(i.text)
#                         years.append(i.text)
                education_start_year = years [0]
                try:
                    education_end_year = years [1]

                except:
                    education_end_year = ""

            if edu_year is None:
                education_start_year = ""
                education_end_year = ""
            
            
            
            institution_logo_link = ""
            try:
                for EachPart in soup.select('img[class*="EntityPhoto-square"]'):
                    institution_logo_link = EachPart['src']
            # institution_logo_link = soup.find("img",{"class":"ivm-view-attr__img--centered EntityPhoto-square-3   evi-image lazy-image ember-view"})
            # if institution_logo_link is None:
            #     institution_logo_link = ""
            # else:
            #     institution_logo_link = institution_logo_link['src']
            except:
                institution_logo_link = ""





            institution_url = "-"

            try:


                institution_linkedin = soup.find_all("div",class_="display-flex flex-row justify-space-between")

                for urlLinkedin in institution_linkedin:
                    try:
                        institution_linkedin_numerical = urlLinkedin.find('a')['href']
                        institution_linkedin_numerical = institution_linkedin_numerical.rstrip("/")
                    except:
                        institution_linkedin_numerical = ""
                if '/search/results/all/' in institution_linkedin_numerical:
                        institution_linkedin_numerical = ''

            except Exception as errors:
                print(errors)
                raise


            page_size = 250
            coll_ref = db.collection("entities")
            if institution_linkedin_numerical =="":
                institution_linkedin_url = ""
            if institution_linkedin_numerical != "":

                    #direct search
                    docs = [
                        snapshot
                        for snapshot in coll_ref.limit(page_size)
                        .where( "about.numericLink", "==", institution_linkedin_numerical
                            ).stream()

                        ]
                    if len(docs) !=0:
                        print("## len(docs) !=0: ")
                        if len (docs) >1 :
                            print("Duplicates . . ...")
                        for doc in docs:
                            docum_out = doc.to_dict()


                            try:
                                #if there is updated_link
                                institution_linkedin_url = docum_out['about']['updated_Link']
                                try:
                                    institution_url = docum_out['about']['Website']
                                except :
                                    institution_url = "-"

                            except :
                                #if there is no updated_Link
                                institution_linkedin_url = getURL(driver, institution_linkedin_numerical)
                                if institution_linkedin_url == None:
                                    continue
                                try:
                                    target_xpath = "//div[@class='pvs-list__container']"
                                    target = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
                                    ActionChains(driver).move_to_element(target).perform()
                                except TimeoutException:
                                    print("### education URL clicked but education page didnt load again")


                                try:
                                    inst_db_id = institution_linkedin_url.split("/school/")[1]
                                except :
                                    inst_db_id = institution_linkedin_url.split("/company/")[1]

                                if 'about' in inst_db_id:
                                    inst_db_id = inst_db_id.replace("/about","")


                                about = {
                                        'about': {'updated_Link':institution_linkedin_url,'date_collected':datetime.date.today().strftime("%d-%b-%y")}
                                        }
                                db.collection(u'entities').document(inst_db_id).set(about,merge=True)

                    else:
                        #print("### len(docs) == 0:")
                        #if there is no numericLink at all
                        numericINSTLink = institution_linkedin_numerical
                        institution_linkedin_url = getURL(driver, institution_linkedin_numerical)
                        if institution_linkedin_url == None:
                            continue
                        try:
                            target_xpath = "//div[@class='pvs-list__container']"
                            target = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
                            ActionChains(driver).move_to_element(target).perform()
                        except TimeoutException:
                            print("education URL clicked but education page didnt load again")
                        try:
                            inst_db_id = institution_linkedin_url.split("/school/")[1]
                        except :
                            inst_db_id = institution_linkedin_url.split("/company/")[1]

                        if '/about' in inst_db_id:
                            inst_db_id = inst_db_id.replace("/about","")

                        about = {
                            'about': {'date_collected':datetime.date.today().strftime("%d-%b-%y"),'numericLink':numericINSTLink,'updated_Link':institution_linkedin_url},'last_updated':datetime.datetime.utcnow(),'id':inst_db_id
                                        }
                        print("@@@ for ",inst_db_id," about to update:", about)
                        db.collection(u'entities').document(inst_db_id).set(about,merge=True)





            education.append([institution_name,degree,major,education_start_year,education_end_year,institution_linkedin_url,institution_logo_link,institution_url])

            new_education = []
            for elem in education:
                if elem not in new_education:
                    new_education.append(elem)
                    education = new_education



            educDict = {"education":[]}



            for ed in new_education:
                educDict['education'].append({"institution_name":ed[0], "degree": ed[1], "major": ed[2], "education_start_year": ed[3], "education_end_year": ed[4],"institution_linkedin_url": ed[5],"institution_logo_link":ed[6],"institution_url":ed[7]})


    return educDict

def getinfowrongLink(driver,li_id):
    
    current_link = driver.current_url
    if '/profile-video' in current_link:
        current_link= current_link.split("/profile-video")[0]
    
    general = {"general":''}
    general['general'] = {"linkedin_url":current_link, "name": "", "header":"","location":"", "profile_pic_link":"",'prounouns':"",'numberOfConnections':0}
    
    contact_info = {"contact_info":''}
    contact_info['contact_info'] = {"email":"", "websites": "", "twitter":"","phone":"","birthday":"","error":""}
    
    experience_result = {"experience":[]}
    experience_result['experience'].append({"title":"", "company_name": "", "period_start": "", "period_end": "", "company_description":"","company_logo_link":"","company_linkedin_url":"","company_url":"","media":"","company_experience_location":""})
    
    education_result = {"education":[]}
    education_result['education'].append({"institution_name":"", "degree": "", "major": "", "education_start_year": "", "education_end_year": "","institution_linkedin_url": "","institution_logo_link":"","institution_url":""})

    
    informationDict = {**general, **contact_info, **experience_result, **education_result}
    informationDict["id"]= current_link.split("https://www.linkedin.com/in/")[1].split("/")[0]
    print("informationDict:",informationDict)
    return informationDict
    
    
def getProfileInfo(driver,link):

    current_link = driver.current_url
    strings_to_remove = ["recruiting", "Recruiting", "We are Hiring", "We're Hiring"]
    pronouns_list=['He/Him','she/her','She/Her','he/him','HE/HIM','SHE/HER','she/they','he/they','they/them','he/she','he/she/they']
    to_replace_with_space=['-','(',')']
    
    current_link="https://www.linkedin.com/in/"+current_link.split("https://www.linkedin.com/in/")[1].split("/")[0]+"/"

    #in testing
    #print("current_link:",current_link)
    #current_link = current_link.split("/")[0]+"/"

    name = ""
    header = ""
    location = ""
    profile_pic_link = ""

  
    try:
        name = driver.find_element_by_xpath("//h1[contains(@class,'align-middle break-words')]").text

        name = re.sub(r'[^A-Za-z0-9 ]+', ' ', name)
        if '  ' in name:
           name = name.replace("  "," ")
            
    except:
        name =""
        print("no name")

    if name == "":
        name_to_return = ""
        prounouns = ""
        person_name_to_return = ""
    if name != "":
        try:
            prounouns = driver.find_elements_by_xpath("//div[@class='mt2 relative']/div/div/span[@class='text-body-small v-align-middle break-words t-black--light']")[0].text.replace(")","").replace("(","")

        except:
            name_to_check = name.lower()
            for pronun in pronouns_list:
                # print (pronun)
                if pronun in name_to_check:
                    prounouns = pronun
                    break
                    # print("pronouns")
                    # answer = True
                else:
                    prounouns = ""

        name_to_return = clean_name(name)
        name_to_return = remove_more_emoji(name_to_return)
        
        for character in to_replace_with_space:
            if character in name_to_return:
                name_to_return2 = name.replace(character,"  ").strip()
                if '  ' in name_to_return2:
                    pers_name = name_to_return2.split("    ")
                    person_name_to_return = pers_name [0]
                else:
                    person_name_to_return = name_to_return
                    
                        
            else:
                person_name_to_return = name_to_return
        
    for string in strings_to_remove:
        if string in person_name_to_return:
            person_name_to_return = person_name_to_return.replace(string, "")
    try:
        header = driver.find_element_by_xpath("//h2[@class='mt1 t-18 t-black t-normal break-words']").text

    except :
        try:
            header = driver.find_element_by_xpath("//div[@class='text-body-medium break-words']").text

        except :
            header = ""
            print("no header")
    

    try:
        location = driver.find_element_by_xpath("//li[@class='t-16 t-black t-normal inline-block']").text

    except :
        try:
            location = driver.find_element_by_xpath("//span[@class='text-body-small inline t-black--light break-words']").text


        except :
            location = ""

    try:


        #presence-entity__image  pv-top-card__photo  lazy-image ember-view
        profile_pic_link = driver.find_element_by_xpath("//img[contains(@class,'profile-picture')]").get_attribute("src")
        #print("### profile_pic_link:", profile_pic_link)
    except NoSuchElementException:
        print("### profile_pic_link exception!!")
        profile_pic_link = ""


    # list_items = driver.find_element_by_xpath("").text
    
   

    try:
        number_of_connections = driver.find_element_by_xpath("//span[@class='t-black--light']").text
        
        if 'connection' in number_of_connections or 'connections' in number_of_connections:
            number_of_connections = number_of_connections.split("connection")[0]
            # number_of_connections = int(number_of_connections)
            
        if '+' in number_of_connections:
            number_of_connections = number_of_connections.replace('+','')
            # number_of_connections = int(number_of_connections)
        
        elif ',' in number_of_connections:
            number_of_connections = number_of_connections.replace(',','')
            # number_of_connections = int(number_of_connections)
        else:
           
           number_of_connections = int(number_of_connections)
            
        if type(number_of_connections) == str:
            number_of_connections = int(number_of_connections)
                
    except :
        try:
            number_of_connections = driver.find_element_by_xpath("//li[@class='text-body-small']").text
            if 'connection' in number_of_connections or 'connections' in number_of_connections:
                number_of_connections = number_of_connections.split("connection")[0]
                # number_of_connections = int(number_of_connections)
                
            if '+' in number_of_connections:
                number_of_connections = number_of_connections.replace('+','')
                # number_of_connections = int(number_of_connections)
            
            elif ',' in number_of_connections:
                number_of_connections = number_of_connections.replace(',','')
                # number_of_connections = int(number_of_connections)
            else:
               
               number_of_connections = int(number_of_connections)
                
            if type(number_of_connections) == str:
                number_of_connections = int(number_of_connections)
        except:
            number_of_connections = 0
        
    general = {"general":''}
    general['general'] = {"linkedin_url":current_link, "name": person_name_to_return, "header":header,"location":location, "profile_pic_link":profile_pic_link, "prounouns": prounouns,"numberOfConnections": number_of_connections}




    
    if moveToElement(driver,"//a[@class='ember-view link-without-visited-state cursor-pointer text-heading-small inline-block break-words']")==True:
        driver.find_element_by_xpath("//a[@class='ember-view link-without-visited-state cursor-pointer text-heading-small inline-block break-words']").click()
    #TESTING
    time.sleep(2 + randint(1, 3))
    websites = []
    twitter_accounts = []
    emails = []
    try:
        email_path = driver.find_element_by_xpath("//section[contains(@class,'pv-contact-info__contact-type')]//h3[text()='Email']")
        email_ref = email_path.find_element(By.XPATH, "./ancestor::section//a[contains(@href,'mailto:')]")
        email = email_ref.text
        
       # email_path = "//section[contains(@class,'pv-contact-info__contact-type')]//h3[text()='Email']"
        # target = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, emai)))
        # #ActionChains(driver).move_to_element(target).perform()
        
        # email = driver.find_element_by_xpath(target_xpath).text
      
            
    except:
        email = ""

    try:
        website = driver.find_elements_by_xpath("//section[contains(@class,'pv-contact-info__contact-type')]//h3[text()='Website']")
        if len(website)==0:
            website = driver.find_elements_by_xpath("//section[contains(@class,'pv-contact-info__contact-type')]//h3[text()='Websites']")
        for dt in website :
            
            element = driver.find_elements_by_xpath("//a[@class='pv-contact-info__contact-link link-without-visited-state']")
            
            #TESTING
            #time.sleep(0.5)
            for value in element:
#                            print(value.text)
                websites.append(value.text)
    except:
        websites = []

    try:
        twitter = driver.find_elements_by_xpath("//section[contains(@class,'pv-contact-info__contact-type')]//h3[text()='Twitter']")
        for twts in twitter:
            tweets = driver.find_elements_by_xpath("//li[@class='pv-contact-info__ci-container t-14']/a")
            for values in tweets:
                twitter_accounts.append((values.text))
                twitter_accounts = list(set(twitter_accounts))
    except:
        twitter = ""

    try:
        phone_path =  driver.find_element_by_xpath("//section[contains(@class,'pv-contact-info__contact-type')]//h3[text()='Phone']")
        phonr_ref = phone_path.find_element(By.XPATH, "./ancestor::section//ul[@class='list-style-none']/li/span[contains(@class, 't-14')]")
        phone = phonr_ref.text
        # phone = phone.split("Phone\n")[1]
    except:
        phone = ""

    try:
        bday_path =  driver.find_element_by_xpath("//section[contains(@class,'pv-contact-info__contact-type')]//h3[text()='Birthday']")
        bday_ref = bday_path.find_element(By.XPATH, "./following-sibling::div/span[contains(@class, 't-14')]")
        birthday = bday_ref.text
        
    except:
        birthday = ""

    contact_info = {"contact_info":''}
    contact_info['contact_info'] = {"email":email, "websites": websites, "twitter":twitter_accounts,"phone":phone,"birthday":birthday,"error":None}

    if moveToElement(driver,"//button[@aria-label='Dismiss']")==True:
        #TESTING
        #time.sleep(1)
        driver.find_element_by_xpath("//button[@aria-label='Dismiss']").click()



    experience_result = getExperience(driver, current_link)
    print("experience_result:")
    print(experience_result)
    
    time.sleep(1)
    
    education_result = getEducation(driver, current_link)
    print("education_result:")
    print(education_result)    
    

    informationDict = {**general, **contact_info, **experience_result, **education_result}
    return informationDict



def createDoc(job_type, doc_id):
    """
    Creates an doc in db with all fields empty
    """
    default = {'contact_info':{"email":"", "websites": "", "twitter":"","phone":"","birthday":""}, "general": {"linkedin_url":"", "name": "", "header":"","location":"", "profile_pic_link":"",'prounouns':'','numberOfConnections':0}, "experience":[], "education":[]}
    db.collection(job_type).document(doc_id).set(default)
    
def extract_entity_linkedin_id (link):
    if "linkedin.com/" not in link:
        return "" #wrong link

    output = link.split("linkedin.com/")[1].split("/")[1]
    #test if there is "?"
    if "?" in output:
        output = output.split("?")[0]
    output = output.split("/")[0]
    return output



def getppl(driver, li_link):
    #print("## in getppl, with li_link=",li_link)
    try:
        driver.get(li_link)
        time.sleep(random.uniform(5, 7))  
    except:
        print("didnt open link, probably timout, let's try again")
        try:
            driver.get(li_link)
            time.sleep(random.uniform(1, 5))  
        except:
            print("it's failing.")
            pass
    #time.sleep(1 + randint(1, 2))

    try:
        target_xpath = "//section[@class='artdeco-toasts']"
        target = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))

    except TimeoutException:
        print("### li_link URL clicked but  page didnt load ")
        updated_Link = driver.current_url
        #print("updated_Link:",updated_Link)
        if updated_Link == "https://www.linkedin.com/404/":
            return "page_doesnt_exist"
             #store empty doc with error
    
    
        if (
            "/checkpoint/challenges" in updated_Link
            or "login?session_redirect" in updated_Link
            or "authwall?trk" in updated_Link
            or updated_Link == "https://www.linkedin.com/"
        ):
            return "security_check"
        if 'view?id' in updated_Link:
        
            return "page_doesnt_exist"
        try:
            smtg_wrong = driver.find_element_by_xpath("//h2[@class='artdeco-empty-state__headline artdeco-empty-state__headline--mercado-error-server-small artdeco-empty-state__headline--mercado-spots-small']")
            smtg_wrong = smtg_wrong.text
            if 'Something went wrong' in smtg_wrong:
                return "page_doesnt_exist"
        except NoSuchElementException:
            pass
        try:
            page_loaded_xpath = "//div[@class='authentication-outlet']"
            trgt_page = WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.XPATH, page_loaded_xpath)))
        except TimeoutException:
            print("page didnt load aka doesnt exist but no error on screen")
            return "page_doesnt_exist"
        
                   



    updated_Link = driver.current_url
    #print("updated_Link:",updated_Link)
    if updated_Link == "https://www.linkedin.com/404/":
        return "page_doesnt_exist"
         #store empty doc with error


    if (
        "/checkpoint/challenge" in updated_Link
        or "login?session_redirect" in updated_Link
        or "authwall?trk" in updated_Link
        or updated_Link == "https://www.linkedin.com/"
    ):
        return "security_check"

    
    if 'view?id' in updated_Link or 'https://www.linkedin.com/404/' in updated_Link:
        print("hooon")
        return "page_doesnt_exist"
     
    
    
    else:
        prof_info=getProfileInfo(driver, li_link)

    return prof_info




# import pandas as pd

# # def default_converter(obj):
# #     if isinstance(obj, datetime):
# #         return obj.strftime('%Y-%m-%d %H:%M:%S')
# #     raise TypeError(f'Object of type {type(obj)} is not JSON serializable')

# # # Function to save data to JSON file
# # def save_to_json(data, filename):
# #     with open(filename, 'w') as f:
# #         json.dump(data, f, default=default_converter, indent=4)

# # # <<<<<<< HEAD
# driver = login("rroobbiinngghhaazzaall99@gmail.com","roby1234")
# # # # =======
# # # # #driver = login("igorpushkin.1@yahoo.com","Rayi897@")
# # # # >>>>>>> 9b6c382d069436464661d5dd71e01e0dbcd20c1e
               
# # df = pd.read_csv("/home/joy/Documents/JULIEN/urgent-ppl/urg0-0.csv")
# # df = df.replace(np.nan, '', regex=True)
# # link  = "https://www.linkedin.com/company/dealroom-co/people/"

# # df['updated_link'] = [np.nan for i in range(len(df))]
# # for ind,link in enumerate(df.Linkedin):
# #     print(link)
# #     print(ind)
# #     # break
# #     # id_person = link.split("/in/")[1]
# #     id_person = link
    
#     li_link = "https://www.linkedin.com/in/"+"nafisjamal"
#     result = getppl(driver, li_link)
#     li_id = "nafisjamal"
#     # if processed_dict == "page_doesnt_exist":
#     #     default = {}
#     #     default = {"contact_info":{"email":"", "websites": "", "twitter":"","phone":"","error":"page_doesnt_exist"}, "general": {"linkedin_url":li_link, "name": "", "header":"","location":"", "profile_pic_link":"",'pronouns':'','numberOfConnections':0}, "experience":[], "education":[], "ppl":{"date_collected":datetime.datetime.strftime(datetime.datetime.today(), "%d-%b-%y")}}
#     #     default["ppl"]["date_collected"] = datetime.datetime.strftime(datetime.datetime.today(), "%d-%b-%y")
#     #     default["id"]= id_person
#     #     default["founder_jobs"] = []
#     #     default["ppl"] = {"date_collected": datetime.datetime.strftime(datetime.datetime.today(), "%d-%b-%y")}
#     #     db.collection("ppl").document(id_person).set(default, merge=True)
        
# #     else:    
#         processed_dict = {
#             "general": result.get("general", {}),
#             "experience": result.get("experience", []),
#             "contact_info": result.get("contact_info", {}),
#             "education": result.get("education", []),
#             'last_updated':datetime.datetime.utcnow(),
#             'parallel_number':randint(1, 10)
#         }
        
# #         # If you want to include additional fields like "ppl" and "founder_jobs":
#         processed_dict["founder_jobs"] = []
#         processed_dict["ppl"] = {"date_collected": datetime.datetime.strftime(datetime.datetime.today(), "%d-%b-%y")}
        
# #         # Populate founder_jobs
#         if "experience" in processed_dict:
#             for exp in processed_dict["experience"]:
#                 company_linkedin_url = exp.get('company_linkedin_url', '')
#                 if exp.get('title') and "founder" in exp['title'].lower():
#                     founder_dict = {
#                         'title': exp['title'],
#                         'started_date': exp.get('period_start', ''),
#                         'linkedin_url': company_linkedin_url
                        
#                     }
#                     processed_dict["founder_jobs"].append(founder_dict)
                    
#         db.collection("ppl").document("nafisjamal").set(processed_dict, merge=True)
        

#      update_person(li_id, processed_dict)



# df_left=df.iloc[ind:]
# df_left.to_csv("/home/joy/Documents/JULIEN/urgent-ppl/urg0-0.csv",index=False)
# # #     filename = f'/home/joy/Desktop/Linkedin/ribal-employees/{id_person}.json'
# # # #     save_to_json(result, filename)

# # <<<<<<< HEAD
# li_link = "https://www.linkedin.com/in/alex-hawat-5b00902/"
# # # # # # # # # # # # # # # # # # # # # # # # li_link = "https://www.linkedin.com/in/preetichaudhary/"
# processed_dict = getppl(driver,li_link)
# # =======
# # #li_link = "https://www.linkedin.com/in/eduardosalazarrealestate/"
# # # # # # # # # # # # # # # # # # # # # # # # li_link = "https://www.linkedin.com/in/preetichaudhary/"
# # #processed_dict = getppl(driver,li_link)
# # >>>>>>> 9b6c382d069436464661d5dd71e01e0dbcd20c1e

# # # # dictso = processed_dict['experience']
# # # # # # # # # processed_dict = result3
    
# # workpm = dictso[1]
# # if workpm['title'] == workpm['company_name'] 
