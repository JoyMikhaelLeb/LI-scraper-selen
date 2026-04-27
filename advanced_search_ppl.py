#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 11:40:58 2023

@author: joy
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 22:20:10 2023

@author: joy
"""
import emoji
from supabase_founding_dates_interface import add_sales_id_people

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

import numpy as np


import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

if not firebase_admin._apps:
    cred = credentials.Certificate('key.json')
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
    
def advanced_search_people_profile(driver,saleID):
    # print("we are working in : ",saleID)
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
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//section[@id='profile-card-section']")))
        
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
    allroles = []
    # com_links = []
    finall = []
    final_result = []
    time.sleep(1)
    
    try:
        # name = driver.find_element_by_xpath("//div[@class='name-title-container']/h1").text
        name = driver.find_element_by_xpath("//div[contains(@class,'name-title-container')]/h1").text
    except Exception as e:
        try:
            name = driver.find_element_by_xpath("//div[@class='_name-title-container_sqh8tm']/h1").text
            
        except:
            try:
                name = driver.find_element_by_xpath("//h1[@data-anonymize='person-name']").text
            except:
                name = ""
        
    if name == "":
        driver.refresh()
        time.sleep(random.uniform(3,10))
        name = driver.find_element_by_xpath("//div[@class='_name-title-container_sqh8tm']/h1").text
    
    elif name == "LinkedIn Member" and moveToElement(driver, "//button[@class='ember-view _button_ps32ck _small_ps32ck _primary_ps32ck _left_ps32ck _container_iq15dg _cta_1xow7n _medium-cta_1xow7n']")==True:
        driver.find_element_by_xpath("//button[@class='ember-view _button_ps32ck _small_ps32ck _primary_ps32ck _left_ps32ck _container_iq15dg _cta_1xow7n _medium-cta_1xow7n']").click()
        name = driver.find_element_by_xpath("//h1[@data-anonymize='person-name']").text
    
    elif name == "LinkedIn Member" and moveToElement(driver, "//span[contains(text(), 'Unlock')]")==False:
        print("Linkedin Member")
        count=0
        final_resultUP =  [[],""]
        result_to_return = final_resultUP
        return result_to_return
    
    elif name == "LinkedIn Member" and moveToElement(driver, "//button[@class='ember-view _button_ps32ck _small_ps32ck _primary_ps32ck _left_ps32ck _container_iq15dg _cta_1xow7n _medium-cta_1xow7n']")==False:
        print("Linkedin Member")
        count=0
        final_resultUP =  [[],""]
        result_to_return = final_resultUP
        return result_to_return
    else:
        name=name
        
    
    
    
    
    try:
        location = driver.find_element_by_xpath("//div[@class='_lockup-caption_sqh8tm _bodyText_1e5nen _default_1i6ulk _sizeSmall_1e5nen _lowEmphasis_1i6ulk']").text
    except:
        try:
            location = driver.find_element_by_xpath("//div[contains(@class,'lockup-caption')]").text
        
        except:
            try:
                div_element = driver.find_element_by_xpath("//div[@class='_bodyText_1e5nen _default_1i6ulk']")
                following_sibling = div_element.find_element_by_xpath("following-sibling::div")
                location= following_sibling.text.split("\n")[0]
            except:
                location =""
    
    
    
   
        
    print("name is: ",name)
    # try:
    #     name = driver.find_element_by_xpath("//div[@class='_name-title-container_sqh8tm']/h1").text
    # except:
    #     name = ""
    
    try:
        header = driver.find_element_by_xpath("//span[@data-anonymize='headline']").text
    except:
        header = ""
    
    # if name=="":
    #     driver.refresh()
    #     time.sleep(random.uniform(3,10))
    #     try:
    #         location = driver.find_element_by_xpath("//div[@class='_lockup-caption_sqh8tm _bodyText_1e5nen _default_1i6ulk _sizeSmall_1e5nen _lowEmphasis_1i6ulk']").text
    #     except:
    #         location =""
        
    #     try:
    #         name = driver.find_element_by_xpath("//div[@class='_name-title-container_sqh8tm']/h1").text
    #     except Exception as t:
    #         print(t)
    #         final_resultUP =  [[],""]
            
    #         return final_resultUP
            
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
    
    if person_linkedin_id=="":
        try:
            driver.find_element_by_xpath("//button[@class='ember-view _button_ps32ck _small_ps32ck _primary_ps32ck _left_ps32ck _container_iq15dg _cta_1xow7n _medium-cta_1xow7n']").click()
            time.sleep(random.uniform(5, 7))
            try:
                profile_butn = driver.find_element_by_xpath("//button[@class='ember-view _button_ps32ck _small_ps32ck _tertiary_ps32ck _circle_ps32ck _container_iq15dg _overflow-menu--trigger_1xow7n']")
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
            
        
    print("pers_liid:  ",person_linkedin_id) 
    
    try:
        scroll_to_element(driver)
    except:
        pass
    try:    
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
        about_person = driver.find_element_by_xpath("//section[@id='about-section']//div[@data-anonymize='person-blurb']")
        if moveToElement(driver, "//section[@id='about-section']//button")==True:
            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
            button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Show more')]"))
)
            button.click()
            print("about clicked")
            # driver.find_element_by_xpath("//section[@class='_about-section_1dtbsb _card_yg4u9b _container_iq15dg _lined_1aegh9 _inset-compact_sfmhx2']").click()
            about_person  = driver.find_element_by_xpath("//p[@data-anonymize='person-blurb']")
            about_person = about_person.text 
            if 'Show less' in about_person:
                about_person = about_person.replace("Show less","")
   
            # return about_person
        else:
   
            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
            try:
                about_person = driver.find_element_by_xpath("//section[@id='about-section']//p").text
            except:
                try:
                    about_person = driver.find_element_by_xpath("//p[@data-anonymize='person-blurb']").text
                except:
                    try:
                        about_person = driver.find_element_by_xpath("//section[@id='about-section']//div[@data-anonymize='person-blurb']").text
          
                    except:
                        about_person=""
    except:
        print("about something is wrong")
        about_person = ""
    
    # driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    selector = Selector(text=driver.page_source)
    list_of_rols = selector.xpath("//div[@data-sn-view-name='lead-current-role']")
    if len(list_of_rols)!=0:
        one_role = list_of_rols.xpath("//li[@class='_position-item_q5pnp1']")
        if len(one_role)==0:
            one_role = list_of_rols.xpath("//div[@data-sn-view-name='lead-current-role']/div")
        for i2 in one_role.extract():
            soup2 = bs(i2,features=("lxml"))
            
            
            company_sales_id = soup2.find('p', class_='_current-role-item_th0xau')
            
            if company_sales_id is not None:
                company_sales_id = company_sales_id.find_next("a")
                try:
                    company_id_numerical = company_sales_id['href']
                except:
                    # print("c_id?")
                    company_id_numerical = ""
                if company_id_numerical!="":
                     company_id_numerical = "https://www.linkedin.com"+company_sales_id['href']
                
                
            else:
                company_id_numerical = ""
            # print("company_sales_id: ",company_sales_id)
            print("company_numerical_id: ",company_id_numerical)
            person_role = soup2.find("span",{"data-anonymize":"job-title"})
            if person_role is not None:
                person_role = person_role.text
            else:
                person_role = ""
                
            company_name = soup2.find("a",{"data-anonymize":"company-name"})
            if company_name is not None:
                company_name = company_name.text
            else:
                company_name = soup2.find("span",{"data-anonymize":"company-name"})
                if company_name is not None:
                    company_name = company_name.text
                else:
                    company_name = ""
            # print(company_name)
            
            
            
            
            role_duration = soup2.find("p",{"class":"_bodyText_1e5nen"})
            
            if role_duration:
                full_duration = role_duration.text.split("\n\n      ")[1].split("\n")[0]
                job_date_start, job_date_end = full_duration.split("–")
            else:
                job_date_start, job_date_end = "", ""
            # if role_duration is None:
            #     role_duration  = soup2.find("span",{"class":"pJMvsmNXnaEDwvXwTdxLuQrMLQdhGnKs"})
            #     job_date_start = ""
            #     job_date_end = ""
            
            # else:
            #     role_duration = role_duration.text
            #     if role_duration == '\n\n\n':
            #         job_date_start = ""
            #         job_date_end = ""
            #     else:
            #         parts = role_duration.strip().split()
    
            #         # Join the parts to form the desired output
            #         full_role_duration = ' '.join(parts[0:2])
    
                    
                    
            #         if full_role_duration =="\n":
            #             job_date_start = ""
            #             job_date_end = ""
            #         if '-' in full_role_duration:
            #             job_date_start = full_role_duration.split("–")[0].strip()
            #             job_date_end = full_role_duration.split("–")[1].strip()
            #         if '–' in full_role_duration:
            #             job_date_start = full_role_duration.split("–")[0].strip()
            #             job_date_end = full_role_duration.split("–")[1].strip()
                        
            #         if '\n' in full_role_duration:
            #             job_date_start = full_role_duration.split("–")[0].strip()
            #             job_date_end = full_role_duration.split("–")[1].strip()
               
                
               
            
            
            
            one_simple_role=[header,company_id_numerical,job_date_start,job_date_end,person_linkedin_id,person_role,company_name,about_person,location,name]
            allroles.append(one_simple_role)
            # print("line493~")
            
    if len(list_of_rols)==0:
        
        list_of_rols = selector.xpath("//div[contains(@class,'current-role-container')]")
        one_role = list_of_rols.xpath("//div[@class='company-lockup-container']")
        for i2 in one_role.extract():
            soup2 = bs(i2,features=("lxml"))
            
            
            company_sales_id = soup2.find('p', class_='_current-role-item_th0xau')
            
            if company_sales_id is not None:
                company_sales_id = company_sales_id.find_next("a")
                try:
                    company_id_numerical = company_sales_id['href']
                except:
                    # print("c_id?")
                    company_id_numerical = ""
                if company_id_numerical!="":
                     company_id_numerical = "https://www.linkedin.com"+company_sales_id['href']
                
                
            else:
                company_id_numerical = ""
            # print("company_sales_id: ",company_sales_id)
            print("company_numerical_id: ",company_id_numerical)
            person_role = soup2.find("span",{"data-anonymize":"job-title"})
            if person_role is not None:
                person_role = person_role.text
            else:
                person_role = ""
                
            company_name = soup2.find("a",{"data-anonymize":"company-name"})
            if company_name is not None:
                company_name = company_name.text
            else:
                company_name = soup2.find("span",{"data-anonymize":"company-name"})
                if company_name is not None:
                    company_name = company_name.text
                else:
                    company_name = ""
            # print(company_name)
            
            
            
            
            role_duration = soup2.find("p",{"class":"_bodyText_1e5nen _default_1i6ulk _sizeSmall_1e5nen"})
            
            
            if role_duration is None:
                role_duration  = soup2.find("span",{"class":"pJMvsmNXnaEDwvXwTdxLuQrMLQdhGnKs"})
                job_date_start = ""
                job_date_end = ""
            
            else:
                role_duration = role_duration.text
                
                parts = role_duration.strip().split()

                # Join the parts to form the desired output
                full_role_duration = ' '.join(parts[0:2])

                
                
                if full_role_duration =="\n":
                    job_date_start = ""
                    job_date_end = ""
                if '-' in full_role_duration:
                    job_date_start = full_role_duration.split("–")[0].strip()
                    job_date_end = full_role_duration.split("–")[1].strip()
                if '–' in full_role_duration:
                    job_date_start = full_role_duration.split("–")[0].strip()
                    job_date_end = full_role_duration.split("–")[1].strip()
                    
                if '\n' in full_role_duration:
                    job_date_start = full_role_duration.split("–")[0].strip()
                    job_date_end = full_role_duration.split("–")[1].strip()
           
                
               
            
            
            
            one_simple_role=[header,company_id_numerical,job_date_start,job_date_end,person_linkedin_id,person_role,company_name,about_person,location,name]
            allroles.append(one_simple_role)
            # print("line 551~")
    
        
    for testrole11 in allroles:
            # print(testrole11)
            if testrole11[1]!="":
                driver.get(testrole11[1])
                time.sleep(random.uniform(5, 60))
                # print("line 564")
                WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.XPATH, "//nav[contains(@class,'sidebar')]")))                
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
                
                driver.get(testrole11[1].replace("/sales",""))
                time.sleep(random.uniform(5,60))
                company_linked_id = driver.current_url
                print("company_linkedin_current_url ")                
                finall = [testrole11[0],testrole11[1],testrole11[2],testrole11[3],testrole11[4],testrole11[5],testrole11[6],testrole11[7],testrole11[8],testrole11[9],company_linked_id,company_website]
                 # finall.append()    
                 
            else:
                company_website = ""
                company_linked_id = ""
                finall = [testrole11[0],testrole11[1],testrole11[2],testrole11[3],testrole11[4],testrole11[5],testrole11[6],testrole11[7],testrole11[8],testrole11[9],company_linked_id,company_website]

                 
            final_result.append(finall)
            final_resultUP = [x for i,x in enumerate(final_result) if x not in final_result[i+1:]]
            
        
                    
            
    result_to_return = final_resultUP
    return result_to_return
        # 
        
    
def get_advanced_search_people_profile(driver,saleID):
    
    try:
        
        get_advan = advanced_search_people_profile(driver, saleID)
        if get_advan == []:
            result_set = []
            # print("**********")
            print("enpty result")     
            count=0
            get_adv_return = result_set,"check_profile",count
            return get_adv_return
        if get_advan == [[], '']:
            result_set = []
            count=0
            get_adv_return = result_set,"check_profile",count
            return get_adv_return
       
        else:
            error=""
            adv_data = {"adv":[]}
            count=1
            for resa in get_advan:
                # print(resa)
                adv_data['adv'].append({"header":resa[0],
                                        'company_sales_link':resa[1],
                                        'experience_start_year':resa[2],
                                        'experience_end_year':resa[3],
                                        'person_linkedin_url':resa[4],
                                        'experience_position':resa[5],
                                        'experience_company_name':resa[6],
                                        'about_person':resa[7],
                                        'location':resa[8],
                                        'name':resa[9],
                                        'experience_linkedin_url':resa[10],
                                        'experience_website':resa[11],
                                        'person_sales_url':saleID})
            
                # if adv_data['adv'][0]['name'] == 'LinkedIn Member':
                #     test_list = adv_data['adv']
                #     done = set()
                #     result_set = []
                #     for d in test_list:
                #         done.add(d['person_sales_url']) 
                #         result_set.append(d)
                        
                #         get_adv_return = result_set,"check_profile",count
                    
                    
            #         return get_adv_return
            test_list = adv_data['adv']
            done = set()
            result_set = []
            for d in test_list:
                done.add(d['person_sales_url']) 
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
                    persID = soup.find("a",{"data-control-name":"view_lead_panel_via_search_lead_name"})['href']
                    persID = persID.split('?')[0]
                    persID = 'https://www.linkedin.com'+persID
                    if persID not in total_opened_profiles:
                        total_opened_profiles.append(persID)
        
                except:
                    persID = ""
                # print(persID)
                try:
                    name = soup.find("span",{"data-anonymize":"person-name"})
                    if name is not None:
                        name=name.text
                        if "\n" in name:
                            name=name.replace("\n            ","").replace("\n          ","")
                        name_to_return = clean_name(name)
                    else:
                        name_to_return = ""
                        
                except:
                    raise
        
                try:
                    location = soup.find("span",{"class":"t-12"})
                    if location is not None:
                        location = location.text
                    else:
                        location = ""
                except:
                    location = ""
                
                    
                
                try:
                    position_title = soup.find("span",{"data-anonymize":"title"})
                    if position_title is not None:
                        position_title = position_title.text
                        if '\n' in position_title:
                            position_title = position_title.replace("\n","")
                        if '            ' in position_title:
                            position_title = position_title.replace("            "," - ")
                        if '          ' in position_title:
                            position_title = position_title.replace("          ","")
                    else:
                        position_title = ""
                except:
                    position_title = ""
                
                try:
                    position_company = soup.find("a",{"data-anonymize":"company-name"})
                    if position_company is not None:
                        position_company = position_company.text
                        if '\n' in position_company:
                            position_company = position_company.replace("\n","")
                        if '            ' in position_company:
                            position_company = position_company.replace("            "," - ")
                        if '          ' in position_company:
                            position_company = position_company.replace("          ","")
                        
                        if ' - ' in position_company:
                            position_company = position_company.replace(" - ","")
                        
                    else:
                        position_company = ""
                except:
                    position_company = "" 
                        
                    
                
                try:
                    duration = soup.find("div",{"class":"artdeco-entity-lockup__metadata ember-view"})
                    if duration is not None:
                        duration = duration.text
                        if '\n' in duration:
                            duration = duration.replace("\n","")
                        if '          ' in duration:
                            duration = duration.replace("          ","-")
                        if '      ' in duration:
                            duration = duration.replace("      ","")
                        if '--' in duration:
                            duration = duration.replace("--"," | ").replace("-","")
                        if '|' in duration:
                            duration_full = duration.split("|")
                            dur_in_role = duration_full[0].strip()
                            dur_in_company = duration_full[1].strip()
                        else:
                            dur_in_role = ""
                            dur_in_company = ""
                except:
                    duration = ""
                
                
                try:
                    about_pers = soup.find("dd",{"class":"t-12 t-black--light mb3"})
                    if about_pers is not None:
                        about_pers = about_pers.text.replace("\n","")
                    if 'see less' in about_pers:
                        about_pers = about_pers.replace("see less","...")
                    else:
                        about_pers=""
                except:
                    about_pers = ""
                    
                try:
                    company_SID = soup.find("a",{"class":"ember-view t-black--light t-bold inline-block"})
                    if company_SID is not None:
                        company_SID = company_SID['href']
                        company_SID = "https://www.linkedin.com"+company_SID.split("?")[0]
                    else:
                        company_SID = ""
                except:
                    company_SID=""
                                   
                gp_ppl.append([name_to_return,persID,location,position_title,position_company,dur_in_role,dur_in_company,about_pers,company_SID])
                
                # print("onfirst page: ",len(gp_ppl))
                # PeopleInfo = {"info":[]}
                # PeopleDetails = pd.DataFrame(columns=['Name','NameID','Location','Position','Company Name','Duration in role','Duration in company'])
                # for ppl in gp_ppl:
                #     new_row = {'Name':ppl[0],'NameID':ppl[1], 'Location':ppl[2], 'Position':ppl[3],'Company Name':ppl[4],'Duration in role':ppl[5],'Duration in company':ppl[6]}    
                #     PeopleDetails = PeopleDetails.append(new_row, ignore_index=True)
    
    
    
    
    elif len(pers_square)!=0 and len(pers_square)<=25 and (max_tab !=1 and check_navigator(driver)==True) :
        
            gp_ppl = []
            
            for i in pers_square.extract():
                soup = bs(i, features="lxml")
                
                try:
                    persID = soup.find("a",{"data-control-name":"view_lead_panel_via_search_lead_name"})['href']
                    persID = persID.split('?')[0]
                    persID = 'https://www.linkedin.com'+persID
                    if persID not in total_opened_profiles:
                        total_opened_profiles.append(persID)
        
                except:
                    persID = ""
                # print(persID)
                try:
                    name = soup.find("span",{"data-anonymize":"person-name"})
                    if name is not None:
                        name=name.text
                        if "\n" in name:
                            name=name.replace("\n            ","").replace("\n          ","")
                        name_to_return = clean_name(name)
                    else:
                        name_to_return = ""
                        
                except:
                    raise
        
                try:
                    location = soup.find("span",{"class":"t-12"})
                    if location is not None:
                        location = location.text
                    else:
                        location = ""
                except:
                    location = ""
                
                    
                
                try:
                    position_title = soup.find("span",{"data-anonymize":"title"})
                    if position_title is not None:
                        position_title = position_title.text
                        if '\n' in position_title:
                            position_title = position_title.replace("\n","")
                        if '            ' in position_title:
                            position_title = position_title.replace("            "," - ")
                        if '          ' in position_title:
                            position_title = position_title.replace("          ","")
                    else:
                        position_title = ""
                except:
                    position_title = ""
                
                try:
                    position_company = soup.find("a",{"data-anonymize":"company-name"})
                    if position_company is not None:
                        position_company = position_company.text
                        if '\n' in position_company:
                            position_company = position_company.replace("\n","")
                        if '            ' in position_company:
                            position_company = position_company.replace("            "," - ")
                        if '          ' in position_company:
                            position_company = position_company.replace("          ","")
                        
                        if ' - ' in position_company:
                            position_company = position_company.replace(" - ","")
                        
                    else:
                        position_company = ""
                except:
                    position_company = "" 
                        
                    
                try:
                    duration = soup.find("div",{"class":"artdeco-entity-lockup__metadata ember-view"})
                    if duration is not None:
                        duration = duration.text
                        if '\n' in duration:
                            duration = duration.replace("\n","")
                        if '          ' in duration:
                            duration = duration.replace("          ","-")
                        if '      ' in duration:
                            duration = duration.replace("      ","")
                        if '--' in duration:
                            duration = duration.replace("--"," | ").replace("-","")
                        if '|' in duration:
                            duration_full = duration.split("|")
                            dur_in_role = duration_full[0].strip()
                            dur_in_company = duration_full[1].strip()
                        else:
                            dur_in_role = ""
                            dur_in_company = ""
                except:
                    duration = ""
                    
                try:
                    about_pers = soup.find("dd",{"class":"t-12 t-black--light mb3"})
                    if about_pers is not None:
                        about_pers = about_pers.text.replace("\n","")
                    else:
                        about_pers=""
                except:
                    about_pers = ""
                try:
                    company_SID = soup.find("a",{"class":"ember-view t-black--light t-bold inline-block"})
                    if company_SID is not None:
                        company_SID = company_SID['href']
                        company_SID = "https://www.linkedin.com"+company_SID.split("?")[0]
                    else:
                        company_SID = ""
                except:
                    company_SID=""
                gp_ppl.append([name_to_return,persID,location,position_title,position_company,dur_in_role,dur_in_company,about_pers,company_SID])
                
            # print("onfirst page: ",len(gp_ppl))
            butn = "//button[contains(@class,'artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view')]"
            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        
            try:
                element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, butn)))
                # print(element.is_enabled())
            except:
                try:
                    butn = "//button[contains(@class,'artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary artdeco-button--disabled ember-view')]"
                    element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, butn)))
                except:
                    print("not more than 25 results")
                    # PeopleInfo = {"info":[]}
                    # PeopleDetails = pd.DataFrame(columns=['Name','NameID','Location','Position','Company Name','Duration in role','Duration in company'])
                    # for ppl in gp_ppl:
                    #     new_row = {'Name':ppl[0],'NameID':ppl[1], 'Location':ppl[2], 'Position':ppl[3],'Company Name':ppl[4],'Duration in role':ppl[5],'Duration in company':ppl[6]}    
                    #     PeopleDetails = PeopleDetails.append(new_row, ignore_index=True)
                    #     # return PeopleDetails
                # print("element in except",element.is_enabled())
                
                
            count = 1
            while True and element.is_enabled()==True and max_tab>count:
                # count_false = count_false+1
                # time_ends = time.asctime()
                # print("time taken before clicking on next page is:  ",time_ends)
                driver.find_element_by_xpath(butn).click()
                time.sleep(random.uniform(2, 15))
                count+=1
                print(count)
                count_false = count
                
                moveToElement(driver,"//ol[@class='artdeco-list background-color-white _border-search-results_1igybl']" )
                time.sleep(random.uniform(2, 15))
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
                    element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, butn)))
                    # print(element.is_enabled())
                except:
                    butn = "//button[contains(@class,'artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary artdeco-button--disabled ember-view')]"
                    element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, butn)))
                            
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
                
                # companies = []
                # companyID = "LinkedIn ID"
                # gp_ppl = []
                
                for i in pers_square.extract():
                    soup = bs(i, features="lxml")
                    
                    try:
                        persID = soup.find("a",{"data-control-name":"view_lead_panel_via_search_lead_name"})['href']
                        persID = persID.split('?')[0]
                        persID = 'https://www.linkedin.com'+persID
            
                    except:
                        persID = ""
                    # print(persID)
                    try:
                        name = soup.find("span",{"data-anonymize":"person-name"})
                        if name is not None:
                            name=name.text
                            if "\n" in name:
                                name=name.replace("\n            ","").replace("\n          ","")
                            name_to_return = clean_name(name)
                        else:
                            name_to_return = ""
                            
                    except:
                        raise
            
                    try:
                        location = soup.find("span",{"class":"t-12"})
                        if location is not None:
                            location = location.text
                        else:
                            location = ""
                    except:
                        location = ""
                    
                        
                    
                    try:
                        position_title = soup.find("span",{"data-anonymize":"title"})
                        if position_title is not None:
                            position_title = position_title.text
                            if '\n' in position_title:
                                position_title = position_title.replace("\n","")
                            if '            ' in position_title:
                                position_title = position_title.replace("            "," - ")
                            if '          ' in position_title:
                                position_title = position_title.replace("          ","")
                        else:
                            position_title = ""
                    except:
                        position_title = ""
                    
                    try:
                        position_company = soup.find("a",{"data-anonymize":"company-name"})
                        if position_company is not None:
                            position_company = position_company.text
                            if '\n' in position_company:
                                position_company = position_company.replace("\n","")
                            if '            ' in position_company:
                                position_company = position_company.replace("            "," - ")
                            if '          ' in position_company:
                                position_company = position_company.replace("          ","")
                            
                            if ' - ' in position_company:
                                position_company = position_company.replace(" - ","")
                            
                        else:
                            position_company = ""
                    except:
                        position_company = "" 
                            
                        
                    
                    try:
                        duration = soup.find("div",{"class":"artdeco-entity-lockup__metadata ember-view"})
                        if duration is not None:
                            duration = duration.text
                            if '\n' in duration:
                                duration = duration.replace("\n","")
                            if '          ' in duration:
                                duration = duration.replace("          ","-")
                            if '      ' in duration:
                                duration = duration.replace("      ","")
                            if '--' in duration:
                                duration = duration.replace("--"," | ").replace("-","")
                            if '|' in duration:
                                duration_full = duration.split("|")
                                dur_in_role = duration_full[0].strip()
                                dur_in_company = duration_full[1].strip()
                            else:
                                dur_in_role = ""
                                dur_in_company = ""
                    except:
                        duration = ""
                            
                    try:
                        about_pers = soup.find("dd",{"class":"t-12 t-black--light mb3"})
                        if about_pers is not None:
                            about_pers = about_pers.text
                        else:
                            about_pers=""
                    except:
                        about_pers = ""
                        
                    try:
                        company_SID = soup.find("a",{"class":"ember-view t-black--light t-bold inline-block"})
                        if company_SID is not None:
                            company_SID = company_SID['href']
                            company_SID = "https://www.linkedin.com"+company_SID.split("?")[0]
                        else:
                            company_SID = ""
                    except:
                        company_SID=""
                    gp_ppl.append([name_to_return,persID,location,position_title,position_company,dur_in_role,dur_in_company,about_pers,company_SID])
                    
                
                    # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                
                    # PeopleInfo = {"info":[]}
                    # PeopleDetails = pd.DataFrame(columns=['Name','NameID','Location','Position','Company Name','Duration in role','Duration in company'])
                    # for ppl in gp_ppl:
                    #     new_row = {'Name':ppl[0],'NameID':ppl[1], 'Location':ppl[2], 'Position':ppl[3],'Company Name':ppl[4],'Duration in role':ppl[5],'Duration in company':ppl[6]}    
                    #     PeopleDetails = PeopleDetails.append(new_row, ignore_index=True)
                    
                    
    
    result_to_return = [gp_ppl,count_false]
    return result_to_return
    
def detailed_data_true(driver,max_tab):
    total_opened_profiles = []
    selector = Selector(text=driver.page_source)
    gp_ppl = []
    strueOpenedProf = []
    salesIDS= []
    all_people_i=[]
    
    list_of_ppl = selector.xpath("//ol[@class='artdeco-list background-color-white _border-search-results_1igybl']")
    
    pers_square = list_of_ppl.xpath("//li[@class='artdeco-list__item pl3 pv3 ']")
    
        
    if len(pers_square)!=0 and len(pers_square)<=25 and (max_tab == 1 or (max_tab!=1 and check_navigator(driver)==False) ) :
            count_false = 1
            for i in pers_square.extract():
                soup = bs(i, features="lxml")
                
                
                try:
                    persID = soup.find("a",{"data-control-name":"view_lead_panel_via_search_lead_name"})['href']
                    persID = persID.split('?')[0]
                    persID = 'https://www.linkedin.com'+persID
                    # print(persID)
                    salesIDS.append(persID)
                    
        
                except:
                    persID = ""
                # print(persID)
                try:
                    name = soup.find("span",{"data-anonymize":"person-name"})
                    if name is not None:
                        name=name.text
                        if "\n" in name:
                            name=name.replace("\n            ","").replace("\n          ","")
                        name_to_return = clean_name(name)
                    else:
                        name_to_return = ""
                        
                except:
                    raise
        
                try:
                    location = soup.find("span",{"class":"t-12"})
                    if location is not None:
                        location = location.text
                    else:
                        location = ""
                except:
                    location = ""
                
                    
                
                try:
                    position_title = soup.find("span",{"data-anonymize":"title"})
                    if position_title is not None:
                        position_title = position_title.text
                        if '\n' in position_title:
                            position_title = position_title.replace("\n","")
                        if '            ' in position_title:
                            position_title = position_title.replace("            "," - ")
                        if '          ' in position_title:
                            position_title = position_title.replace("          ","")
                    else:
                        position_title = ""
                except:
                    position_title = ""
                
                try:
                    position_company = soup.find("a",{"data-anonymize":"company-name"})
                    if position_company is not None:
                        position_company = position_company.text
                        if '\n' in position_company:
                            position_company = position_company.replace("\n","")
                        if '            ' in position_company:
                            position_company = position_company.replace("            "," - ")
                        if '          ' in position_company:
                            position_company = position_company.replace("          ","")
                        
                        if ' - ' in position_company:
                            position_company = position_company.replace(" - ","")
                        
                    else:
                        position_company = ""
                except:
                    position_company = "" 
                        
                    
                try:
                    duration = soup.find("div",{"class":"artdeco-entity-lockup__metadata ember-view"})
                    if duration is not None:
                        duration = duration.text
                        if '\n' in duration:
                            duration = duration.replace("\n","")
                        if '          ' in duration:
                            duration = duration.replace("          ","-")
                        if '      ' in duration:
                            duration = duration.replace("      ","")
                        if '--' in duration:
                            duration = duration.replace("--"," | ").replace("-","")
                        if '|' in duration:
                            duration_full = duration.split("|")
                            dur_in_role = duration_full[0].strip()
                            dur_in_company = duration_full[1].strip().strip()
                        else:
                            dur_in_role = ""
                            dur_in_company = ""
                except:
                    dur_in_role = ""
                    dur_in_company = ""
                    
                    
                
                person_full = [persID,name_to_return,location,position_title,position_company,dur_in_role,dur_in_company]
                all_people_i.append(person_full)
                for set_ppl in all_people_i:
                    # print(set_ppl)
                    if set_ppl[0]!="":
                        if set_ppl[0] not in total_opened_profiles:
                            total_opened_profiles.append(set_ppl[0])
                            
                            sales_info = advanced_search_people_profile(driver,set_ppl[0])
                            finalthig = [set_ppl[0],set_ppl[1],set_ppl[2],set_ppl[3],set_ppl[4],set_ppl[5],set_ppl[6]]
                            
                            
                            for sale_fn in sales_info:
                                # print(sale_fn)
                                
                                fn_sale = [sale_fn[0],sale_fn[1],sale_fn[2],sale_fn[3],sale_fn[4],sale_fn[5],sale_fn[6],sale_fn[7],sale_fn[8],sale_fn[9]]
                                all_prof_info = finalthig+fn_sale
                                
                                strueOpenedProf.append(all_prof_info)
                    # final_opened_prof = [x for i,x in enumerate(strueOpenedProf) if x not in strueOpenedProf[i+1:]]
        
                      
    elif len(pers_square)!=0 and len(pers_square)<=25 and (max_tab !=1 and check_navigator(driver)==True) :
        for i in pers_square.extract():
                soup = bs(i, features="lxml")
                
                try:
                    persID = soup.find("a",{"data-control-name":"view_lead_panel_via_search_lead_name"})['href']
                    persID = persID.split('?')[0]
                    persID = 'https://www.linkedin.com'+persID
                    
        
                except:
                    persID = ""
                # print(persID)
                try:
                    name = soup.find("span",{"data-anonymize":"person-name"})
                    if name is not None:
                        name=name.text
                        if "\n" in name:
                            name=name.replace("\n            ","").replace("\n          ","")
                        name_to_return = clean_name(name)
                    else:
                        name_to_return = ""
                        
                except:
                    raise
        
                try:
                    location = soup.find("span",{"class":"t-12"})
                    if location is not None:
                        location = location.text
                    else:
                        location = ""
                except:
                    location = ""
                
                    
                
                try:
                    position_title = soup.find("span",{"data-anonymize":"title"})
                    if position_title is not None:
                        position_title = position_title.text
                        if '\n' in position_title:
                            position_title = position_title.replace("\n","")
                        if '            ' in position_title:
                            position_title = position_title.replace("            "," - ")
                        if '          ' in position_title:
                            position_title = position_title.replace("          ","")
                    else:
                        position_title = ""
                except:
                    position_title = ""
                
                try:
                    position_company = soup.find("a",{"data-anonymize":"company-name"})
                    if position_company is not None:
                        position_company = position_company.text
                        if '\n' in position_company:
                            position_company = position_company.replace("\n","")
                        if '            ' in position_company:
                            position_company = position_company.replace("            "," - ")
                        if '          ' in position_company:
                            position_company = position_company.replace("          ","")
                        
                        if ' - ' in position_company:
                            position_company = position_company.replace(" - ","")
                        
                    else:
                        position_company = ""
                except:
                    position_company = "" 
                        
                    
                try:
                    duration = soup.find("div",{"class":"artdeco-entity-lockup__metadata ember-view"})
                    if duration is not None:
                        duration = duration.text
                        if '\n' in duration:
                            duration = duration.replace("\n","")
                        if '          ' in duration:
                            duration = duration.replace("          ","-")
                        if '      ' in duration:
                            duration = duration.replace("      ","")
                        if '--' in duration:
                            duration = duration.replace("--"," | ").replace("-","")
                        if '|' in duration:
                            duration_full = duration.split("|")
                            dur_in_role = duration_full[0].strip()
                            dur_in_company = duration_full[1].strip()
                        else:
                            dur_in_role = ""
                            dur_in_company = ""
                except:
                    duration = ""
                    
                
                    
                all_people_i.append([persID,name_to_return,location,position_title,position_company,dur_in_role,dur_in_company])
                
            # print("onfirst page: ",len(gp_ppl))
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
            time.sleep(random.uniform(3, 4))
            count+=1
            print("count::::   ",count)
            
            moveToElement(driver,"//ol[@class='artdeco-list background-color-white _border-search-results_1igybl']" )
            time.sleep(random.uniform(2, 3))
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
            
        
            
            try:
                element = WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.XPATH, butn)))
                # print(element.is_enabled())
            except:
                butn = "//button[contains(@class,'artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary artdeco-button--disabled ember-view')]"
                element = WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.XPATH, butn)))
                        
            moveToElement(driver,"//ol[@class='artdeco-list background-color-white _border-search-results_1igybl']" )
            time.sleep(random.uniform(1, 2))
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
            
            # companies = []
            # companyID = "LinkedIn ID"
            # gp_ppl = []
            
            for i in pers_square.extract():
                soup = bs(i, features="lxml")
                
                try:
                    persID = soup.find("a",{"data-control-name":"view_lead_panel_via_search_lead_name"})['href']
                    persID = persID.split('?')[0]
                    persID = 'https://www.linkedin.com'+persID
        
                except:
                    persID = ""
                # print(persID)
                try:
                    name = soup.find("span",{"data-anonymize":"person-name"})
                    if name is not None:
                        name=name.text
                        if "\n" in name:
                            name=name.replace("\n            ","").replace("\n          ","")
                        name_to_return = clean_name(name)
                    else:
                        name_to_return = ""
                        
                except:
                    raise
        
                try:
                    location = soup.find("span",{"class":"t-12"})
                    if location is not None:
                        location = location.text
                    else:
                        location = ""
                except:
                    location = ""
                
                    
                
                try:
                    position_title = soup.find("span",{"data-anonymize":"title"})
                    if position_title is not None:
                        position_title = position_title.text
                        if '\n' in position_title:
                            position_title = position_title.replace("\n","")
                        if '            ' in position_title:
                            position_title = position_title.replace("            "," - ")
                        if '          ' in position_title:
                            position_title = position_title.replace("          ","")
                    else:
                        position_title = ""
                except:
                    position_title = ""
                
                try:
                    position_company = soup.find("a",{"data-anonymize":"company-name"})
                    if position_company is not None:
                        position_company = position_company.text
                        if '\n' in position_company:
                            position_company = position_company.replace("\n","")
                        if '            ' in position_company:
                            position_company = position_company.replace("            "," - ")
                        if '          ' in position_company:
                            position_company = position_company.replace("          ","")
                        
                        if ' - ' in position_company:
                            position_company = position_company.replace(" - ","")
                        
                    else:
                        position_company = ""
                except:
                    position_company = "" 
                        
                    
                
                try:
                    duration = soup.find("div",{"class":"artdeco-entity-lockup__metadata ember-view"})
                    if duration is not None:
                        duration = duration.text
                        if '\n' in duration:
                            duration = duration.replace("\n","")
                        if '          ' in duration:
                            duration = duration.replace("          ","-")
                        if '      ' in duration:
                            duration = duration.replace("      ","")
                        if '--' in duration:
                            duration = duration.replace("--"," | ").replace("-","")
                        if '|' in duration:
                            duration_full = duration.split("|")
                            dur_in_role = duration_full[0].strip()
                            dur_in_company = duration_full[1].strip()
                        else:
                            dur_in_role = ""
                            dur_in_company = ""
                except:
                    duration = ""
                        
                
                    
                all_people_i.append([persID,name_to_return,location,position_title,position_company,dur_in_role,dur_in_company])
                
        for set_ppl in all_people_i:
            # print(set_ppl)
            if set_ppl[0]!="":
                if set_ppl[0] not in total_opened_profiles:
                    total_opened_profiles.append(set_ppl[0])
                    # print(set_ppl[0])
                    sales_info = advanced_search_people_profile(driver,set_ppl[0])
                    
                    finalthig = [set_ppl[0],set_ppl[1],set_ppl[2],set_ppl[3],set_ppl[4],set_ppl[5],set_ppl[6]]
                    
                    
                    for sale_fn in sales_info:
                        # print(sale_fn)
                        try:
                            fn_sale = [sale_fn[0],sale_fn[1],sale_fn[2],sale_fn[3],sale_fn[4],sale_fn[5],sale_fn[6],sale_fn[7],sale_fn[8],sale_fn[9]]
                        except:
                            fn_sale = []
                        all_prof_info = finalthig+fn_sale
                        
                        strueOpenedProf.append(all_prof_info)
            
        
             
            
    
    else:
        raise
    
   
    result_to_return = [strueOpenedProf,len(total_opened_profiles)]
    return result_to_return
            
            
            
            
            

                                   
                
    
def sales_search(driver,search_link,detailed_data,max_tab,return_counts_only=False):
   
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
            sales_result_number =driver.find_element_by_xpath("//div[contains(@class, 't-14 flex align-items-center mlA pl3')]").text.split("result")[0]
            sales_result_number = int(sales_result_number)
            
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
                biglist
                salesInfo['sales'].append({'name':biglist[0],
                                                  'person_sales_url':biglist[1],
                                                  'location': biglist[2],
                                                  'position':biglist[3],
                                                  'company_name':biglist[4],
                                                  'duration_in_role':biglist[5].split(" in")[0],
                                                  'duration_in_company':biglist[6].split(" in")[0],
                                                  'about_person':biglist[7],
                                                  'company_sales_link':biglist[8]
                                                  
                                                  }) 
                      
                salesInfo['number_of_tabs']=sales_detailed_data[1]
                
            
                
        if detailed_data == True:
            salesInfo = {"sales":[]}
            sales_detailed_data = detailed_data_true(driver, max_tab)
            
            for biglist in sales_detailed_data[0]:
                
                salesInfo['sales'].append({'person_sales_url':biglist[0],
                                                  'name':biglist[1],
                                                  'location': biglist[2],
                                                  'position':biglist[3],
                                                  'company_name':biglist[4],
                                                  'duration_in_role':biglist[5].split(" in")[0],
                                                  'duration_in_company':biglist[6].split(" in")[0],
                                                  'header':biglist[7],
                                                  'company_sales_link':biglist[8],
                                                  'experience_start_year':biglist[9],
                                                  'experience_end_year':biglist[10],
                                                  'person_linkedin_url':biglist[11],
                                                  'experience_position':biglist[12],
                                                  'experience_company_name':biglist[13],
                                                  'about_person':biglist[14],
                                                  'experience_linkedin_url':biglist[15],
                                                  'experience_website':biglist[16]
                                                  }) 
                      
                salesInfo['number_of_profile_opened']=sales_detailed_data[1]
                
           
                
        test_list = salesInfo['sales']
        done = set()
        result_set = []
        for d in test_list:
            done.add(d['person_sales_url']) 
            result_set.append(d)
                
        if detailed_data == True:
            return_result = result_set,salesInfo['number_of_profile_opened'],""
        if detailed_data == False:
            return_result = result_set,salesInfo['number_of_tabs'],""
        print("adv sales result : ",return_result)
        return return_result

# # import pandas as pd
# if __name__ == '__main__':
    
# # # # # # # # # # #         time_Start = time.asctime()
        
#         username="rroobbiinngghhaazzaall99@gmail.com"
#         password="roby1234"                       
#         driver=login(username, password) 
        
# # # #         df = pd.read_csv("/home/joy/Desktop/html_adv_loops/output-2611-queue-2024-work.csv")
# # # #         for index, row in df.iterrows():
# # # #             print(index)
# # # #             print(row['link_of_pers'])
# # # #             # break
# # # #             sale_id = row['link_of_pers']
# # # #             rst1 = get_advanced_search_people_profile(driver, sale_id)
            
# # # #             profile_li_id = rst1[0][0]['person_linkedin_url'].split("/in/")[1].rstrip("/")
# # # #             sales_link = sale_id.split("/sales/lead/")[1]
# # # #             add_sales_id_people(profile_li_id, sales_link) 
            
            
# # # #             processed_dict = {"processed":{"num_of_profiles":1, "result_main": {"error": None,"error_field":None,"result": rst1[0] },"detailed_data":True}}
# # # #             processed_dict["last_updated"] = datetime.datetime.utcnow()
# # # #             db.collection("ppl_search_advanced").document(row['req_target']).set(processed_dict, merge=True)


                        
        
# # # #             # Get tasks reference
# # # #             tasks_ref = (db.collection("automation")
# # # #                           .document("current")
# # # #                           .collection("requests")
# # # #                           .document("r1_26112024_adhoc_1")
# # # #                           .collection("tasks"))
            
# # # #             # Update task status (add this if needed)
# # # #             tasks_ref.document(row['req_id']).update({'status': "processed_success"})
            
        
        
        
# # # # # # # #         search_link = "https://www.linkedin.com/sales/search/people?query=(recentSearchParam%3A(doLogHistory%3Atrue)%2Cfilters%3AList((type%3ACURRENT_COMPANY%2Cvalues%3AList((id%3Aurn%253Ali%253Aorganization%253A74126343%2Ctext%3AAnthropic%2CselectionType%3AINCLUDED)))))&sessionId=WAt1z7UyRYmCBk2Xft6bjw%3D%3D"
# # # # # # # #         detailed_data = False
# # # # # # # #         return_counts_only=False
# # # # # # # #         max_tab = 100
        
# # # # # # # #         resul = sales_search(driver, search_link, detailed_data, max_tab,return_counts_only)
# # # # # # #         # saleID="https://www.linkedin.com/sales/lead/ACoAADK4Sm8B61xM3TWbrybEvveuLzFPXe7bpQA,name,S89h"
#         saleID="https://www.linkedin.com/sales/lead/ACwAAA7CnGIBqyunSTxUTa4oHFNSYcUEwxJnnng,NAME_SEARCH,kOwB"
#         driver.get(saleID)
#         rst1 = get_advanced_search_people_profile(driver, saleID)
#         profile_li_id = rst1[0][0]['person_linkedin_url'].split("/in/")[1].rstrip("/")
#         sales_link = saleID.split("/sales/lead/")[1]
# #         sale_id = sales_link.split("/sales/lead/")[1]
#         add_sales_id_people(profile_li_id, sales_link) 
#         processed_dict = {"processed":{"num_of_profiles":1, "result_main": {"error": None,"error_field":None,"result": rst1[0] },"detailed_data":True}}
#         processed_dict["last_updated"] = datetime.datetime.utcnow()
#         db.collection("ppl_search_advanced").document("DRTWENTY21+ACCEL_UNICORN_P5_OTHER____anchorage_2__ACwAAA7CnGIBqyunSTxUTa4oHFNSYcUEwxJnnng,NAME_SEARCH,kOwB+12012025+70414798").set(processed_dict, merge=True)

        
        
        
        
        
        
        
        
        
        
        
        
        
        
# # # # # # # # # # # # # # # # # # # # # #         time_end = time.asctime()

# # # # # # # # rst1 = []
# # # # # # # # rst1=[[{'header': 'Jenny’s fiancé. Kai Dad. Lulus favorite human. Founder and CEO.',
# # # # # # # #         'company_sales_link': '',
# # # # # # # #         'experience_start_year': '', 
# # # # # # # #         'experience_end_year': '',
# # # # # # # #         'person_linkedin_url': 'https://www.linkedin.com/in/lucisewell',
# # # # # # # #         'experience_position': '',
# # # # # # # #         'experience_company_name': '',
# # # # # # # #         'about_person': "",
# # # # # # # #         'location': 'Santa Clara, California, United States', 
# # # # # # # #         'name': 'Luciano S', 
# # # # # # # #         'experience_linkedin_url': '', 
# # # # # # # #         'experience_website': '',
# # # # # # # #         'person_sales_url': saleID}]]



# target = "DRTWENTY21+ACCEL_P5_TEST_2__ACwAAAC5YmMB7R0x16Y5tOrrApw3cDUUbrAvQ1o,NAME_SEARCH,kCOy+28112024+33673868"
# processed_dict = {"processed":{"num_of_profiles":1, "result_main": {"error": None,"error_field":None,"result": rst1[0] },"detailed_data":True}}
# processed_dict["last_updated"] = datetime.datetime.utcnow()
# db.collection("ppl_search_advanced").document(target).set(processed_dict, merge=True)

# tasks_ref = db.collection("automation").document("current").collection("requests").document("r1_14062024_adhoc_1").collection("tasks")
            
# another_query = tasks_ref.where("target", "==", target).stream()
# for task_doc in another_query:
#     task_doc.reference.update({"status": "processed_success"})
# db.collection("automation").document("current").collection("requests").document(
#             "r1_14062024_adhoc_1").collection("tasks").document(
#                 "DRTWENTY21+JISA0LDG1LX9MHX+14062024+21519685").update({'status':"processed_success"})


# db.collection("ppl_search_advanced").document("DRTWENTY21+08LWDHM8KTCO84S+26042024+55279869").set(processed_dict, merge=True)






# data = resul[0]
# keys = data[0].keys()

# # Write the data to the CSV file
# with open("/home/joy/Desktop/Linkedin/ribal-employees/current-anthropic-4tabs.csv", 'w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=keys)
    
#     # Write header
#     writer.writeheader()
    
#     # Write rows
#     for row in data:
#         writer.writerow(row)

# print('CSV file created successfully:', csv_file)




