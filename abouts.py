#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 16:34:16 2021

@author: joy
"""
from selenium.common.exceptions import NoSuchElementException,TimeoutException

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs

import time
from time import sleep
from selenium.webdriver.common.keys import Keys

from random import randint
import random

from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector
# import pandas as pd
import datetime
from utils import linkedin_login as login, page_doesnt_exist_check, getNumberOfEmployees


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

if not firebase_admin._apps:
    cred = credentials.Certificate('spherical-list-284723-216944ab15f1.json') 
    default_app = firebase_admin.initialize_app(cred)

db = firestore.client()
def check_exists_by_xpath(driver, xpath):
 
    try:

        driver.find_element_by_xpath(xpath)

    except NoSuchElementException:

        return True

    return False


def moveToElement(driver, target_xpath):

    try:
        target = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, target_xpath))
        )
        ActionChains(driver).move_to_element(target).perform()
        return True
    except:
        return False
    
    
def getNumberOfEmployees_old_way(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'link-without-visited-state') and contains(text(), 'employee')]"))
        ).click()
        
        time.sleep(1)
         
        if 'currentCompany' not in driver.current_url:
         
             numeric_link = driver.current_url.split("%5B%22")[1].split("%22%5D")[0]
             
             driver.get("https://www.linkedin.com/search/results/people/?currentCompany=%5B%22"+numeric_link+"%22%5D&origin=FACETED_SEARCH&sid=EYp")
             time.sleep(random.uniform(5, 10))
         
        try:
             numberOfEmployees = driver.find_element_by_xpath("//h2[contains(@class, 'pb2 t-black--light t-14')]").text.split("result")[0]
             
             if 'About' in numberOfEmployees:
                 numberOfEmployees = numberOfEmployees.split("About ")[1]
            
             else:
                 numberOfEmployees = numberOfEmployees
            
             
            
        
        except:
            numberOfEmployees = 0   
            numberOfEmployees_to_return  =  numberOfEmployees   
             
    except TimeoutException:
        # raise
        numberOfEmployees = 0
        numberOfEmployees_to_return = 0
    
    if numberOfEmployees != 0 :
        if ',' in numberOfEmployees:
            numberOfEmployees = numberOfEmployees.replace(",","")
           
        elif 'k' in numberOfEmployees or 'K' in numberOfEmployees:
            try:
                numberOfEmployees = int(numberOfEmployees.replace("k",""))*1000
            except:
                numberOfEmployees = int(numberOfEmployees.replace("K",""))*1000
       
        elif 'm' in numberOfEmployees or 'M' in numberOfEmployees:
            try:
                numberOfEmployees = int(numberOfEmployees.replace("m",""))*1000000
            except:
                numberOfEmployees = int(numberOfEmployees.replace("M",""))*1000000
            
        numberOfEmployees_to_return = int(numberOfEmployees)
        
    return  numberOfEmployees_to_return

# def get_numberOFEmployees_old_way(driver):
    
#     try:
#         numberOfEmployees = driver.find_element_by_xpath(
#             "//span[@class= 'v-align-middle']"
#         )
#         numberOfEmployees = numberOfEmployees.text
#         numberOfEmployees = numberOfEmployees.split("See ")[1].split(" employee")[0]
#         if "all" in numberOfEmployees:
#             numberOfEmployees = numberOfEmployees.split("all ")[1]
#         try:
#             numberOfEmployees = int(numberOfEmployees.replace(",", ""))

#         except:
#             numberOfEmployees = int(numberOfEmployees)

#     except:
#         try:
#             numberOfEmployees = driver.find_element_by_xpath(
#                 "//span[@class='link-without-visited-state t-bold t-black--light']"
#             )
#             numberOfEmployees = numberOfEmployees.text
#             numberOfEmployees = numberOfEmployees.split("See ")[1].split(
#                 " employee"
#             )[0]
#             if "all" in numberOfEmployees:
#                 numberOfEmployees = numberOfEmployees.split("all ")[1]
#             try:
#                 numberOfEmployees = int(numberOfEmployees.replace(",", ""))

#             except:
#                 numberOfEmployees = int(numberOfEmployees)

#         except:
#                 try:
#                     numberOfEmployees = driver.find_element_by_xpath(
#                         "//span[@class='org-top-card-secondary-content__see-all t-normal t-black--light link-without-visited-state link-without-hover-state']"
#                         ).text
#                     if 'employee' in numberOfEmployees:
#                         numberOfEmployees = numberOfEmployees.split(" employee")[0]
#                     if 'all' in numberOfEmployees:
#                         numberOfEmployees = numberOfEmployees.split("all ")[1]
                    
#                     try:
#                         numberOfEmployees = int(numberOfEmployees.replace(",",""))

#                     except:
#                         numberOfEmployees = int(numberOfEmployees)


#                 except:
#                     numberOfEmployees = 0
#                     numberOfEmployees = int(numberOfEmployees)
                    
                    
#     if numberOfEmployees == 0:
#         try:
#             numberOfEmployees = driver.find_element_by_xpath(
#                 "//span[@class='t-normal t-black--light link-without-visited-state link-without-hover-state']"
#                 ).text
#             if 'employee' in numberOfEmployees:
#                 numberOfEmployees = numberOfEmployees.split(" employee")[0]
            
#             if 'all' in numberOfEmployees:
#                 numberOfEmployees = numberOfEmployees.split("all ")[1]
            
#             try:
#                 numberOfEmployees = int(numberOfEmployees.replace(",",""))

#             except:
#                 try:
#                     numberOfEmployees = int(numberOfEmployees)
#                 except:
#                     if '-' in numberOfEmployees:
#                         driver.find_element_by_xpath("//span[@class='t-normal t-black--light link-without-visited-state link-without-hover-state']").click()
#                         time.sleep(random.uniform(5, 10))
#                         numberOfEmployees = driver.find_element_by_xpath("//h2[contains(@class, 'pb2 t-black--light t-14')]").text.split("result")[0]
#                         try:
#                             numberOfEmployees= int(numberOfEmployees)
#                         except:
#                             numberOfEmployees = int(numberOfEmployees.replace(",",""))

#         except:
#             try:
#                 # empl= driver.find_element_by_xpath1("t-normal t-black--light link-without-visited-state link-without-hover-state").text
#                 numberOfEmployees=driver.find_element_by_xpath("//span[contains(@class, 't-normal t-black--light link-without-visited-state link-without-hover-state')]").text
#                 numberOfEmployees = numberOfEmployees.split(" employee")[0]
            
#                 if 'all' in numberOfEmployees:
#                     numberOfEmployees = numberOfEmployees.split("all ")[1]
#                 else:
#                     try:
#                         numberOfEmployees= int(numberOfEmployees)
#                     except:
#                         numberOfEmployees = int(numberOfEmployees.replace(",",""))
#                 try:
#                     numberOfEmployees= int(numberOfEmployees)
#                 except:
#                     numberOfEmployees = int(numberOfEmployees.replace(",",""))
           
            
#             except:
#                 numberOfEmployees = 0
                
#     # if numberOfEmployees == 0:
#     #     try:
#     #         click_el = driver.find_element_by_xpath("")
#     driver.execute_script("window.history.go(-1)")
#     return numberOfEmployees

def getAbouts(driver, link):
    # try:
    #     if moveToElement(driver,"//*[contains(text(), ' do a quick security check')]"):
    #         print("Security Check is needed")
    #     return "sec_check"
    # except:
    #     pass

    link = link + "/about/"

    if "linkedin.com/" not in link:
        aboutDict = {"about": []}
        aboutDict["about"].append(
            {
                "Name":"",
                "updated_Link": "",
                "Overview": "",
                "Website": "",
                "Industry": "",
                "Headquarters": "",
                "CompanySize": "",
                "CompType": "",
                "Founded": "",
                "Speciality": "",
                # "Phone":"",
                "location": "",
                "Warning": "",
                "date_collected": "",
                "numberOfEmployees": 0,
                "company_logo_link": "",
                "verified":"",
                "error":None,
            }
        )
        return aboutDict

    if "linkedin.com/" in link:
        try:
            driver.get(link)
            time.sleep(random.uniform(5, 10))
        except TimeoutException:
            print("Here's the timeout in experience. Refreshing...")
            driver.refresh()
            time.sleep(random.uniform(5, 10))
            driver.get(link)
            time.sleep(random.uniform(5, 10))
        
        time.sleep(random.uniform(4, 9))
        try:
            if moveToElement(
                driver,
                "//*[contains(text(), 'Uh oh, we can’t seem to find the page you’re looking for')]",
            ):
                aboutDict = {"about": []}
                aboutDict["about"].append(
                    {
                        "Name":"",
                        "updated_Link": link,
                        "Overview": "",
                        "Website": "",
                        "Industry": "",
                        "Headquarters": "",
                        "CompanySize": "",
                        "CompType": "",
                        "Founded": "",
                        "Speciality": "",
                        # "Phone":"",
                        "location": "",
                        "Warning": "",
                        "date_collected": "",
                        "numberOfEmployees": 0,
                        "company_logo_link": "",
                        "verified":"",
                        "error":"page_doesnt_exist",
                    }
                )
                aboutDict["about"][0]['error'] = "page_doesnt_exist"
                return aboutDict

        except:
            pass


        if page_doesnt_exist_check(driver):
            aboutDict = {"about": []}
            aboutDict["about"].append(
                {
                    "Name":"",
                    "updated_Link": link,
                    "Overview": "",
                    "Website": "",
                    "Industry": "",
                    "Headquarters": "",
                    "CompanySize": "",
                    "CompType": "",
                    "Founded": "",
                    "Speciality": "",
                    # "Phone":"",
                    "location": "",
                    "Warning": "",
                    "date_collected": "",
                    "numberOfEmployees": 0,
                    "company_logo_link": "",
                    "verified":"",
                    "error":"page_doesnt_exist",
                    
                }
            )
            # aboutDict["about"][0]['error'] = "page_doesnt_exist"
            return aboutDict

        updated_Link = driver.current_url
        if (
            "/checkpoint/challenges" in updated_Link
            or "login?session_redirect" in updated_Link
            or "authwall?trk" in updated_Link
            or updated_Link == "https://www.linkedin.com/"
        ):
            return "security_check"
        if updated_Link == "https://www.linkedin.com/404/":
            aboutDict = {"about": []}
            aboutDict["about"].append(
                {
                    "Name":"",
                    "updated_Link": link,
                    "Overview": "",
                    "Website": "",
                    "Industry": "",
                    "Headquarters": "",
                    "CompanySize": "",
                    "CompType": "",
                    "Founded": "",
                    "Speciality": "",
                    # "Phone":"",
                    "location": "",
                    "Warning": "",
                    "date_collected": "",
                    "numberOfEmployees": 0,
                    "company_logo_link": "",
                    "verified":"",
                    "error":"page_doesnt_exist",
                    
                }
            )
            # aboutDict["about"][0]['error'] = "page_doesnt_exist"
            return aboutDict
        
        if updated_Link == "https://www.linkedin.com/company/unavailable/":
            print("PAGE UNAVAILABLE")  # ✅ Debugging step
            aboutDict = {"about": []}
            aboutDict["about"].append(
                {
                    "Name": "",
                    "updated_Link": link,
                    "Overview": "",
                    "Website": "",
                    "Industry": "",
                    "Headquarters": "",
                    "CompanySize": "",
                    "CompType": "",
                    "Founded": "",
                    "Speciality": "",
                    "location": "",
                    "Warning": "",
                    "date_collected": "",
                    "numberOfEmployees": 0,
                    "company_logo_link": "",
                    "verified": "",
                    "error": "page_doesnt_exist",
                }
            )
            return aboutDict
        
        
        try:
            smtg_wrong = driver.find_element_by_xpath("//h2[@class='artdeco-empty-state__headline artdeco-empty-state__headline--mercado-error-server-small artdeco-empty-state__headline--mercado-spots-small']")
            smtg_wrong = smtg_wrong.text
            if 'Something went wrong' in smtg_wrong:
                aboutDict = {"about": []}
                aboutDict["about"].append(
                    {
                        "Name":"",
                        "updated_Link": link,
                        "Overview": "",
                        "Website": "",
                        "Industry": "",
                        "Headquarters": "",
                        "CompanySize": "",
                        "CompType": "",
                        "Founded": "",
                        "Speciality": "",
                        # "Phone":"",
                        "location": "",
                        "Warning": "",
                        "date_collected": "",
                        "numberOfEmployees": 0,
                        "company_logo_link": "",
                        "verified":"",
                        "error":"page_doesnt_exist",
                        
                    }
            )
            # aboutDict["about"][0]['error'] = "page_doesnt_exist"
            return aboutDict
        except:
            pass
        
        numberOfEmployees = 0
        Name = ""
        OverView = ""
        Website = ""
        industry = ""

        Headquarters = ""
        CompanySize = ""
        CompType = ""
        verified = ""
        Founded = ""
        Specialties = ""
        location = ""
        # phone = ""
        warn = ""
        date_collected = ""
        try:
            date_collected = datetime.date.today().strftime("%d-%b-%y")
        except Exception as e:
            date_collected = ""
            print(e)

        time.sleep(randint(1, 3))

        try:
            company_logo_link = driver.find_element_by_xpath("//div[@class='org-top-card-primary-content__logo-container']/img")
            # company_logo_link = driver.find_element_by_xpath(
            #     "//div[@class='org-top-card-primary-content__logo-container']/img[@class='lazy-image ember-view org-top-card-primary-content__logo']"
            # )
            company_logo_link = company_logo_link.get_attribute("src")

        except:
            print("There is no logo link")
            company_logo_link = ""
        try:
            Name = driver.find_element_by_xpath(
                "//div[@class='block mt2']//span[@dir='ltr']"
                )
            Name = Name.text

        except:
            try:
                Name = driver.find_element_by_xpath(
                "//h1[contains(@class,'ember-view org-top-card-summary__title')]"
                )
                Name = Name.text
            except:
                print("NO NAME?")
                Name = ""


        driver.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
        time.sleep(randint(1, 3))
        try:
            OverView = driver.find_element_by_xpath(
                "//p[@class='break-words white-space-pre-wrap mb5 t-14 t-black--light t-normal']"
            )
            OverView = OverView.text
        except:
            
            try:
                OverView = driver.find_element_by_xpath("//p[contains(@class,'break-words white-space-pre-wrap t-black--light')]")
                    
                
                OverView = OverView.text
            except:
                print("No overview")
                OverView = ""
        try:
            dts0 = driver.find_elements_by_xpath("//dl[contains(@class,'overflow-hidden')]")
            

            for dt in dts0:
                if "Website" in dt.get_attribute("innerText"):
                    inner_text = dt.get_attribute("innerText")
                    lines = inner_text.split('\n')

                    # Loop through the lines to find the website
                    Website = None
                    for i, line in enumerate(lines):
                        if "Website" in line:
                            # Assuming the website URL is on the next line
                            if i + 1 < len(lines):
                                Website = lines[i + 1]
                                break
            # for dt in dts0:
            #     if "Website" om dt.get_attribute("innerText") == "Website":
            #         Website = (
            #             dt.get_attribute("innerText")
            #             + "-"
            #             + dt.find_element_by_xpath("./following-sibling::dd").text
            #         )
            #         Website = Website.split("Website-")[1]

        except:
            Website = ""
        try:
            dts1 = driver.find_elements_by_xpath("//dl[contains(@class,'overflow-hidden')]")
            for dt in dts1:
                if "Industry" in dt.get_attribute("innerText"):
                    inner_text_ind = dt.get_attribute("innerText")
                    lines_ind = inner_text_ind.split('\n')

                    # Loop through the lines to find the website
                    industry = None
                    for i, line in enumerate(lines_ind):
                        if "Industry" in line:
                            # Assuming the website URL is on the next line
                            if i + 1 < len(lines_ind):
                                industry = lines_ind[i + 1]
                                break
                # if dt.get_attribute("innerText") == "Industry":
                #     industry = (
                #         dt.get_attribute("innerText")
                #         + "-"
                #         + dt.find_element_by_xpath("./following-sibling::dd").text
                #     )
                #     industry = industry.split("Industry-")[1]

        except:
            industry = ""
        try:
            dts2 = driver.find_elements_by_xpath("//dl[contains(@class,'overflow-hidden')]")
            
            for dt in dts2:
                if "Company size" in dt.get_attribute("innerText"):
                    inner_text_cz = dt.get_attribute("innerText")
                    lines_cz= inner_text_cz.split('\n')

                    # Loop through the lines to find the website
                    CompanySize = None
                    for i, line in enumerate(lines_cz):
                        if "Company size" in line:
                            # Assuming the website URL is on the next line
                            if i + 1 < len(lines_cz):
                                CompanySize = lines_cz[i + 1]
                                break
            
            # for dt in dts2:
            #     if dt.get_attribute("innerText") == "Company size":
            #         CompanySize = (
            #             dt.get_attribute("innerText")
            #             + "-"
            #             + dt.find_element_by_xpath("./following-sibling::dd").text
            #         )
            #         CompanySize = CompanySize.split("size-")[1]
        except:
            CompanySize = ""

        try:
            dts3 = driver.find_elements_by_xpath("//dl[contains(@class,'overflow-hidden')]")
            
            for dt in dts3:
                if "Headquarters" in dt.get_attribute("innerText"):
                    inner_text_headq = dt.get_attribute("innerText")
                    lines_headq= inner_text_headq.split('\n')

                    # Loop through the lines to find the website
                    Headquarters = None
                    for i, line in enumerate(lines_headq):
                        if "Headquarters" in line:
                            # Assuming the website URL is on the next line
                            if i + 1 < len(lines_headq):
                                Headquarters = lines_headq[i + 1]
                                break
            
            # for dt in dts3:
            #     if dt.get_attribute("innerText") == "Headquarters":
            #         Headquarters = (
            #             dt.get_attribute("innerText")
            #             + "-"
            #             + dt.find_element_by_xpath("./following-sibling::dd").text
            #         )
            #         Headquarters = Headquarters.split("Headquarters-")[1]
        except:
            Headquarters = ""
        try:
            dts4 = driver.find_elements_by_xpath("//dl[contains(@class,'overflow-hidden')]")
            
            for dt in dts4:
                if "Type" in dt.get_attribute("innerText"):
                    inner_text_type = dt.get_attribute("innerText")
                    lines_type= inner_text_type.split('\n')

                    # Loop through the lines to find the website
                    CompType = None
                    for i, line in enumerate(lines_type):
                        if "Type " in line:
                            # print(lines_type)
                            # Assuming the website URL is on the next line
                            if i + 1 < len(lines_type):
                                CompType = lines_type[i + 1]
                                break
            
            # for dt in dts4:
            #     if dt.get_attribute("innerText") == "Type":
            #         CompType = (
            #             dt.get_attribute("innerText")
            #             + "-"
            #             + dt.find_element_by_xpath("./following-sibling::dd").text
            #         )
            #         CompType = CompType.split("-")[1]
        except:
            CompType = ""
        try:
            dts5 = driver.find_elements_by_xpath("//dl[contains(@class,'overflow-hidden')]")
            
            for dt in dts5:
                if "Founded" in dt.get_attribute("innerText"):
                    inner_text_found = dt.get_attribute("innerText")
                    lines_found= inner_text_found.split('\n')

                    # Loop through the lines to find the website
                    Founded = None
                    for i, line in enumerate(lines_found):
                        if "Founded" in line:
                            # Assuming the website URL is on the next line
                            if i + 1 < len(lines_found):
                                Founded = lines_found[i + 1]
                                break
            
            
            # for dt in dts5:
            #     if dt.get_attribute("innerText") == "Founded":
            #         Founded = (
            #             dt.get_attribute("innerText")
            #             + "-"
            #             + dt.find_element_by_xpath("./following-sibling::dd").text
            #         )
            #         Founded = Founded.split("-")[1]
        except:
            Founded = ""
            
            
        try:
            dts6 = driver.find_elements_by_xpath("//dl[contains(@class,'overflow-hidden')]")
            
            for dt in dts6:
                if "Specialties" in dt.get_attribute("innerText"):
                    inner_text_sp = dt.get_attribute("innerText")
                    lines_sp= inner_text_sp.split('\n')

                    # Loop through the lines to find the website
                    Specialties = None
                    for i, line in enumerate(lines_sp):
                        if "Specialties" in line:
                            # Assuming the website URL is on the next line
                            if i + 1 < len(lines_sp):
                                Specialties = lines_sp[i + 1]
                                break
            
            
            # for dt in dts6:
            #     if dt.get_attribute("innerText") == "Specialties":
            #         Specialties = (
            #             dt.get_attribute("innerText")
            #             + "-"
            #             + dt.find_element_by_xpath("./following-sibling::dd").text
            #         )
            #         Specialties = Specialties.split("Specialties-")[1]
        except:
            Specialties = ""
            
            
            
        try:
            dts6 = driver.find_elements_by_xpath("//dl[contains(@class,'overflow-hidden')]")
            
            for dt in dts6:
                if "Phone" in dt.get_attribute("innerText"):
                    inner_text_phone = dt.get_attribute("innerText")
                    lines_phone= inner_text_phone.split('\n')

                    # Loop through the lines to find the website
                    phone = None
                    for i, line in enumerate(lines_phone):
                        if "Phone" in line:
                            # Assuming the phone number is on the same line or the next line
                            if "Phone number is" in line:
                                phone = line.split("Phone number is ")[1]
                            elif i + 1 < len(lines) and "Phone number is" in lines[i + 1]:
                                phone = lines_phone[i + 1].split("Phone number is ")[1]
                            elif i + 1 < len(lines):
                                phone = lines_phone[i + 1]
                            break

            
            
            # for dt in dts6:
            #     if dt.get_attribute("innerText") == "Specialties":
            #         Specialties = (
            #             dt.get_attribute("innerText")
            #             + "-"
            #             + dt.find_element_by_xpath("./following-sibling::dd").text
            #         )
            #         Specialties = Specialties.split("Specialties-")[1]
        except:
            phone = ""
            

        try:
            location = driver.find_element_by_xpath(
                "//p[@class='t-14 t-black--light t-normal break-words']"
            ).text
        except:
            location = ""

        try:
            warn = driver.find_element_by_xpath(
                "//p[@class='t-14 t-black--light mt2']"
            ).text
        except:
            warn = ""
            
        try:
            dts7 = driver.find_elements_by_xpath("//dl[contains(@class,'overflow-hidden')]")
            
            if "Verified" in dt.get_attribute("innerText"):
                # Now we get the corresponding 'dd' after the 'dt' containing "Verified page"
                # Find all 'dt' elements within this 'dl'
                dt_elements = dt.find_elements_by_tag_name("dt")
                for dt_element in dt_elements:
                    if "Verified page" in dt_element.get_attribute("innerText"):
                        # Get the next sibling 'dd' element
                        dd_element = dt_element.find_element_by_xpath("following-sibling::dd[1]")
                        verified = dd_element.get_attribute("innerText")
                        break

        except:
            verified = ""
            
        ppl_link=link.replace("/about/","")
        driver.get(ppl_link+'/people')
        time.sleep(random.uniform(10,15))
        
        try:
            WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.XPATH, "//div[@class='org-grid__content-height-enforcer']")))   
        except:
            print("no tables to see number of ppl")
            pass
        
        # time.sleep(3)
        try:
            try:
                numberOfEmployees = driver.find_element_by_xpath("//h2[@class='t-20 t-black t-bold']").text
            except:
                try:
                    numberOfEmployees = driver.find_element_by_xpath("//h2[@class='text-heading-xlarge']").text
                except:
                    numberOfEmployees = driver.find_element_by_xpath("//div[@class='org-people__header-spacing-carousel']").text
            
            if 'alumni' in numberOfEmployees:
                numberOfEmployees = getNumberOfEmployees_old_way(driver)
            else:
                numberOfEmployees = numberOfEmployees.split(" ")[0]
                if ',' in numberOfEmployees:
                    numberOfEmployees = numberOfEmployees.replace(",","")
            
            
            
            
            numberOfEmployees = int(numberOfEmployees)
            # print("numberOfEmployees is:    ",numberOfEmployees)
            if numberOfEmployees ==0:
                numberOfEmployees = getNumberOfEmployees_old_way(driver)
            print("numberOfEmployees is:    ",numberOfEmployees)
        except:
            numberOfEmployees = getNumberOfEmployees_old_way(driver)
            print("numberOfEmployees is:    ",numberOfEmployees)
        #     raise
            # try:
            #     snde_link = driver.current_url
            #     snde_link = snde_link.split("?face")[0]
            #     driver.get(snde_link)
                
            #     driver.find_element_by_xpath("//button[@class='artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view']").click()
            #     driver.find_element_by_xpath("//button[@class='artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view']").click()
                
                    
                
            #     selector = Selector(text=driver.page_source)
            #     all_employees = driver.find_elements_by_xpath("//div[@class='artdeco-card p4 m2 org-people-bar-graph-module__network']//div[@class='org-people-bar-graph-element__percentage-bar-info truncate full-width mt2 mb1 t-14 t-black--light t-normal']")
            #     empl = []
                
            #     for i in all_employees:
            #         i.click()
            #         soup = bs(i)
            #         num = soup.find('div', {'class': 'org-people-bar-graph-element__percentage-bar-info truncate full-width mt2 mb1 t-14 t-black--light t-normal'})
            #         children = num.findChildren("strong" , recursive=False)
            #         for numberOfEmpl in children:
            #             numberOfEmpl = int(numberOfEmpl.text)
                         
                        
                        
            #         empl.append(numberOfEmpl)
            #         numberOfEmployees = sum(empl)
                
            # except:
            #     print("no number of empl")
            #     numberOfEmployees = int(0)
        
        
        
        # if numberOfEmployees == 0:
        #     ppl_link=link.replace("/about/","")
        #     driver.get(ppl_link+'/people/')
        #     time.sleep(4)
        #     try:
        #         driver.find_element_by_xpath("//button[@class='artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view']").click()
        #         driver.find_element_by_xpath("//button[@class='artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view']").click()
                
                    
                
        #         selector = Selector(text=driver.page_source)
        #         all_employees = selector.xpath("//div[@class='artdeco-card p4 m2 org-people-bar-graph-module__network']//div[@class='org-people-bar-graph-element__percentage-bar-info truncate full-width mt2 mb1 t-14 t-black--light t-normal']")
        #         empl = []
                
        #         for i in all_employees.extract():
        #             soup = bs(i)
        #             num = soup.find('div', {'class': 'org-people-bar-graph-element__percentage-bar-info truncate full-width mt2 mb1 t-14 t-black--light t-normal'})
        #             children = num.findChildren("strong" , recursive=False)
        #             for numberOfEmpl in children:
        #                 numberOfEmpl = int(numberOfEmpl.text)
                        
                        
                        
        #             empl.append(numberOfEmpl)
        #             numberOfEmployees = sum(empl)
                    
                    
                   
                        
        
        #     except:
        #         print("no next to get the number")
        #         numberOfEmpl = int(0)
        #         numberOfEmployees = numberOfEmpl

        aboutDict = {"about": []}
        aboutDict["about"].append(
            {
                "Name":Name,
                "updated_Link": updated_Link,
                "Overview": OverView,
                "Website": Website,
                "Industry": industry,
                "Headquarters": Headquarters,
                "CompanySize": CompanySize,
                "CompType": CompType,
                "Founded": Founded,
                "Speciality": Specialties,
                # "Phone":phone,
                "location": location,
                "Warning": warn,
                "date_collected": date_collected,
                "numberOfEmployees": numberOfEmployees,
                "company_logo_link": company_logo_link,
                "verified":verified,
                "error":None,
            }
        )
    else:
        aboutDict = {"about": []}
        aboutDict["about"].append(
            {
                "Name":"",
                "updated_Link": "",
                "Overview": "",
                "Website": "",
                "Industry": "",
                "Headquarters": "",
                "CompanySize": "",
                "CompType": "",
                "Founded": "",
                "Speciality": "",
                # "Phone":"",
                "location": "",
                "Warning": "",
                "date_collected": "",
                "numberOfEmployees": 0,
                "company_logo_link": "",
                "verified":"",
                "error":None,
            }
        )
        return aboutDict
    
    print("aboutDICT: ",aboutDict)
    return aboutDict







def get_numerical_link_missing(driver):
    
    try:
        empl = driver.find_element_by_xpath("//span[@class= 'v-align-middle']").text
        empl = empl.split(" employee")[0]
        if 'all' in empl:
            empl = empl.split("all ")[1]
        try:
            empl= int(empl)
        except:
            empl = int(empl.replace(",",""))
        if empl == "1 ":
                empl  = int(empl)
    except:
        try:
            empl = driver.find_element_by_xpath("//span[@class='link-without-visited-state t-bold t-black--light']").text
            empl = empl.split("employee")[0].split("See ")[1]
            if 'all' in empl:
                empl = empl.split("all ")[1]
                try:
                    empl= int(empl)
                except:
                        empl = int(empl.replace(",",""))
            if empl == "1 ":
                empl  = int(empl)
        except:
            try:
                empl=driver.find_element_by_xpath("//span[@class='org-top-card-secondary-content__see-all t-normal t-black--light link-without-visited-state link-without-hover-state']").text
                empl = empl.split(" employee")[0]
                try:
                    empl= int(empl)
                except:
                        empl = int(empl.replace(",",""))
            except:
             empl=0
    print("numberofEmployees: ", empl)        
    if empl>0:
         
         try:
            peopleclick = driver.find_elements_by_xpath("//div[@class='org-top-card-secondary-content__connections display-flex mt4 mb1']/a")[1]
            pplclick2 = peopleclick.get_attribute("href")
            driver.get(pplclick2)
            time.sleep(random.uniform(4, 9))
        
         except:
            peopleclick = driver.find_element_by_xpath("//div[@class='display-flex mt2 mb1']/a")
            sleep(randint(1,2))

            peopleclick.click()
            
         
         print("clicked on empl")
         sleep(randint(1,2))
         current_company_link = driver.current_url
         sleep(randint(1,3))

        
         try:
             current_company_link = current_company_link.split("%5B%22")[1]
             current_company_link=current_company_link.split("%22%5D")[0]
             
         except:
             try:
                 current_company_link = current_company_link.split("%5B")[1]
                 current_company_link=current_company_link.split("%5D")[0]
             except:
                 current_company_link = current_company_link.split("%5B")[1]
                 current_company_link=current_company_link.split("%5D")[0]
                 
             
         numerical_link = "https://www.linkedin.com/company/"+current_company_link
         
    else:
        numerical_link = ""
         
                         
                 
    return numerical_link
    

def save_numerical(driver, li_id,abouts):
    if abouts == True:
        li_id_abouts = getAbouts(driver, "https://www.linkedin.com/company/"+li_id)
        
    driver.get("https://www.linkedin.com/company/"+li_id)
    document_id = li_id
    
    doc_ref = db.collection(u'entities').document(document_id)

    doc = doc_ref.get()

    if doc.exists:
            document_output=doc.to_dict()  
            try:
                numerical_link_found = document_output['about']['numericLink']
                if numerical_link_found == "":
                    numerical_link_found = get_numerical_link_missing(driver)
                    
                    about = {
                        'about': {'numericLink':numerical_link_found,'updated_Link':li_id},'last_updated':datetime.datetime.utcnow(),'id':document_id
                                    }
                    db.collection(u'entities').document(document_id).set(about,merge=True) 
            
                    
                
            except:
                numerical_link_found = get_numerical_link_missing(driver)
               
                about = {
                    'about': {'numericLink':numerical_link_found,'updated_Link':li_id},'last_updated':datetime.datetime.utcnow(),'id':document_id
                                }
                db.collection(u'entities').document(document_id).set(about,merge=True) 
      
    else:
        numerical_link_found = get_numerical_link_missing(driver)
        
        about = {
            'about': {'numericLink':numerical_link_found,'updated_Link':li_id},'last_updated':datetime.datetime.utcnow(),'id':document_id
                        }
        db.collection(u'entities').document(document_id).set(about,merge=True) 
    
            
                
     
    return numerical_link_found
    
    
# # # # # # # # time_Start = time.asctime()
# driver = login("rroobbiinngghhaazzaall99@gmail.com","roby1234")
# link = "https://www.linkedin.com/company/france-antifouling/"
# answ = getAbouts(driver, link)
# # 