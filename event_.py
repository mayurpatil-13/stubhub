# import time
# import pandas as pd
# from selenium import webdriver
# from selenium.common.exceptions import (NoSuchElementException,
#                                         StaleElementReferenceException,
#                                         TimeoutException)
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# import pandas as pd
# import time
# import pymongo

# driver = webdriver.Chrome() 
# driver.maximize_window()

# # client = pymongo.MongoClient('mongodb+srv://aniketchopade2971:Aniket2971@cluster0.scwcgeh.mongodb.net/')

# def getEvent():
 
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get("https://www.stubhub.com/new-york-giants-tickets/performer/6184/")

# Wait for the page to load completely
time.sleep(20)

# Get the page source
html_source = driver.page_source

# Search for the script element with id "index-data" in the page source
script_start = html_source.find('<script id="index-data"')
script_end = html_source.find('</script>', script_start)

if script_start != -1 and script_end != -1:
    # Extract the script content
    script_content = html_source[script_start:script_end]
    print(script_content)
else:
    print("Script element not found.")

# Close the WebDriver
driver.quit()
