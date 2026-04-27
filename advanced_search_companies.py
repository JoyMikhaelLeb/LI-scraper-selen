#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 12:33:55 2023

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

# import numpy as np


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


def moveToElement(driver, target_xpath):
    
    try:
        target = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
        ActionChains(driver).move_to_element(target).perform()
        return True
    except:
        return False



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
    
    
def advanced_search_people_company(driver,sale_company_ID):
    driver.get(sale_company_ID)
    time.sleep(random.uniform(5, 25))
    
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
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//section[@id='account-page-container']")))
        
    except:
        try:
           while moveToElement(driver, "//*[contains(text(), 'something has gone')]")==True:
               print("looping here")
               driver.refresh()
               time.sleep(random.uniform(5,10))
               try:
                   WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//section[@id='profile-card-section']")))
               except:
                   print("didnt catch the page. something wrong")
        except:    
            print("profile not available")
            final_resultUP =  [[],""]
            
            return final_resultUP
        
    name = driver.find_element_by_xpath("//div[@data-anonymize='company-name']").text
        
    try:
            company_website =driver.find_element_by_xpath("//a[@data-control-name='visit_company_website']").get_attribute("href")
            if 'linkedin.com/sales/company/' in company_website:
                company_website = company_website.split("/company/")[1]
    except:
        try:
            time.sleep(3)
            company_website =driver.find_element_by_xpath("//a[@data-control-name='visit_company_website']").get_attribute("href")
            if 'linkedin.com/sales/company/' in company_website:
                company_website = company_website.split("/company/")[1] 
        except:
            company_website=""
            
            
    try:
        company_location = driver.find_element_by_xpath("//div[@data-anonymize='location']").text
    except:
        company_location = ""
            
    company_headquarter = ""
    company_speciality = ""
    company_founded = ""
    company_type = ""
    
    try:
        driver.find_element_by_xpath("//button[@data-control-name='read_more_description']").click()
        time.sleep(random.uniform(1,3))
    
        company_about = driver.find_element_by_xpath('//p[@data-anonymize="company-blurb"]').text
        if '        ' in company_about:
            company_about = company_about.replace("        ","")
        if '\n      ' in company_about:
            company_about = company_about.replace("\n      ","")
        
        if company_website == "":
            try:
                company_website = driver.find_element_by_xpath("//dd[@class='company-details-panel__content']").text
            except:
                company_website = ""
        
        
        try:
            company_headquarter = driver.find_element_by_xpath("//dd[@class='company-details-panel__content company-details-panel-headquarters t-black--light']").text
        except:
            company_headquarter = ""
            
        try:
            company_type = driver.find_element_by_xpath("//dd[@class='company-details-panel__content company-details-panel-type t-black--light']").text
        except:
            company_type = ""
    except:
        try:
            company_about = driver.find_element_by_xpath('//div[@data-anonymize="company-blurb"]').text
        except:
            company_about = ""
       
        

    
    try:
        company_speciality = driver.find_element_by_xpath("//dd[@class='company-details-panel__content company-details-panel-specialties t-black--light']").text
        
    except:
        company_speciality = ""
        
        
    try:
        company_founded = driver.find_element_by_xpath("//dd[@class='company-details-panel__content company-details-panel-founded t-black--light']").text
    except:
        company_founded = ""
        
        
    company_linkedin_link_numerical = sale_company_ID.replace("sales/","")
    try:
        # company_linkedin_link_numerical = company_linkedin_link_numerical.replace("/sales","")
        driver.get(company_linkedin_link_numerical)
        time.sleep(random.uniform(1,5))
        company_linkedin_url = driver.current_url
        if '/about/' in company_linkedin_url:
            company_linkedin_url.split("about")[0]
        
        
    except:
        company_linkedin_url= ""
            
          
    # industry = driver.find_element_by_xpath("//span[@data-anonymize='industry']").text
    # company_size_onLI = industry = driver.find_element_by_xpath("//span[@data-anonymize='company-size']").text.split(" ")[0]
        
    
    
    final_resultUP = [name, company_website,company_about,company_headquarter,company_type,company_location,company_speciality,company_founded,company_linkedin_url]

    # result_to_return = final_resultUP
    return final_resultUP




