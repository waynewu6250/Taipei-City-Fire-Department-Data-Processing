from selenium import webdriver
from selenium.webdriver.support.select import Select
import pandas as pd
import numpy as np
import os
import re
import random
import chardet
from time import sleep
from utils_week import *
basename = "D:\\Users\TFD\Downloads"

def run_1(yr = 2019, mth = 5, date = 1, num = 4, past = 3):
    def run():
        browser = open_browser()
        browser = login(browser)
        button1 = browser.find_element_by_id("案件資料分析")
        button1.click()
        return browser

    browser = run()

    browser.get("http://10.50.100.119/TFD/CaseMaintain/Analysis/FireAIDAnalyze_Select_1.asp")

    for i in range(date,date+num):

        year = browser.find_element_by_xpath("//input[@type='text'][@name='Sys_Yearf']")
        year.clear()
        year.send_keys(str(yr))
        month = browser.find_element_by_xpath("//input[@type='text'][@name='Sys_Monthf']")
        month.clear()
        month.send_keys(str(mth))
        day = browser.find_element_by_xpath("//input[@type='text'][@name='Sys_Dayf']")
        day.clear()
        day.send_keys(str(i))

        select1 = Select(browser.find_element_by_name("Analyzef"))
        select1.select_by_value("0")

        button1 = browser.find_element_by_xpath("//input[@type='button'][@name='btnExcel']")
        button1.click()
        sleep(1)
        browser.back()


    # Change file names
    files = [basename+"\\"+i for i in os.listdir(basename) if i.find("火災與救護分析統計報告總表") != -1]
    files.sort(key = lambda fn: os.path.getmtime(fn))
    for i,name in enumerate(files):
        newname = basename+'\\'+str(i+1+past)+'.xls'
        os.rename(name,newname)

        
def run_2(yr = 2019, mth = 5, date = 1, num = 4, past = 3):
    def run():
        browser = open_browser()
        browser = login(browser)
        button1 = browser.find_element_by_id("案件資料分析")
        button1.click()
        return browser
    
    browser = run()

    browser.get("http://10.50.100.119/TFD/CaseMaintain/Analysis/CaseAnalyze_Select_1.asp")


    for i in range(date,date+num):

        select1 = Select(browser.find_element_by_name("Sys_UpdateDate"))
        select1.select_by_value("8")

        year = browser.find_element_by_xpath("//input[@type='text'][@name='Sys_Yearf']")
        year.clear()
        year.send_keys(str(yr))
        month = browser.find_element_by_xpath("//input[@type='text'][@name='Sys_Mothf']")
        month.clear()
        month.send_keys(str(mth))
        day = browser.find_element_by_xpath("//input[@type='text'][@name='Sys_Dayf']")
        day.clear()
        day.send_keys(str(i))
        year1 = browser.find_element_by_xpath("//input[@type='text'][@name='Sys_Year1f']")
        year1.clear()
        year1.send_keys(str(yr))
        month1 = browser.find_element_by_xpath("//input[@type='text'][@name='Sys_Moth1f']")
        month1.clear()
        month1.send_keys(str(mth))
        day1 = browser.find_element_by_xpath("//input[@type='text'][@name='Sys_Day1f']")
        day1.clear()
        day1.send_keys(str(i))

        select2 = Select(browser.find_element_by_name("Analyzef1"))
        select2.select_by_value("520")
        select3 = Select(browser.find_element_by_name("Analyzef2"))
        select3.select_by_value("18")

        button1 = browser.find_element_by_xpath("//input[@type='button'][@name='b1']")
        button1.click()

        button2 = browser.find_element_by_xpath("//input[@type='button'][@name='GetList']")
        button2.click()
        sleep(2)
        browser.back()


    # Change file names
    files = [basename+"\\"+i for i in os.listdir(basename) if i.find("案件統計分析") != -1]
    files.sort(key = lambda fn: os.path.getmtime(fn))
    for i,name in enumerate(files):
        newname = basename+'\\'+str(i+1+past)+'.xls'
        os.rename(name,newname)
    
