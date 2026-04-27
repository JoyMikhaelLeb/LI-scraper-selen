#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 16:12:48 2022

@author: joy
"""

from selenium.webdriver.support import expected_conditions as EC
import random
from webdriver_manager.chrome import ChromeDriverManager
import datetime
#from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver

import time

from selenium.webdriver.common.keys import Keys

from random import randint

from selenium.common.exceptions import NoSuchElementException,TimeoutException

from selenium.webdriver.common.action_chains import ActionChains
from scrapy.selector import Selector
#
from bs4 import BeautifulSoup as bs

# import pandas as pd

from bs4 import BeautifulSoup, Tag, NavigableString
import re


def check_exists_by_xpath(driver, xpath):

    try:

        driver.find_element_by_xpath(xpath)

    except NoSuchElementException:

        return True

    return False


        
def login(username, password,headless=False):
    url = "https://www.linkedin.com/login"
    chrome_options = webdriver.ChromeOptions()

    if not headless:
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--incognito")
        
        chrome_options.add_argument("--start-maximized")
        # print("removed incognito")
    else:
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

    try:
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)

        if headless:
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    except :
        print(f"Errof")
        raise

    if headless:
        print("Browser ready in headless mode")
    
    driver.get(url)

    driver.find_element_by_id("username").send_keys(username)

    driver.find_element_by_id("password").send_keys(password)
    
    try:
        label = driver.find_element(By.CSS_SELECTOR, "label[for='rememberMeOptIn-checkbox']")
        label.click()
        print("unchecked-rememberme")
    except:
        pass
    
    driver.find_element_by_xpath("//div[contains(@class,'login__form_action_container')]//*[contains(@aria-label, 'Sign in')]").click()
    time.sleep(2 + randint(1, 3))
    
    current_url = driver.current_url
    
    if 'linkedin.com/checkpoint/challenge/' in current_url:
        
        
        elements = driver.find_elements_by_xpath("//button[normalize-space(text())='Agree to comply']")
        if len(elements) > 0:
            print("Element found! Clicking it...")
            elements[0].click()
            time.sleep(2 + randint(1, 3))
        else:
            print("Element not found. Skipping...")
            print("Verification required. Waiting for code...")
            driver.find_element_by_xpath("//button[@class='btn__resend_link']").click()
            # verification_code = wait_for_verification_code(username)
            # if verification_code!="":
            #     try:
            #         verification_input = driver.find_element_by_id("input__phone_verification_pin")
            #         verification_input.send_keys(verification_code)
            #         time.sleep(1)
            #         driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Submit code')]").click()
            #         print("Verification code submitted.")
            #         time.sleep(5)
            #     except:
            #         try:
            #             wait = WebDriverWait(driver, 15)

            #             verification_input = driver.find_element_by_xpath("//input[@class='form__input--text input_verification_code']")
            #             verification_input.send_keys(verification_code)
            #             recovery_input = wait.until(
            #                 EC.visibility_of_element_located(
            #                     (By.XPATH, "//form[@id='two-step-challenge-recovery-code']//input[@name='pin']")
            #                 )
            #             )
            #             recovery_input.send_keys(verification_code)
                        
            #             submit_button = wait.until(
            #                 EC.element_to_be_clickable(
            #                     (By.XPATH, "//form[@id='two-step-challenge-recovery-code']//button[@type='submit']")
            #                 )
            #             )
                        
            #             submit_button.click()


            #             print("Verification code submitted.")
            #         except Exception as e:
            #             print(f"Error entering verification code: {e}")
            #             driver.quit()
            #             return None
            # else:
            #     print("No verification code received. Exiting.")
            #     driver.quit()
            #     return None
        
    return driver


def moveToElement(driver, target_xpath):
    
    try:
        target = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
        ActionChains(driver).move_to_element(target).perform()
        return True
    except TimeoutException:
        return False
    
def get_numberOFEmployees_old_way(driver):
    
    try:
        numberOfEmployees = driver.find_element_by_xpath(
            "//span[@class= 'v-align-middle']"
        )
        numberOfEmployees = numberOfEmployees.text
        numberOfEmployees = numberOfEmployees.split("See ")[1].split(" employee")[0]
        if "all" in numberOfEmployees:
            numberOfEmployees = numberOfEmployees.split("all ")[1]
        try:
            numberOfEmployees = int(numberOfEmployees.replace(",", ""))

        except:
            numberOfEmployees = int(numberOfEmployees)

    except:
        try:
            numberOfEmployees = driver.find_element_by_xpath(
                "//span[@class='link-without-visited-state t-bold t-black--light']"
            )
            numberOfEmployees = numberOfEmployees.text
            numberOfEmployees = numberOfEmployees.split("See ")[1].split(
                " employee"
            )[0]
            if "all" in numberOfEmployees:
                numberOfEmployees = numberOfEmployees.split("all ")[1]
            try:
                numberOfEmployees = int(numberOfEmployees.replace(",", ""))

            except:
                numberOfEmployees = int(numberOfEmployees)

        except:
                try:
                    numberOfEmployees = driver.find_element_by_xpath(
                        "//span[@class='org-top-card-secondary-content__see-all t-normal t-black--light link-without-visited-state link-without-hover-state']"
                        ).text
                    if 'employee' in numberOfEmployees:
                        numberOfEmployees = numberOfEmployees.split(" employee")[0]
                    if 'all' in numberOfEmployees:
                        numberOfEmployees = numberOfEmployees.split("all ")[1]
                    
                    try:
                        numberOfEmployees = int(numberOfEmployees.replace(",",""))

                    except:
                        numberOfEmployees = int(numberOfEmployees)


                except:
                    numberOfEmployees = "0"
                    numberOfEmployees = int(numberOfEmployees)
    return numberOfEmployees


# def get_25_months_employees__old(driver,li_id):
#     if moveToElement(driver,"//g[@class='scope']"):
            
#             print("no page")
#             insightsDict = {"insights":[]}
            
        
#             return insightsDict
        
#     if "linkedin.com/" in li_id:
#         link = li_id + '/insights/'
#         driver.get(link)
#         time.sleep(random.uniform(3, 10))
#         updated_Link = driver.current_url
#         if (
#             "/checkpoint/challenges" in updated_Link
#             or "login?session_redirect" in updated_Link
#             or "authwall?trk" in updated_Link
#             or updated_Link == "https://www.linkedin.com/"
#         ):
#             return "security_check"
#     if updated_Link == "https://www.linkedin.com/404/":
#             insightsDict = {"insights":[]}
#             return insightsDict
#     try:
#             smtg_wrong = driver.find_element_by_xpath("//h2[@class='artdeco-empty-state__headline artdeco-empty-state__headline--mercado-error-server-small artdeco-empty-state__headline--mercado-spots-small']")
#             smtg_wrong = smtg_wrong.text
#             if 'Something went wrong' in smtg_wrong:
#                 insightsDict = {"insights":[]}
#                 return insightsDict
                
#     except:
#         pass
        
        
    
    
    
#     try:
#         if moveToElement(driver,"//*[contains(text(), 'Oops!')]")==True:
#             insightsDict = {"insights":[]}
            
#             return insightsDict  
        
#     except:
#         pass
    
#     try:
#         if moveToElement(driver,"//*[contains(text(), 'Page not found')]")==True:
#             insightsDict = {"insights":[]}
            
        
#             return insightsDict  
        
#     except:
#         pass
        
    
#     try:
#         if moveToElement(driver,"//*[contains(text(), 'HTTP Error 400. The request URL is invalid.')]")==True:
#                 insightsDict = {"insights":[]}
                
        
#                 return insightsDict            
#     except:
#         pass
    
#     insights = []
#     insightsDict = {"insights":[]}
    
#     paths = driver.find_elements_by_xpath("//table[@id='org-insight__a11y-table']//tr")
#     for elemn in paths[1:]:
#         # print(elemn)
#         infos = elemn.get_attribute("innerText")
#         month = infos.split("\t")[0]
#         empl = infos.split("\t")[1]
#         if ',' in empl:
#             empl = empl.replace(",","")
#             empl = int(empl)
#         else:
#             empl = int(empl)
            
            
#         insights.append([month,empl])
#         insightsDict['insights'].append({month:empl})

#     if len(insightsDict['insights'])==0:
        
#         driver.get(link)
#         time.sleep(random.uniform(3, 10))
#         try:
#             check_path = driver.find_element_by_xpath("//div[@class='org-premium-container__header']//h2[@class='org-premium-container__title t-20 t-black t-bold' and text()='Total employee count']")
#             insights.append([month,empl])
#         except:
#             print("there are no insights")
        
#     return insightsDict

def get_25_months_employees(driver,li_id):
    
    
    date_collected = datetime.date.today().strftime("%d-%b-%y")
    updated_Link = driver.current_url
    if moveToElement(driver,"//g[@class='scope']"):
            
            print("no page")
            result_dict = {
            'date_collected': date_collected,
            'updated_link': updated_Link.replace("/insights",""),
            'number_of_employees_history': [],
            'note':'noINSIGHTS'
        }
    # return result_dict
            
    #         result_dict = insightsDict
                
        
            return result_dict         
        
    if "linkedin.com/" in li_id:
        if '?' in li_id:
            li_id = li_id.split("?")[0]
        link = li_id + '/insights/'
        driver.get(link)
        time.sleep(random.uniform(3, 10))
        updated_Link = driver.current_url
        if (
            "/checkpoint/challenges" in updated_Link
            or "login?session_redirect" in updated_Link
            or "authwall?trk" in updated_Link
            or updated_Link == "https://www.linkedin.com/"
        ):
            return "security_check"
    if updated_Link == "https://www.linkedin.com/404/":
            result_dict = {
            'date_collected': date_collected,
            'updated_link': updated_Link.replace("/insights",""),
            'number_of_employees_history': [],
            'note':'noINSIGHTS'
        }
                
        
            return result_dict         
            
    try:
            smtg_wrong = driver.find_element_by_xpath("//h2[@class='artdeco-empty-state__headline artdeco-empty-state__headline--mercado-error-server-small artdeco-empty-state__headline--mercado-spots-small']")
            smtg_wrong = smtg_wrong.text
            if 'Something went wrong' in smtg_wrong:
                result_dict = {
            'date_collected': date_collected,
            'updated_link': updated_Link.replace("/insights",""),
            'number_of_employees_history': [],
            'note':'noINSIGHTS'
        }
                
        
                return result_dict         
                
                
    except:
        pass
        
        
    
    
    
    try:
        if moveToElement(driver,"//*[contains(text(), 'Oops!')]")==True:
            result_dict = {
            'date_collected': date_collected,
            'updated_link': updated_Link.replace("/insights",""),
            'number_of_employees_history': [],
            'note':'noINSIGHTS'
        }
                
        
            return result_dict         
        
    except:
        pass
    
    try:
        if moveToElement(driver,"//*[contains(text(), 'Page not found')]")==True:
            # insightsDict = {"insights":[]}
            # result_dict = insightsDict
            result_dict = {
            'date_collected': date_collected,
            'updated_link': updated_Link.replace("/insights",""),
            'number_of_employees_history': [],
            'note':'noINSIGHTS'
        }
        
            return result_dict         
        
    except:
        pass
        
    
    try:
        if moveToElement(driver,"//*[contains(text(), 'HTTP Error 400. The request URL is invalid.')]")==True:
                result_dict = {
            'date_collected': date_collected,
            'updated_link': updated_Link.replace("/insights",""),
            'number_of_employees_history': [],
            'note':'noINSIGHTS'
        }
                
        
                return result_dict            
    except:
        pass
    # insightsDict_to_return = {"Insights":[]}
    date_collected = datetime.date.today().strftime("%d-%b-%y")
    if moveToElement(driver, "//h2[contains(., 'Total employee count')]") == False:
        print("there is no insight... Let's try again loading the page")
        driver.refresh()
        time.sleep(random.uniform(5, 10))
        driver.get(link)
        time.sleep(random.uniform(5, 10))
        if moveToElement(driver,"//h2[contains(., 'Total employee count')]")==False:
            if moveToElement(driver, "//a[contains(@href, '/insights')]")==True :
                print("no insights after refreshing, we will stop and return the dict")
                result_dict = {
            'date_collected': date_collected,
            'updated_link': updated_Link.replace("/insights",""),
            'number_of_employees_history': [],
            'note':'noINSIGHTS'
        }
    
                return result_dict
        else:
            print("something is wrong")
            result_dict = {
            'date_collected': date_collected,
            'updated_link': updated_Link.replace("/insights",""),
            'number_of_employees_history': [],
            'note':'noINSIGHTS'
        }
            
            return result_dict         
    
    
    insights = []
    insightsDict_to_return = {"Insights":[]}
    
    
    count = 0 
    while count <5 :
        try:
            # time.sleep(randint(1, 3))
#                t = "//*[name()='svg']//*[name()='g' and contains(@class,'highcharts-markers highcharts-series-0 highcharts-area-series highcharts-tracker')]/*[name()='path']"   
            t = "//*[name()='svg']//*[name()='g' and contains(@class,'highcharts-markers highcharts-series-0 highcharts-area-series highcharts-color-0 highcharts-tracker')]/*[name()='path']"

            test = driver.find_elements_by_xpath(t)
            results = []
            for el in test:
                hover = ActionChains(driver).move_to_element(el)
                hover.perform()
                time.sleep(0.1)
#                    date = self.driver.find_elements_by_css_selector(".highcharts-color-undefined > span:nth-child(1)")
                date = driver.find_elements_by_css_selector(".highcharts-color-0 > span:nth-child(1)")

                # time.sleep(randint(1, 3))
                results.append(date[0].text)
            break
        except :
            print("Exception thrown, retrying:", count+1)
            count+=1
    
#     t = "//*[name()='svg']//*[name()='g' and contains(@class,'highcharts-markers highcharts-series-0 highcharts-area-series highcharts-color-0 highcharts-tracker')]/*[name()='path']"
    
#     test = driver.find_elements_by_xpath(t)
    

#     results = []
    
#     for el in test:
#         hover = ActionChains(driver).move_to_element(el)
#         hover.perform()
#         time.sleep(0.3)
        
        
# #                    date = self.driver.find_elements_by_css_selector(".highcharts-color-undefined > span:nth-child(1)")
#         date = driver.find_elements_by_css_selector(".highcharts-color-0 > span:nth-child(1)")
#         print(date)
#         # time.sleep(randint(1, 3))
#         results.append(date[0].text)
        
    for one_rst in results:
        
        month = one_rst.split("\n")[0]
        empl =one_rst.split("\n")[1].split("employee")[0]
        if ',' in empl:
            nbr_of_empl = empl.replace(",","")
            nbre_of_empl = int(nbr_of_empl)
        else:
            nbre_of_empl = int(empl)
        date_collected = datetime.date.today().strftime("%d-%b-%y")
        insights.append([month,nbre_of_empl])
        insightsDict_to_return['Insights'].append({month:nbre_of_empl})


    
    # paths = driver.find_elements_by_xpath("//table[@id='org-insight__a11y-table']//tr")
    # for elemn in paths[1:]:
    #     # print(elemn)
    #     infos = elemn.get_attribute("innerText")
    #     month = infos.split("\t")[0]
    #     empl = infos.split("\t")[1]
    #     if ',' in empl:
    #         empl = empl.replace(",","")
    #         empl = int(empl)
    #     else:
    #         empl = int(empl)
            
    #     # date_collected = datetime.date.today().strftime("%d-%b-%y")
    #     insights.append([month,empl])
    #     insightsDict_to_return['Insights'].append({month:empl})
    
        
        
        
    date_collected = datetime.date.today().strftime("%d-%b-%y")
    insights_to_return =[date_collected, insightsDict_to_return['Insights']]
   
    date_collected_to_return, number_of_employees_history = insights_to_return

    result_dict = {
        'date_collected': date_collected,
        'updated_link': updated_Link.replace("/insights",""),
        'number_of_employees_history': number_of_employees_history,
        'note':'cool'
    }
    return result_dict


# import datetime

# PeopleDetails = pd.DataFrame(columns=['linkedin_url','Date','Number_of_employees'])

# driver = login("rroobbiinngghhaazzaall99@gmail.com","roby1234")
# li_id = "https://www.linkedin.com/company/anthropic/"
# # df1 = pd.read_csv("/home/joy/Downloads/todeletelaterwhendone/lefts/left0.csv")
# # # df1 = df1.replace(np.nan, '', regex=True)

# # # # Initialize an empty list to hold the data
# # data = []

# # for ind, li_id in enumerate(df1.linkedin):
# #     print(ind)
# #     print(li_id)
    
# #     ress = get_25_months_employees__old(driver, li_id)
# #     values_of_work = ress['insights']
    
# #     for ppl in values_of_work:
# #         print(list(ppl))
# #         for k, v in ppl.items():
# #             print(k, v)
# #             new_row = {'linkedin_url': li_id, 'Date': k, 'Number_of_employees': v}
# #             data.append(new_row)

# # # Create a new DataFrame from the data
# # new_df = pd.DataFrame(data)

# # # Concatenate the new DataFrame with PeopleDetails
# # PeopleDetails = pd.concat([PeopleDetails, new_df], ignore_index=True)


# # PeopleDetails.to_csv("/home/joy/Downloads/todeletelaterwhendone/lefts/left0---0.csv",index=False)
# # df_left=df1.iloc[ind:]
# # df_left.to_csv("/home/joy/Downloads/todeletelaterwhendone/lefts/lefts0-0.csv",index=False)
# # # li_id='https://www.linkedin.com/company/airmo/'
# new_insights = get_25_months_employees(driver, li_id)
# values_of_work = ress['insights']
# # # # str(list(ppl)).replace("['","").replace("']","")
# # PeopleDetails = pd.DataFrame(columns=['Linkedin_ID', 'Date', 'Number_of_employees', 'date_collected'])
# rows = []

# for ppl in values_of_work:
#     for k, v in ppl.items():
#         new_row = {'Linkedin_ID': li_id, 'Date': k, 'Number_of_employees': v, 'date_collected': datetime.date.today().strftime("%d-%b-%y")}
#         rows.append(new_row)

# PeopleDetails = pd.DataFrame(rows)

# # for ppl in values_of_work:
# #     for k, v in ppl.items():
# #         new_row = {'Linkedin_ID': li_id, 'Date': k, 'Number_of_employees': v, 'date_collected': datetime.date.today().strftime("%d-%b-%y")}
# #         PeopleDetails = PeopleDetails.append(new_row, ignore_index=True)

# # Save DataFrame to CSV
# PeopleDetails.to_csv('airmo.csv', index=False)


# # # # # df1 = pd.DataFrame(values_of_work)





# # PeopleDetails.to_csv("khealthinc-result.csv",index=False)