def get_advanced_search_company_profile(driver,sale_company_ID):
    
    try:
        
        get_advan = advanced_search_people_company(driver, sale_company_ID)
        if get_advan == []:
            result_set = []
            # print("**********")
            print("enpty result")     
            count=0
            get_adv_return = result_set,"check_profile",count
            return get_adv_return

            
        error=""
        adv_data = {"adv":[]}
        count=1
        adv_data['adv'].append({"name":get_advan[0],
                                    'website':get_advan[1],
                                    'overview':get_advan[2],
                                    'headquarters':get_advan[3],
                                    'type':get_advan[4],
                                    'location':get_advan[5],
                                    "speciality":get_advan[6],
                                    "founded":get_advan[7],
                                    "company_linkedin_url":get_advan[8],
                                    'company_sales_url':sale_company_ID})
    

        test_list = adv_data['adv']
        done = set()
        result_set = []
        for d in test_list:
            done.add(d['company_sales_url']) 
            result_set.append(d)
            
        get_adv_return = result_set,error,count
        
        
        
    except Exception as e:
            result_set = []
            # print("**********")
            print(e)     
            count=0
            get_adv_return = result_set,"check_profile",count
            
    return get_adv_return
    

def detailed_data_false(driver,max_tab):
    total_opened_profiles = []
    selector = Selector(text=driver.page_source)
    
    list_of_ppl = selector.xpath("//ol[@class='artdeco-list background-color-white _border-search-results_1igybl']")
  
    pers_square = list_of_ppl.xpath("//li[@class='artdeco-list__item pl3 pv3 ']")
    if len(pers_square)!=0 and len(pers_square)<=25 and (max_tab == 1 or (max_tab!=1 and check_navigator(driver)==False) ) :
            count_false = 1
            gp_ppl = []
            for i in pers_square.extract():
                soup = bs(i, features="lxml")
                
                try:
                    comID = soup.find("a",{"data-control-name":"view_company_via_result_name"})['href']
                    comID = comID.split('?')[0]
                    comID = 'https://www.linkedin.com'+comID
                    if comID not in total_opened_profiles:
                        total_opened_profiles.append(comID)
        
                except:
                    comID = ""
            
                try:
                    name = soup.find("a",{"data-anonymize":"company-name"})
                    if name is not None:
                        name=name.text
                        if "\n" in name:
                            name=name.replace("\n            ","").replace("\n          ","")
                        try:
                            name = name.split("\n ")[0]
                        except:
                            pass
                        name_to_return = clean_name(name)
                    else:
                        name_to_return = ""
                        
                except:
                    raise
                    
                try:
                    industry = soup.find("span",{"data-anonymize":"industry"})
                    if industry is not None:
                        industry = industry.text
                    if '\n' in industry:
                        industry = industry.replace("\n        ","").replace("\n          ","")
                        try:
                            industry = industry.split("\n ")[0]
                        except:
                            pass
                except:
                    industry = ""
                    
                    
                try:
                    compsize = soup.find("a",{"data-anonymize":"company-size"})
                    if compsize is not None:
                        
                        compsize = compsize.text.split(" ")[0]
                        if 'K' in compsize:
                            company_size = compsize.split("K")[0]
                         
                            company_size = int(float(company_size)*1000)
                        elif 'M' in compsize:
                            company_size = compsize.split("K")[0]
                            company_size = int(int(company_size)*1000000)
                        else:
                            company_size = compsize
                            
                    
                except:
                    company_size = ""
                    
                try:
                    revenues = soup.find("span",{"data-anonymize":"revenue"})
                    if revenues is not None:
                        revenues = revenues.text
                               
                except:
                    revenues = ""
                    
                try:
                    company_logo_link = soup.find("img",{"class":"lazy-image ember-view"})
                    if company_logo_link is not None:
                        company_logo_link = company_logo_link['src']
                        
                except:
                    company_logo_link = ""
                    
                    
                gp_ppl.append([name_to_return,comID,industry,company_size,revenues,company_logo_link])
            
    elif len(pers_square)!=0 and len(pers_square)<=25 and (max_tab !=1 and check_navigator(driver)==True) :
        
            gp_ppl = []
            
            for i in pers_square.extract():
                soup = bs(i, features="lxml")
                try:
                    comID = soup.find("a",{"data-control-name":"view_company_via_result_name"})['href']
                    comID = comID.split('?')[0]
                    comID = 'https://www.linkedin.com'+comID
                    if comID not in total_opened_profiles:
                        total_opened_profiles.append(comID)
        
                except:
                    comID = ""
            
                try:
                    name = soup.find("a",{"data-anonymize":"company-name"})
                    if name is not None:
                        name=name.text
                        if "\n" in name:
                            name=name.replace("\n            ","").replace("\n          ","")
                        try:
                            name = name.split("\n ")[0]
                        except:
                            pass
                        name_to_return = clean_name(name)
                    else:
                        name_to_return = ""
                        
                except:
                    raise
            
                try:
                    industry = soup.find("span",{"data-anonymize":"industry"})
                    if industry is not None:
                        industry = industry.text
                    if '\n' in industry:
                        industry = industry.replace("\n        ","").replace("\n          ","")
                        try:
                            industry = industry.split("\n ")[0]
                        except:
                            pass
                except:
                    industry = ""
                    
                    
                try:
                    compsize = soup.find("a",{"data-anonymize":"company-size"})
                    if compsize is not None:
                        
                        compsize = compsize.text.split(" ")[0]
                        if 'K' in compsize:
                            company_size = compsize.split("K")[0]
                         
                            company_size = int(float(company_size)*1000)
                        elif 'M' in compsize:
                            company_size = compsize.split("K")[0]
                            company_size = int(int(company_size)*1000000)
                        else:
                            company_size = compsize
                            
                    
                except:
                    company_size = ""
                    
                try:
                    revenues = soup.find("span",{"data-anonymize":"revenue"})
                    if revenues is not None:
                        revenues = revenues.text
                               
                except:
                    revenues = ""
                    
                try:
                    company_logo_link = soup.find("img",{"class":"lazy-image ember-view"})
                    if company_logo_link is not None:
                        company_logo_link = company_logo_link['src']
                        
                except:
                    company_logo_link = ""
                    
                    
                gp_ppl.append([name_to_return,comID,industry,company_size,revenues,company_logo_link])
            
            butn = "//button[contains(@class,'artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view')]"
            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            
            try:
                 element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, butn)))
                 # print(element.is_enabled())
            except:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                butn = "//button[contains(@class,'artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary artdeco-button--disabled ember-view')]"
                try:
                    element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, butn)))
                except:
                    button= "//button[@class='artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view']"
                    element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, butn)))
                # print("element in except",element.is_enabled())     
                
            count = 1
            while True and element.is_enabled()==True and max_tab>count:
                
                # count_false = count_false+1
                # time_ends = time.asctime()
                # print("time taken before clicking on next page is:  ",time_ends)
                driver.find_element_by_xpath(butn).click()
                time.sleep(random.uniform(2, 5))
                count+=1
                print(count)
                count_false = count
                
                    # gp_ppl.append([name_to_return,comID,industry,company_size,revenues,company_logo_link])
                    
                    # result_to_return = [gp_ppl,count_false]
                    # return result_to_return                 
                moveToElement(driver,"//ol[@class='artdeco-list background-color-white _border-search-results_1igybl']" )
                time.sleep(random.uniform(2, 5))
                try:
                    scrollDown1(driver,1)
                except:
                    try:
                        try:
                            scrollDown2(driver,1)
                        except:
                            scrollDown3(driver,1)
                    except:
                        print("unscrollable page")
                        if moveToElement(driver, "//h3[contains(text(), 'No accounts')]")==True:
                            # print("here")
                            result_to_return = [gp_ppl,(count_false-1)]
                            return result_to_return        
                    
                dialog = driver.find_element_by_xpath("//div[@id='search-results-container']")
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
                
                try:
                    # top = driver.find_elements_by_xpath("//li[@class='artdeco-list__item pl3 pv3 ']")[0]
                    all_see_more =  driver.find_elements_by_xpath("//button[@class='t-12 button--unstyled inline-block t-bold t-black--light']")
                    for smo in all_see_more:
                        smo.click()
                        
                    try:
                        scrollDown1(driver,1)
                    except:
                        try:
                            try:
                                scrollDown2(driver,1)
                            except:
                                scrollDown3(driver,1)
                        except:
                            print("unscrollable page")
                except:
                    pass
            
                
                try:
                    element = WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.XPATH, butn)))
                    # print(element.is_enabled())
                except:
                    butn = "//button[contains(@class,'artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary artdeco-button--disabled ember-view')]"
                    element = WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.XPATH, butn)))
                            
                moveToElement(driver,"//ol[@class='artdeco-list background-color-white _border-search-results_1igybl']" )
                time.sleep(random.uniform(2, 5))
                try:
                    scrollDown1(driver,1)
                except:
                    try:
                        try:
                            scrollDown2(driver,1)
                        except:
                            scrollDown3(driver,1)
                    except:
                        print("unscrollable page")
                
                dialog = driver.find_element_by_xpath("//div[@id='search-results-container']")
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
                # top = driver.find_elements_by_xpath("//li[@class='artdeco-list__item pl3 pv3 ']")[0]
                
                
            
                selector = Selector(text=driver.page_source)
                list_of_ppl = selector.xpath("//ol[@class='artdeco-list background-color-white _border-search-results_1igybl']")
  
                pers_square = list_of_ppl.xpath("//li[@class='artdeco-list__item pl3 pv3 ']")
                for i in pers_square.extract():
                    soup = bs(i, features="lxml")
                    try:
                        comID = soup.find("a",{"data-control-name":"view_company_via_result_name"})['href']
                        comID = comID.split('?')[0]
                        comID = 'https://www.linkedin.com'+comID
                        if comID not in total_opened_profiles:
                            total_opened_profiles.append(comID)
            
                    except:
                        comID = ""
                
                    try:
                        name = soup.find("a",{"data-anonymize":"company-name"})
                        if name is not None:
                            name=name.text
                            if "\n" in name:
                                name=name.replace("\n            ","").replace("\n          ","")
                            try:
                                name = name.split("\n ")[0]
                            except:
                                pass
                            name_to_return = clean_name(name)
                        else:
                            name_to_return = ""
                            
                    except:
                        raise
                
                    try:
                        industry = soup.find("span",{"data-anonymize":"industry"})
                        if industry is not None:
                            industry = industry.text
                        if '\n' in industry:
                            industry = industry.replace("\n        ","").replace("\n          ","")
                            try:
                                industry = industry.split("\n ")[0]
                            except:
                                pass
                    except:
                        industry = ""
                        
                        
                    try:
                        compsize = soup.find("a",{"data-anonymize":"company-size"})
                        if compsize is not None:
                            
                            compsize = compsize.text.split(" ")[0]
                            if 'K' in compsize:
                                company_size = compsize.split("K")[0]
                             
                                company_size = int(float(company_size)*1000)
                            elif 'M' in compsize:
                                company_size = compsize.split("K")[0]
                                company_size = int(int(company_size)*1000000)
                            else:
                                company_size = compsize
                            
                    
                    except:
                        company_size = ""
                        
                    try:
                        revenues = soup.find("span",{"data-anonymize":"revenue"})
                        if revenues is not None:
                            revenues = revenues.text
                                   
                    except:
                        revenues = ""
                        
                    try:
                        company_logo_link = soup.find("img",{"class":"lazy-image ember-view"})
                        if company_logo_link is not None:
                            company_logo_link = company_logo_link['src']
                            
                    except:
                        company_logo_link = ""
                        
                        
                    gp_ppl.append([name_to_return,comID,industry,company_size,revenues,company_logo_link])
                    
    result_to_return = [gp_ppl,count_false]
    return result_to_return                 
            


