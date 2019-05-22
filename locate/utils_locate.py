from selenium import webdriver
from selenium.webdriver.support.select import Select
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

def find_page(browser, m, d):
    #Service Selection
    button1 = browser.find_element_by_id("案件維護")
    button1.click()
    
    #案件維護 Page
    browser.get("http://10.50.100.119/TFD/CaseMaintain/QueryCase_Select.asp")
    select1 = Select(browser.find_element_by_name("Sys_UpdateDate"))
    select1.select_by_value("8")
    
    
    
    month = browser.find_element_by_xpath("//input[@type='text'][@name='Sys_Moth']")
    month.clear()
    month.send_keys(m)
    month1 = browser.find_element_by_xpath("//input[@type='text'][@name='Sys_Moth1']")
    month1.clear()
    month1.send_keys(m)
    day = browser.find_element_by_xpath("//input[@type='text'][@name='Sys_Day']")
    day.clear()
    day.send_keys(d)
    day1 = browser.find_element_by_xpath("//input[@type='text'][@name='Sys_Day1']")
    day1.clear()
    day1.send_keys(d)
    
    select2 = Select(browser.find_element_by_xpath("//select[@name='havalue']"))
    select2.select_by_value("1")
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
    
    newdata = newdata[~newdata.loc[:,5].str.contains("受理轉報")]
    newdata = newdata[~newdata.loc[:,6].str.contains("捉蛇")]
    newdata = newdata[~newdata.loc[:,6].str.contains("捕蜂")]
    newdata = newdata[newdata.loc[:,8].str.contains("號")]
    
    return newdata

def get_dispatcher(browser, newdata):
    table = browser.find_element_by_name("myForm")
    table_rows = table.find_elements_by_tag_name('tr')
    
    dispatchers = []

    for i in newdata.index:
        table_cols = table_rows[i].find_elements_by_tag_name('td')
        button = table_cols[13].find_element_by_xpath("input[@name='Hist']")
        button.click()
        browser.switch_to.window(browser.window_handles[1])

        sleep(1)
        dispatchers.append(extract(browser, newdata))
        print("Success: "+str(i))

        browser.switch_to.window(browser.window_handles[0])
    
    newdata["派遣員"] = np.array(dispatchers)
    newdata.loc[:,8] = newdata.loc[:,8].map(lambda x: x[:-6])
    newdata["地址"] = newdata.loc[:,8]
    newdata.loc[:,8] = newdata["派遣員"]
    newdata.pop("派遣員")
    
    return browser, newdata

def extract(browser, newdata): 
    
    html = browser.page_source
    tables = pd.read_html(html)
    return tables[0].loc[2,1][:3]


###############################
##      Get Address Data     ##
###############################

def get_browser():
    
    # Get browser
    browser = webdriver.Chrome()
    browser.get("http://www.houseno.tcg.gov.tw/?ccms_cs=1")
    
    # Find search button
    button = browser.find_element_by_id("collapsible_control_3")
    button.click()
    iframes = browser.find_element_by_tag_name("iframe")
    
    # Switch to search table
    browser.switch_to.frame("ifrm_03_ADDRHTR")
    browser.switch_to.frame("frm_new1")
    
    sleep(1)
    
    return browser

