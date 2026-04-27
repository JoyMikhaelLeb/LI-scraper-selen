#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 12:15:03 2024

@author: joy
"""

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
import pandas as pd
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

def getNumerical(driver, link):
    # try:
    #     if moveToElement(driver,"//*[contains(text(), ' do a quick security check')]"):
    #         print("Security Check is needed")
    #     return "sec_check"
    # except:
    #     pass

    link = link 

    if "linkedin.com/" not in link:
        aboutDict = {"about": []}
        aboutDict["about"].append(
            {
                
                "updated_Link": "",
               
                "date_collected": "",
                "numberOfEmployees": 0,
               
                "error":None,
            }
        )
        return aboutDict

    if "linkedin.com/" in link:
        try:
            driver.get(link)
            # time.sleep(0.25)
        except TimeoutException:
            print("Here's the timeout in experience. Refreshing...")
            driver.refresh()
            time.sleep(random.uniform(5, 10))
            driver.get(link)
            time.sleep(random.uniform(5, 10))
        # 
        # time.sleep(random.uniform(1, 3))
        try:
            if moveToElement(
                driver,
                "//*[contains(text(), 'Uh oh, we can’t seem to find the page you’re looking for')]",
            ):
                aboutDict = {"about": []}
                aboutDict["about"].append(
                    {
                       
                        "updated_Link": link,
                        
                        "date_collected": "",
                       
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
                   
                    "updated_Link": link,
                   
                    "date_collected": "",
                   
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
                   
                    "updated_Link": link,
                   
                    "date_collected": "",
                   
                    "error":"page_doesnt_exist",
                    
                }
            )
            # aboutDict["about"][0]['error'] = "page_doesnt_exist"
            return aboutDict
        
        if updated_Link == "https://www.linkedin.com/company/unavailable/":
            print("PAGE UNAVAILABLE")
            aboutDict = {"about": []}
            aboutDict["about"].append(
                {
                   
                    "updated_Link": link,
                  
                    "date_collected": "",
                   
                    "error":"page_doesnt_exist",
                    
                }
            )
            # aboutDict["about"][0]['error'] = "page_doesnt_exist"
            return aboutDict
        
        
        try:
            smtg_wrong = driver.find_element_by_xpath("//h2[@class='artdeco-empty-state__headline artdeco-empty-state__headline--mercado-error-server-small artdeco-empty-state__headline--mercado-spots-small']")
            smtg_wrong = smtg_wrong.text
            if 'Something went wrong' in smtg_wrong:
                aboutDict = {"about": []}
                aboutDict["about"].append(
                    {
                      
                        "updated_Link": link,
                       
                        "date_collected": "",
                      
                        "error":"page_doesnt_exist",
                        
                    }
            )
            # aboutDict["about"][0]['error'] = "page_doesnt_exist"
            return aboutDict
        except:
            pass
        
      
        date_collected = ""
        try:
            date_collected = datetime.date.today().strftime("%d-%b-%y")
        except Exception as e:
            date_collected = ""
            print(e)

        # time.sleep(randint(1, 3))

      

        aboutDict = {"about": []}
        aboutDict["about"].append(
            {
                
                "updated_Link": updated_Link,
                
                "date_collected": date_collected,
               
                "error":None,
            }
        )
    else:
        aboutDict = {"about": []}
        aboutDict["about"].append(
            {
                
                "updated_Link": "",
               
                "date_collected": "",
                
                "error":None,
            }
        )
        return aboutDict
    
    print("aboutDICT: ",aboutDict)
    return aboutDict



# driver = login("luciekhodeir@gmail.com","lucyy76@")
# df = pd.read_csv("/home/joy/Documents/numerical_fast/queue_num_1612-0.csv")

# for index, row in df.iterrows():
#     # break
#     target = row['target']
#     link = f"https://www.linkedin.com/company/{target}"
#     print(f"Index: {index}")
#     # break
#     result = getNumerical(driver, link)  # Call the pre-existing function
    
#     aboutDICT = result  # Assuming result is a dictionary like shown
        
#         # Extract and clean 'doc_id'
#     try:
#         doc_id = aboutDICT['about'][0]['updated_Link'].split("/company/")[1].replace("/", "")
#     except:
#         try:
#             doc_id = aboutDICT['about'][0]['updated_Link'].split("/school/")[1].replace("/", "")
#         except:
#             doc_id = aboutDICT['about'][0]['updated_Link'].split("/showcase/")[1].replace("/", "")
    
#     firestore_data = {
#             "about": {
#                 "date_collected": aboutDICT['about'][0]['date_collected'],
#                 "error": None,
#                 "numericLink": link,
#                 "updated_Link": aboutDICT['about'][0]['updated_Link']
#             },
#             "id":doc_id,
#             "parallel_number":randint(1, 10),
#             "last_updated": datetime.datetime.utcnow()
#         }
    
#     db.collection("entities").document(doc_id).set(firestore_data,merge=True)
#     print(f"saved,  {doc_id}, to FS")
    
            
        
#     df_left=df.iloc[index:]
#     df_left.to_csv("/home/joy/Documents/numerical_fast/queue_num_1612-0.csv", index=False)