def sales_company_search(driver,search_link,detailed_data,max_tab,return_counts_only=False):
   
    driver.get(search_link)
    time.sleep(random.uniform(5, 25))
    try:
        WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.XPATH, "//ol[@class='artdeco-list background-color-white _border-search-results_1igybl']")))
    except:
        if moveToElement(driver,"//ol[@class='artdeco-list background-color-white _border-search-results_1igybl']" )==False:
            return_result = [],0,""
            
            return return_result
    updated_Link = driver.current_url
    if (
        "/checkpoint/challenges" in updated_Link
        or "login?session_redirect" in updated_Link
        or "authwall?trk" in updated_Link
        or updated_Link == "https://www.linkedin.com/"
    ):
        return "security_check"
    
    if return_counts_only==True:
        time.sleep(random.uniform(3, 8))
        try:
            sales_result_number = driver.find_element_by_xpath("//div[@class='t-14 flex align-items-center mlA pl3 ']/span").text.split(" result")[0]
            
            
        except:
            sales_result_number = "0"
        
        salesNumber = {"nbre":[]}
        salesNumber['nbre'].append({"search_total_results":sales_result_number})
        
        salesNumberToreturn = salesNumber['nbre'][0]
        return_result = salesNumberToreturn,1,""
        return return_result
    
    if return_counts_only==False:
        time.sleep(random.uniform(7, 9))
        if moveToElement(driver, "//h3[contains(text(), 'No leads')]")==True:
          return_result = [],0,""
          return return_result
      
        else:
            print("no exception, will start working on search")
            pass
        if moveToElement(driver,"//ol[@class='artdeco-list background-color-white _border-search-results_1igybl']" )==False:
            return_result = [],0,""
            
            return return_result
        
        
        # time.sleep(random.uniform(2, 5))
        try:
            coll_butn = driver.find_element_by_xpath("//button[@aria-label='Collapse filter panel']")
            coll_butn.click()
            moveToElement(driver,"//ol[@class='artdeco-list background-color-white _border-search-results_1igybl']" )
        except:
            pass
            print("menu opened already")
        
        
        
        try:
            scrollDown1(driver,1)
        except:
            try:
                try:
                    scrollDown2(driver,1)
                except:
                    scrollDown3(driver,1)
            except:
                print("unscrollable page")
        # scrollDown2(driver,1)
        try:
            dialog = driver.find_element_by_xpath("//div[@id='search-results-container']")
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
        except:
            print("no scroll")
            
        try:
            all_see_more =  driver.find_elements_by_xpath("//button[@class='t-12 button--unstyled inline-block t-bold t-black--light']")
            for smo in all_see_more:
                smo.click()
                
            try:
                scrollDown1(driver,1)
            except:
                try:
                    try:
                        scrollDown2(driver,1)
                    except:
                        scrollDown3(driver,1)
                except:
                    print("unscrollable page")
        except:
            pass
        # scrollDown2(driver,1)
        try:
            dialog = driver.find_element_by_xpath("//div[@id='search-results-container']")
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
        except:
            print("no scroll")
           
        
        if detailed_data == False:
            time.sleep(random.uniform(2, 3))
            salesInfo = {"sales":[]}
            
            sales_detailed_data = detailed_data_false(driver, max_tab)
            for biglist in sales_detailed_data[0]:
                # biglist
                try:
                    salesInfo['sales'].append({'name':biglist[0],
                                                      'company_sales_url':biglist[1],
                                                      'company_industry': biglist[2],
                                                      'number_of_employees':biglist[3],
                                                      'revenue':biglist[4],
                                                      'company_logo':biglist[5].split(" in")[0],
                                                      
                                                      }) 
                except:
                    salesInfo['sales'].append({'name':biglist[0],
                                                  'company_sales_url':biglist[1],
                                                  'company_industry': biglist[2],
                                                  'number_of_employees':biglist[3],
                                                  'revenue':biglist[4],
                                                  'company_logo':"",
                                                  
                                                  }) 
                salesInfo['number_of_tabs']=sales_detailed_data[1]
                            
                
        # if detailed_data == True:
        #     salesInfo = {"sales":[]}
        #     sales_detailed_data = detailed_data_true(driver, max_tab)
        #     for biglist in sales_detailed_data[0]:
                
        #         salesInfo['sales'].append({'name':biglist[0],
        #                                           'company_sales_url':biglist[1],
        #                                           'company_industry': biglist[2],
        #                                           'number_of_employees_on_LINKEDIN':biglist[3],
        #                                           'revenue':biglist[4],
        #                                           'company_logo':biglist[5].split(" in")[0],
                                                  
        #                                           }) 
                      
        #         salesInfo['number_of_profile_opened']=sales_detailed_data[1]
                
           
                
        test_list = salesInfo['sales']
        done = set()
        result_set = []
        for d in test_list:
            done.add(d['company_sales_url']) 
            result_set.append(d)
                
        if detailed_data == True:
            return_result = result_set,salesInfo['number_of_profile_opened'],""
        if detailed_data == False:
            return_result = result_set,salesInfo['number_of_tabs'],""
        print("adv sales result : ",return_result)
        return return_result
    
    
    

