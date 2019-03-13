from selenium import webdriver
import pandas as pd
import numpy as np
import re
import random
import chardet
from time import sleep

###############################
#Find the table from browser###
###############################

def open_browser():
    #Open the browser and redirect to home page
    browser = webdriver.Chrome()
    browser.get("http://10.50.100.119/TFD/TFD_Login.asp")
    return browser

def login(browser):
    #Home Page
    account = browser.find_element_by_name("MemberID")
    account.send_keys("a2715730205")
    password =  browser.find_element_by_name("MemberPW")
    password.send_keys("V121163994")
    login_button = browser.find_element_by_name("b1")
    login_button.click()
    return browser

def find_page(browser):
    #Service Selection
    button1 = browser.find_element_by_id("案件維護")
    button1.click()
    
    #案件維護 Page
    browser.get("http://10.50.100.119/TFD/CaseMaintain/QueryCase_Select.asp")
    from selenium.webdriver.support.select import Select
    select1 = Select(browser.find_element_by_name("Sys_UpdateDate"))
    select1.select_by_value("3")
    select2 = Select(browser.find_element_by_xpath("//select[@name='Case_Type']"))
    select2.select_by_value("520")
    button2 = browser.find_element_by_name("select")
    button2.click()
    
    return browser

###############################
#Data Processing with Pandas###
###############################

def read_data(browser):
    
    #Read 案件維護 html
    data = pd.read_html(browser.page_source)
    
    for i in range(len(data)):
        if data[i].iloc[0,0] == "案件列表":
            here = data[i]
            break

    newdata = here.iloc[2:,1:9].dropna(axis=0, how='all')
    newdata = newdata[::-1]
    newdata.pop(2)
    newdata.pop(4)
    newdata.pop(5)
    newdata.pop(6)

    newdata = newdata.reset_index(drop=True)
    
    return newdata

def insert_all_data(browser, newdata):
    table = browser.find_element_by_name("myForm")
    table_rows = table.find_elements_by_tag_name('tr')
    numbers = []

    for i in range(len(newdata)+2,2,-1):
        table_cols = table_rows[i].find_elements_by_tag_name('td')
        button = table_cols[13].find_element_by_xpath("input[@name='Hist']")
        button.click()
        browser.switch_to.window(browser.window_handles[1])

        sleep(1)
        cur = (len(newdata)-i+2)*3
        number = extract(browser)
        numbers.append(number)
        print("Success: "+str(i))

        browser.switch_to.window(browser.window_handles[0])
    
    return browser, newdata, numbers

def extract(browser): 
    
    html = browser.page_source
    tables = pd.read_html(html)
    return tables[0].iloc[2,5]