def find_address(browser, road="中山北路", section="一", lan="126", l="", num="1", fl="", gg=""):
    
    def func(x):
        find = re.match('(.*鄰)(.*)',x)
        if find != None:
            print(find.group(2))
        return find.group(2)
    
    # Insert address
    address = browser.find_element_by_name("ttrstreet")
    address.clear()
    address.send_keys(road)
    
    sec = Select(browser.find_element_by_name("ttrsection"))
    sec.select_by_value(section)

    lane = browser.find_element_by_name("ttrshi")
    lane.clear()
    lane.send_keys(lan)

    lo = browser.find_element_by_name("ttrlo")
    lo.clear()
    lo.send_keys(l)

    number = browser.find_element_by_name("ttrnum")
    number.clear()
    number.send_keys(num)

    floor = Select(browser.find_element_by_name("ttrfloor"))
    floor.select_by_value(fl)

    g = browser.find_element_by_name("ttrg")
    g.clear()
    g.send_keys(gg)
    
    sleep(1)

    button2 = browser.find_element_by_name("search")
    button2.click()
    
    try:
        browser.switch_to.alert.accept()
        browser.switch_to.parent_frame()
        browser.switch_to.frame("frm_new2")
        back = browser.find_element_by_xpath('//a[@href="javascript:history.back()"]')
        back.click()
        return ["此地址","查無結果"]
    except:
        browser.switch_to.parent_frame()
        browser.switch_to.frame("frm_new2")

        data = pd.read_html(browser.page_source)
        data = data[0]

        end = data[data.loc[:,0].str.contains("本資料僅供參考，不作為其他證明使用")].index.values
        address_info = data.loc[2:end[0]-1,0].reset_index().loc[:,0]
        address_info = address_info.map(lambda x: func(x))
        
        back = browser.find_element_by_xpath('//a[@href="javascript:history.back()"]')
        back.click()
        sleep(1)
        return address_info 

def handle_data(file):
    data = pd.read_excel(file)
    data["路"] = data["地址"].str.extract(r'.*區(.*?)\d+')
    data["段"] = data["地址"].str.extract(r'.*路(.*?)段\d+')
    data["巷"] = data["地址"].str.extract(r'.*[段路街](.*?)巷\d+')
    data["弄"] = data["地址"].str.extract(r'.*巷(.*?)弄\d+')
    data["號"] = data["地址"].str.extract(r'.*[路段巷弄街](.*?)號')
    data["號"] = data["號"].map(lambda x: x.split("-")[0])
    data["樓"] = data["地址"].str.extract(r'.*?(\d+)樓')
    sec_dic = {np.nan:'', '1':"一", '2':"二", '3':"三", '4':"四", '5':"五", '6':"六", '7':"七", '8':"八", '9':"九", '10':"十"}
    floor_dic = {np.nan:'', '1':"一", '2':"二", '3':"三", '4':"四", '5':"五", '6':"六", '7':"七", '8':"八", '9':"九", '10':"十",
                 '11':"十一", '12':"十二", '13':"十三", '14':"十四", '15':"十五", '16':"十六", '17':"十七", '18':"十八", '19':"十九", '20':"二十",
                 '21':"二十一", '22':"二十二", '23':"二十三", '24':"二十四", '25':"二十五", '26':"二十六", '27':"二十七", '28':"二十八", '29':"二十九", '30':"三十",
                 '31':"三十一", '32':"三十二", '33':"三十三", '34':"三十四", '35':"三十五", '36':"三十六", '37':"三十七", '38':"三十八", '39':"三十九", '40':"四十",
                 '41':"四十一", '42':"四十二", '43':"四十三", '44':"四十四", '45':"四十五", '46':"四十六", '47':"四十七", '48':"四十八", '49':"四十九", '50':"五十",
                 '51':"五十一", '52':"五十二", '53':"五十三", '54':"五十四", '55':"五十五", '56':"五十六", '57':"五十七", '58':"五十八", '59':"五十九", '60':"六十",
                 '61':"六十一", '62':"六十二", '63':"六十三", '64':"六十四", '65':"六十五", '66':"六十六", '67':"六十七", '68':"六十八", '69':"六十九", '70':"七十",
                 '71':"七十一", '72':"七十二", '73':"七十三", '74':"七十四", '75':"七十五", '76':"七十六", '77':"七十七", '78':"七十八", '79':"七十九", '80':"八十",
                 '81':"八十一", '82':"八十二", '83':"八十三", '84':"八十四", '85':"八十五", '86':"八十六", '87':"八十七", '88':"八十八", '89':"八十九", '90':"九十",
                 '91':"九十一", '92':"九十二", '93':"九十三", '94':"九十四", '95':"九十五", '96':"九十六", '97':"九十七", '98':"九十八", '99':"九十九", '100':"一00"}
    data["段"] = data["段"].map(sec_dic)
    data["樓"] = data["樓"].map(floor_dic)
    data = data.fillna("")
    
    return data
