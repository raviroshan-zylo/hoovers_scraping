# to Scrape uploaded file from aventions site

from multiprocessing.sharedctypes import Value
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
import os



cd = os.path.abspath(__file__)
fileDirectory = os.path.dirname(cd)
parentDirectory = os.path.dirname(fileDirectory)

driver = webdriver.Chrome(ChromeDriverManager().install())
#input = r"/Users/vivek.verma/Documents/code/HVRS_Automation/input/lists_to_scrape.csv"


def reading_file():
    try:
        file = pd.read_csv(parentDirectory + '/hoovers_scraping/input/lists_to_scrape.csv')
        #file = pd.read_csv(r"/Users/vivek.verma/Documents/E_DRIVE/Python/hoover;s/input/chunks_74.csv")
        settings_value = file['Settings value'].to_list()

        url_list = file['list_url'].to_list()
        #userid ="shikha.sharma@zylotech.in"
        #user_password = "zylotech@202"
        
        userid = settings_value[0]
        user_password = settings_value[1]
        grid = settings_value[2]
        sort = settings_value[3]
        list_url = url_list
    except:
        raise Exception('unable to read input file/data value')
    # print("Input Reading File.....")
    return [userid,user_password,grid,sort,list_url]
    



#### Settings 
fileread = reading_file() 
userid = fileread[0]
userpassword = fileread[1]
list_url = fileread[4]      # url of the list to scrape
grid = fileread[2]          #grid name to scrape
sort = fileread[3]          # data sorting order name



#### Settings 
# userid = 'mohit.rathor@zylotech.in'
# userpassword = 'Terminus@2030'
# list_urls = [
#             'https://app.avention.com/list/9c684c82-a342-4817-ac96-a0e102e839a4',
#             'https://app.avention.com/list/375f0b39-06c6-4c5c-a60b-7d815dc693c1'] 
            #['https://app.avention.com/list/235c8316-dca9-4770-9e1a-035182779cec','https://app.avention.com/list/d3009c42-09ee-417b-bd57-4e6067630feb','https://app.avention.com/list/fa4756d4-a6bf-4adf-9a98-53842ef54771']    # url of the list to scrape


# grid = 'D&B Company Grid'        #grid name to scrape
# sort = 'Matched: Yes'        # data sorting order name


# to login to the hoovers site.



def hoovers_login(login_id,login_password):
    """this functions logs in to the avention site in 
        a chrome browser instance and returns the browser instance.

    Args:
        login_id (string): avention user id
        login_password (string): avention password

    Returns:
        object: browser instance
    """    

    if login_id == '' or login_password == '':
        raise Exception('login credentials not passed')

    #driver = webdriver.Chrome()
    global driver
    
    
    
    driver.get('https://app.avention.com/')
    time.sleep(6)
    print("Input Reading File.....")


    #driver.find_element_by_id('username').send_keys(userid)
    driver.find_element(By.ID,'username').send_keys(userid)
    
    time.sleep(4)
    #driver.find_element_by_class_name('continue-btn').click()
    driver.find_element(By.CLASS_NAME,'continue-btn').click()
    
    time.sleep(4)
    #driver.find_element_by_id('password').send_keys(userpassword)
    driver.find_element(By.ID,'password').send_keys(userpassword)
    
    
    time.sleep(4)
    #driver.find_element_by_class_name('continue-btn').click()
    driver.find_element(By.CLASS_NAME,'continue-btn').click()
    
    time.sleep(5)

    #Checking if logged in without any issue
    try:
        #login_error = driver.find_element_by_class_name("login-error").text
        login_error = driver.find_element(By.CLASS_NAME,"login-error").text
        
        time.sleep(2)
    except:
        login_error=""

    if "login credentials are already in use" in login_error:
        raise Exception("login credentials are already in use")
    elif "Invalid User Name or Password" in login_error:
        raise Exception("Invalid User Name or Password")
    time.sleep(5)
    if driver.current_url != 'https://app.avention.com/':
            raise Exception('Some Error Occured, Login failed')



    print('logged in successfully')
    return driver


