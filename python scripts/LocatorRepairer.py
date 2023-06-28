from bs4 import BeautifulSoup
# from io import StringIO, BytesIO
import sqlite3
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException
from selenium.webdriver.common.by import By
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.remote.file_detector import LocalFileDetector


  
def get_webdriver_instance():
    seleniumlib = BuiltIn().get_library_instance('SeleniumLibrary')
    return seleniumlib.driver

def insert_element(locator):
    driver = get_webdriver_instance()
    test_name = BuiltIn().get_variable_value('${TEST NAME}')
    test_path = BuiltIn().get_variable_value('${SUITE SOURCE}')
    print(test_path)
    try:
        element = driver.find_element(determine_locating_strategy(driver,locator),locator)
    except [NoSuchElementException,InvalidSelectorException] as e:
        repair_locator()
    os.getcwd()
    e_id = str(element.get_attribute("id"))
    e_class = str(element.get_attribute("class"))
    e_name = str(element.get_attribute("name"))
    e_value = str(element.get_attribute("value"))
    e_type = str(element.get_attribute("type"))
    e_alt = str(element.get_attribute("alt"))
    e_src = str(element.get_attribute("src"))
    e_href = str(element.get_attribute("href"))
    e_size = str(element.get_attribute("size"))
    e_onclick = str(element.get_attribute("onclick"))
    e_height = str(element.get_attribute("height"))
    e_width = str(element.get_attribute("width"))
    e_xpath = str(element.get_attribute("xpath"))
    x_axis = str(element.value_of_css_property("x-axis"))
    y_axis = str(element.value_of_css_property("y-axis"))
    img_b64 = str(element.screenshot_as_base64)
    # print("id:"+str(e_id))
    # print("class:"+str(e_class))
    # print("name:"+str(e_name))
    # print("value:"+str(e_value))
    # print("type:"+str(e_type))
    # print("alt:"+str(e_alt))
    # print("src:"+str(e_src))
    # print("href:"+str(e_href))
    # print("size:"+str(e_size))
    # print("onclick:"+str(e_onclick))
    # print("height:"+str(e_height))
    # print("width:"+str(e_width))
    # print("xpath:"+str(e_xpath))
    # print("x:"+str(x_axis))
    # print("y:"+str(y_axis))
    print(locator)
    
    database =  "BGLocators.db"
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        query = "INSERT INTO locator VALUES('"+e_id+"','"+test_name+"','"+test_path+"', '"+e_class+"','"+e_name+"','"+e_value+"','"+e_type+"','"+e_alt+"','"+e_src+"','"+e_href+"','"+e_size+"','"+e_onclick+"','"+e_height+"','"+e_width+"','"+e_xpath+"','"+x_axis+"','"+y_axis+"','"+img_b64+"');"
        # query = 'Select * from locator;'
        # print(query)
        cursor.execute(query)
        sqliteConnection.commit()
        # result = cursor.fetchall()
        # print('SQLite Version is {}'.format(result))
    except Exception as e:
        print(e)

def determine_locating_strategy(driver, string):
    # Check if the string is an ID
    try:
        if  driver.find_elements(By.ID, string):
            return By.ID
    except:
        pass
    # Check if the string is a class name
    try:
        if  driver.find_elements(By.CLASS_NAME, string):
            return By.CLASS_NAME
    except:
        pass
    try:
        # Check if the string is a name
        if  driver.find_elements(By.NAME, string):
            return By.NAME
    except:
        pass
    try:
        # Check if the string is a link text
        if  driver.find_elements(By.LINK_TEXT, string):
            return By.LINK_TEXT
    except:
        pass
    try:
        # Check if the string is a partial link text
        if  driver.find_elements(By.PARTIAL_LINK_TEXT, string):
            return By.PARTIAL_LINK_TEXT
    except:
        pass
    try:
        # Check if the string is a tag name
        if  driver.find_elements(By.TAG_NAME, string):
            return By.TAG_NAME
    except:
        pass
    try:
        # Check if the string is an XPath
        if  driver.find_elements(By.XPATH, string):
            return By.XPATH
    except:
        pass
        
def repair_locator(locator):
    pass