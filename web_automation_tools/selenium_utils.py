"""
Purpose: This package allows for interaction with webpages
and not just scraping (clicking buttons, entering forms, etc...)


"""
import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# -- setting up the chrome adapter for driver --
"""
How to get the .exe file
1) 3 dots in top right corner > Help > About Google Chrome
--> will show what version of chrome you have and if version is up to date

2) Download the zip folder
    download: https://sites.google.com/chromium.org/driver/
3) Extract and and get the path all the way to the exe file

"""
from pathlib import Path
chrome_driver_path = str(
    Path("C:/Users/celii/Downloads/chromedriver_win32/chromedriver.exe").absolute()
)



searching_notes = """
options like find, find_all
- find_element(name,"the value") # us the BY package to get the right name
- find_elements(name,"value")

from selenium.webdriver.common.by import By

# the By class just is a mapping of the concept to the string
ID = "id", NAME = "name", XPATH = "xpath", TAG_NAME = "tag name", CLASS_NAME = "class name"

# by id:
login_form = driver.find_element(By.ID, 'loginForm')

# by xml
login_form = driver.find_element(By.XPATH, "/html/body/form[1]")

# by tag name
heading1 = driver.find_element(By.TAG_NAME, 'h1')

# by class name
content = driver.find_element(By.CLASS_NAME, 'content')
"""

entering_input_notes = """
The keys class is like typing keys in keyboard
from selenium.webdriver.common.keys import Keys

Ex:'ARROW_DOWN','DOWN','END','ENTER',

Example of using: 
elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
"""


def example_headless_driver(url = 'https://duckduckgo.com'):
    
    # setting the options to be headless
    options = Options()
    options.add_argument("--headless")
    assert options.headless
    
    # creating a headless chrome driver with path to the .exe file
    driver = Chrome(chrome_driver_path,options = options)
    
    # finding an element and writing some text into it
    elem = driver.find_element(By.NAME, "q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    
    #checking that some results were found
    assert "No results found." not in driver.page_source
    
    # closing the headless driver
    driver.close()


def example_find_link_where_text_equal():
    """
    The A represents looking for a link tag
    and the inside part specifies what we want the text equal to
    """
    driver.find_elements_by_xpath("//a[text()='Locations']")


import selenium_utils