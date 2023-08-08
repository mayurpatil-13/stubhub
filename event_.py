# from selenium import webdriver
# import time
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/94.0.4606.81 Safari/537.36')
# driver = webdriver.Chrome(options=chrome_options)
# driver.get("view-source:https://www.stubhub.com/philadelphia-eagles-tickets/performer/761/")

# time.sleep(10)

# html_source  = driver.find_element(By.ID,"index-data").get_attribute("innerHTML")

# print(html_source)

# driver.close()

from selenium import webdriver
from bs4 import BeautifulSoup
import time

chrome_options = Options()
chrome_options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.stubhub.com/philadelphia-eagles-tickets/performer/761/')
time.sleep(10)

soup = BeautifulSoup(driver.page_source,'html.parser')
# script  = soup.find("script", {"id": "index-data"}).text.strip()

print(soup.prettify())