#To logout of avention site.
def hoovers_logout(driver):
    """to logout of avention

    Args:
        driver (object): looged in browser instance
    """
    driver.execute_script("window.scrollTo(document.body.scrollHeight,0)")
    time.sleep(8)    
    #driver.find_elements_by_class_name('ant-menu-submenu-horizontal')[4].click()
    driver.find_elements(By.CLASS_NAME,'ant-menu-submenu-horizontal')[4].click()
    
    time.sleep(8)
    #log_out_list = driver.find_element_by_class_name('side-menu-dropdown').find_elements_by_tag_name('li')
    log_out_list = driver.find_element(By.CLASS_NAME,'side-menu-dropdown').find_elements(By.TAG_NAME,'li')

    
    #looping through the list to find out logout
    for each in log_out_list:
        if each.text == 'Logout':
            each.click()
            print('Logged out successfully')
            break



def hoovers_table_to_csv(page_source):
    """to save avention result table into a csv

    Args:
        page_source (object): page souce of selenium browser instance

    Returns:
        _type_: pandas df
    """    

    soup = BeautifulSoup(page_source,'html.parser')
    soup.find(class_="ant-table-container")
    table = pd.read_html(page_source)[1]

    with open("output/result_output_file.csv","a+",encoding="utf-8") as f:
        table.to_csv(f,header=False,index=False)
    return table



def hoovers_file_list_navigation(url,driver):
    """Navigates through all the pages of avention list and copies result in csv.

    Args:
        url (string): url of the file which has been uploaded
        driver (object): selenium chrome browser instance
    """    
    try:
        driver.maximize_window()
        driver.implicitly_wait(15) # waiting for 15 second for elements to be found
        driver.get(url) 
        time.sleep(6)

        #driver.find_element_by_class_name('selected-view-icon').click()
        driver.find_element(By.CLASS_NAME,'selected-view-icon').click()
        
        time.sleep(3)
        #driver.find_element_by_class_name('view-table-label').click()    #udate class
        
        driver.find_elements(By.CLASS_NAME,'top-level-view')[1].click()
        time.sleep(3)

        # grid table list
        #tables = driver.find_element_by_class_name('view-selection-dropdown').find_element_by_class_name('sliding-navigation').find_elements_by_tag_name('li')

        tables = driver.find_element(By.CLASS_NAME,'view-selection-dropdown').find_element(By.CLASS_NAME,'sliding-navigation').find_elements(By.TAG_NAME,'li')

        for each in tables:
            if each.text == grid:  # selecting the result table as per passed 'grid' variable value
                each.click()
                break


        time.sleep(6)

        #driver.find_elements_by_class_name('ant-select-selection-item')[1].click()
        driver.find_elements(By.CLASS_NAME,'ant-select-selection-item')[1].click()
        
        time.sleep(5)
        
        # Sorting order options
        #sorting_list = driver.find_elements_by_class_name('ant-select-item-option-content')

        sorting_list = driver.find_elements(By.CLASS_NAME,'ant-select-item-option-content')

        for each in sorting_list:
            if each.text == sort: # selecting the table order as per passed 'sort' variable value
                each.click()
            
        # Counting total pages to navigate
        #total_result = driver.find_element_by_class_name('vertical-align-middle').find_element_by_tag_name('span').text
        total_result = driver.find_element(By.CLASS_NAME,'vertical-align-middle').find_element(By.TAG_NAME,'span').text
        
        #print(total_result)
        #total_pages_count = round(int(total_result)/25)
        #total_pages_count = round(int(total_result.replace(' Results',''))/25)
        total_pages_count = round(int(total_result.replace(',',''))/25)
        
        

        # Navigating through each page
        for x in range(total_pages_count):
            #print(total_pages_count) 
            time.sleep(6)
            table =  hoovers_table_to_csv(driver.page_source) # Calling this function to save result in csv
            #print(table)
        
            if len(table[1].drop_duplicates()) ==1:
                # print('all data copied from url ', url)
                break
            
            #driver.find_element_by_class_name('pagination-nav')[2].click()
            
            #driver.find_element(by = By.CLASS_NAME,Value)

            
            #driver.find_element_by_id('next').click()
            driver.find_element(By.XPATH,"(//button[@class = 'pagination-nav'])[2]").click()
            time.sleep(6)
        print('all data copied from url ', url)
        driver.minimize_window()
    except Exception as e:
        print(e," Copied ",url," pages= ", x)
        hoovers_logout(driver)
        


def list_scraping():
    driver = hoovers_login(userid,userpassword)
    for each_url in list_url:
        hoovers_file_list_navigation(each_url,driver)
    
    try:
        
        time.sleep(2)
        hoovers_logout(driver)
    except:
        driver.refresh()
        time.sleep(5)
       
        hoovers_logout(driver)

    print('All urls Copied')   


list_scraping()