# if __name__ == '__main__':
    
# # # #         time_Start = time.asctime()
        
#         username="igorpushkin.1@yahoo.com"
#         password="Rayi897@"                       
#         driver=login(username, password) 
        
#         # detailed_data = False
#         # max_tab = 40
#         # return_counts_only = False
        
        
#         # search_link = "https://www.linkedin.com/sales/search/company?query=(filters%3AList((type%3ANUM_OF_FOLLOWERS%2Cvalues%3AList((id%3ANFR3%2Ctext%3A101-1000%2CselectionType%3AINCLUDED)%2C(id%3ANFR2%2Ctext%3A51-100%2CselectionType%3AINCLUDED)))%2C(type%3ACOMPANY_HEADCOUNT%2Cvalues%3AList((id%3AB%2Ctext%3A1-10%2CselectionType%3AINCLUDED)))%2C(type%3AINDUSTRY%2Cvalues%3AList((id%3A4%2Ctext%3ASoftware%2520Development%2CselectionType%3AINCLUDED)%2C(id%3A109%2Ctext%3AComputer%2520Games%2CselectionType%3AEXCLUDED)%2C(id%3A3131%2Ctext%3AMobile%2520Gaming%2520Apps%2CselectionType%3AEXCLUDED)))%2C(type%3ACOMPANY_HEADCOUNT_GROWTH%2CrangeValue%3A(min%3A25))%2C(type%3AANNUAL_REVENUE%2CrangeValue%3A(min%3A0%2Cmax%3A5)%2CselectedSubFilter%3AUSD)%2C(type%3AREGION%2Cvalues%3AList((id%3A102299470%2Ctext%3AEngland%252C%2520United%2520Kingdom%2CselectionType%3AINCLUDED)))))&sessionId=19mRdF%2BYQyKjnckIq87O1w%3D%3D&viewAllFilters=true"
#         # resul = sales_company_search(driver, search_link, detailed_data, max_tab,return_counts_only)

        
#         # sale_company_ID="https://www.linkedin.com/sales/company/610087"
# # #         # rst1 = get_advanced_search_company_profile(driver, sale_company_ID)
        
