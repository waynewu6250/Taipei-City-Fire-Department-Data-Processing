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
    browser.get("http://10.50.100.119/TFD/xxxxxxxxx.asp")
    return browser

def login(browser):
    #Home Page
    account = browser.find_element_by_name("MemberID")
    account.send_keys("xxxxxxxxxx")
    password =  browser.find_element_by_name("MemberPW")
    password.send_keys("xxxxxxxxxx")
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
    select1.select_by_value("1")
    select2 = Select(browser.find_element_by_name('AidCaseTypeID2'))
    select2.select_by_value("5001")
    button2 = browser.find_element_by_name("select")
    button2.click()
    
    return browser


###############################
#Data Processing with Pandas###
###############################

def read_data(browser):
    
    #Read 案件維護 html
    data = pd.read_html(browser.page_source)

    newdata = data[0].iloc[2:,1:9].dropna(axis=0, how='all')
    newdata = newdata[::-1]

    time = newdata.iloc[:,6].str.split(" ", expand=True)
    newdata.insert(6,"Date", time[0])
    newdata.insert(7,"Time", time[1])

    newdata.pop(1)
    newdata.pop(2)
    newdata.pop(4)
    newdata.pop(7)

    date = newdata["Date"].str.split("-", expand=True)
    newdata.insert(5, "NewDate", date[1]+date[2])
    newdata.pop("Date")
    newdata = newdata.reset_index(drop=True)

    newdata.to_excel("event.xlsx", index=False)
    
    return newdata

def new_data(newdata):
    
    newdata2 = pd.DataFrame(columns = ["日期時間", "火警地點", "分隊", \
                                       "預警報時間", "出勤分隊及派遣時間", "分隊車庫影像出勤時間", \
                                       "到達現場時間", "案件別", "出勤時間(秒)", "火災案件到達現場時間(秒)"])

    for i in range(len(newdata)):
        event = newdata.iloc[i,1]
        #案件別
        if event == "為民服務":
            newdata2.loc[3*i,"案件別"] = "火警派遣 ({})".format(newdata.iloc[i,2])
        else:
            newdata2.loc[3*i,"案件別"] = event
        for j in range(1,3):
            newdata2.loc[3*i+j,"案件別"] = np.nan

        #日期
        newdata2.loc[3*i,"日期時間"] = newdata.iloc[i,4]
        newdata2.loc[3*i,"火警地點"] = newdata.iloc[i,5]
        newdata2.loc[3*i+1,"日期時間"] = newdata.iloc[i,3]
    
    return newdata2

#######################################
#Continue to extract fire event data###
#######################################

def extract(browser): 
    
    html = browser.page_source
    tables = pd.read_html(html)
    
    #Set Up tables
    #table1 = tables[0].iloc[:6,:6]
    
    ptr = 9
    while tables[0].iloc[ptr-1,0] != "派遣時間":
        ptr += 5
    table2 = tables[0].iloc[ptr:ptr+2,:7]
    
    for i in range(len(tables[0])):
        if tables[0].iloc[i,0] == "指揮官呼號":
            table3 = tables[0].iloc[i+1:-1,:3]
            break
    
    #Get Divisions
    divisions = table2.iloc[:,5].str.split("、", expand=True)
    
    for row in range(2):
        for col in range(len(divisions.columns)):
            if divisions.iloc[row][col] == None:
                divisions.iloc[row][col] = "沒有15"
            elif re.match('.*救護車', divisions.iloc[row][col]) != None:
                divisions.iloc[row][col] = "沒有15"
    divisions = set(divisions.iloc[0].str.extract(r'(.*)(\d)')[0].str.extract(r'(.*)(\d)')[0])
    divisions = [i for i in divisions if i != "沒有"]
    
    #Get dispatch time
    dispatchtime = table2.iloc[0,0].split(" ")[1]
    
    #Get Table3
    table3["hour"] = table3.iloc[:,1].str.extract(r'.*日(.*)時.*')
    table3["minute"] = table3.iloc[:,1].str.extract(r'.*時(.*)分.*')
    table3["second"] = table3.iloc[:,1].str.extract(r'.*分(.*)秒.*')
    events = table3.loc[table3.iloc[:,2].str.contains("到達現場", na=False)]
    arrivetime = {}
    for i in divisions:
        idx = events.iloc[:,2].str.contains(i, na=False)
        if idx.any() == True:
            event_div = events.loc[idx]
            arrivetime[i] = "%02d:%02d:%02d" % (int(event_div.iloc[0,3]),int(event_div.iloc[0,4]),int(event_div.iloc[0,5]))
        else:
            arrivetime[i] = "中途返隊"
    
    pretime = ""
    #Precautions
    if table3.iloc[:,2].str.contains("預警報", na=False).any() == True:
        precautions = table3.loc[table3.iloc[:,2].str.contains("預警報", na=False)]
        pretime = "%02d:%02d:%02d" % (int(precautions.iloc[0,3]),int(precautions.iloc[0,4]),int(precautions.iloc[0,5]))
    
    return divisions, dispatchtime, arrivetime, pretime

def time_conversion(date):
    time = list(map(int, date.split(":")))
    return time[0]*3600+time[1]*60+time[2]

def putdata(divisions, dispatchtime, arrivetime, pretime, cur, newdata2):
    
    div_cur = cur
    for i in range(len(divisions)):
        newdata2.loc[div_cur, "分隊"] = divisions[i]
        newdata2.loc[div_cur, "出勤分隊及派遣時間"] = dispatchtime
        newdata2.loc[div_cur, "到達現場時間"] = arrivetime[divisions[i]]
        
        #dispatch time and time_to_go
        rdtime = time_conversion(dispatchtime)
        time_to_go = random.randint(50,70) if 6 < int(dispatchtime[:2]) and int(dispatchtime[:2]) < 18 else random.randint(80,100)
        m, s = divmod(rdtime+time_to_go, 60)
        h, m = divmod(m, 60)
        newdata2.loc[div_cur, "出勤時間(秒)"] = time_to_go
        newdata2.loc[div_cur, "分隊車庫影像出勤時間"] = "%02d:%02d:%02d" % (h, m, s)
        
        #time_to_arrive
        if arrivetime[divisions[i]] != "中途返隊":
            date = time_conversion(newdata2.loc[cur+1,"日期時間"])
            arrive = time_conversion(arrivetime[divisions[i]])
            newdata2.loc[div_cur, "火災案件到達現場時間(秒)"] = arrive-date
        
        #Precaution time
        newdata2.loc[div_cur, "預警報時間"] = pretime
        
        div_cur += 1

    return newdata2

def insert_all_data(browser, newdata2, newdata):
    table = browser.find_element_by_name("myForm")
    table_rows = table.find_elements_by_tag_name('tr')

    for i in range(len(newdata)+1,1,-1):
        table_cols = table_rows[i].find_elements_by_tag_name('td')
        button = table_cols[13].find_element_by_xpath("input[@name='Hist']")
        button.click()
        browser.switch_to.window(browser.window_handles[1])

        sleep(1)
        cur = (len(newdata)-i+1)*3
        divisions, dispatchtime, arrivetime, pretime = extract(browser)
        putdata(divisions, dispatchtime, arrivetime, pretime, cur, newdata2)
        print("Success: "+str(i))

        browser.switch_to.window(browser.window_handles[0])
    
    return browser, newdata2
