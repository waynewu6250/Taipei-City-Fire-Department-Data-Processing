from selenium import webdriver
import pandas as pd
import numpy as np
import re
import random
import chardet
from time import sleep

def open_browser():
    #Open the browser and redirect to home page
    browser = webdriver.Chrome()
    browser.get("http://10.50.100.119/TFD/xxxxxxxxx.asp")
    return browser

def login(browser):
    #Home Page
    account = browser.find_element_by_name("MemberID")
    account.send_keys("xxxxxxxxxxxx")
    password =  browser.find_element_by_name("MemberPW")
    password.send_keys("xxxxxxxxxxxx")
    login_button = browser.find_element_by_name("b1")
    login_button.click()
    return browser

def find_page(browser, number):
    
    #案件維護 Page
    browser.get("http://10.50.100.119/TFD/CaseMaintain/QueryCase_Select.asp")
    query = browser.find_element_by_xpath("//input[@type='text'][@name='QueryCaseID']")
    query.clear()
    query.send_keys(number)

    button2 = browser.find_element_by_name("select")
    button2.click()
    
    return browser

def time_conversion(date):
    time = list(map(int, date.split(":")))
    return time[0]*3600+time[1]*60+time[2]

def extract(browser): 
    
    html = browser.page_source
    tables = pd.read_html(html)
    
    for i in range(len(tables[0])):
        if tables[0].iloc[i,0] == "指揮官呼號":
            table3 = tables[0].iloc[i+1:-1,:3]
            break
    
    #Get Table3
    table3["hour"] = table3.iloc[:,1].str.extract(r'.*日(.*)時.*')
    table3["minute"] = table3.iloc[:,1].str.extract(r'.*時(.*)分.*')
    table3["second"] = table3.iloc[:,1].str.extract(r'.*分(.*)秒.*')
    
    time = ""
    if table3.iloc[:,2].str.contains("", na=False).any() == True:
        out = table3.loc[table3.iloc[:,2].str.contains("車機狀態", na=False)]
        time = "%02d:%02d:%02d" % (int(out.iloc[0,3]),int(out.iloc[0,4]),int(out.iloc[0,5]))
    
    return time