#         df = pd.read_csv("/home/joy/Desktop/comp-2003/link0.csv")

#         df = df.replace(np.nan, '', regex=True)
# #         # # link  = "https://www.linkedin.com/company/dealroom-co/people/"
#         df['name'] = [np.nan for i in range(len(df))]
#         df['website'] = [np.nan for i in range(len(df))]
#         df['overview'] = [np.nan for i in range(len(df))]
#         df['headquarters'] = [np.nan for i in range(len(df))]
#         df['type'] = [np.nan for i in range(len(df))]
#         df['location'] = [np.nan for i in range(len(df))]
#         df['speciality'] = [np.nan for i in range(len(df))]
#         df['founded'] = [np.nan for i in range(len(df))]
#         df['company_linkedin_url'] = [np.nan for i in range(len(df))]
#         # df['company_sales_url'] = [np.nan for i in range(len(df))]
        
#         # df['linkedin_profil_link'] = [np.nan for i in range(len(df))]
        
#         for ind,sale_company_ID in enumerate(df.company_sales_url):
#             print(sale_company_ID)
#             print(ind)
        
#             result= get_advanced_search_company_profile(driver, sale_company_ID)
#             data = result[0][0]
            
                
#             df.loc[ind, "name"] = data["name"]
#             df.loc[ind, "website"] = data["website"]
#             df.loc[ind, "overview"] = data["overview"]
#             df.loc[ind,"headquarters"] = data["headquarters"]
            
#             df.loc[ind,'type'] = data["type"]
#             df.loc[ind,'location'] = data['location']
#             df.loc[ind,'speciality'] = data['speciality']
            
#             df.loc[ind,'founded'] = data['founded']
#             df.loc[ind,'company_linkedin_url'] = data['company_linkedin_url']
#             df.loc[ind,'company_sales_url'] = data['company_sales_url']
            
            
#             # print("result:   ",result)
#             # df.loc[ind, "linkedin_profile_link"] = result
            
            
            
        
#         df_left=df.iloc[ind:]
#         df_left.to_csv("/home/joy/Desktop/comp-2003/link0-0.csv", index=False)
    
#         df.to_csv("/home/joy/Desktop/comp-2003/link0---0.csv", index=False)
        
# import csv
# data = resul[0]  # Assuming result is your data

# # # Extract keys from the first dictionary
# keys = set().union(*(d.keys() for d in data))

# # Write the data to the CSV file
# csv_file = "link2010.csv"

# with open(csv_file, 'w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=keys)
    
#     # Write header
#     writer.writeheader()
    
# #     # Write rows
#     for row in data:
#         writer.writerow(row)

# print('CSV file created successfully:', csv_file)
