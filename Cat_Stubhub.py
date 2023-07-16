import ssl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
import pymongo

client = pymongo.MongoClient('mongodb+srv://aniketchopade2971:Aniket2971@cluster0.scwcgeh.mongodb.net/')

db = client['stubhub-database']

cat_collection = db.Entity

cat_collection.insert_one({"start": 'Okay'})

print("mongodb connecting ...")
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 800))  
display.start()

chrome_options = Options()

chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=1400,1500")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("enable-automation")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-dev-shm-usage")


def check_doccument(data):
    result = cat_collection.find_one(data)
    if result:
        return False
    else:
        return True
        
def entityDataExtract():
    driver = webdriver.Chrome(options=chrome_options)

    # ==== category list
    urls_list = ['https://www.stubhub.com/sports-tickets/category/28/' , 'https://www.stubhub.com/concert-tickets/category/1/' , 'https://www.stubhub.com/theater-and-arts-tickets/category/174/']

    categories =[ 'Sports' , 'Concerts' ,'TheatreAndArts']
    i=0

    for url in urls_list:
        df = pd.DataFrame(columns = ['name' ,'stubhub_entity_id' ,'category_name','entityLink' , 'type'])

        driver.get(url)

        wait = WebDriverWait(driver, 20)

        arrow = True
        print("loading all web page data...")

        # ==== loading all data
        while(arrow != False):
            WebDriverWait(driver , 20)
            time.sleep(2)
            try:
                element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "jsLylC", " " ))]'))
            )   
                if element.is_displayed():
                    element.click()
            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                arrow = False

        WebDriverWait(driver , 30)
            
        event_element = driver.find_elements('xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "dMxVrR", " " ))]/a')

        events_list =[]
        print("======")
        print(len(event_element))
        
        # ==== adding data to mongodb
        for element in event_element: 
            
            event_content = element.get_attribute('href')
            splitted_link = event_content.split("/")
            name =splitted_link[len(splitted_link)-4]
            stubhub_entity_id = splitted_link[len(splitted_link)-2]
            type =splitted_link[len(splitted_link)-3] 
        
            row_data = {'name':name , 'stubhub_entity_id':stubhub_entity_id ,'category_name':categories[i]  ,'entityLink' : event_content , 'type':type}
        
            # ==== add data to dataframe
            pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)    
            # df = df.append(row_data,ignore_index = True)
            
            if check_doccument(row_data):
                cat_collection.insert_one(row_data)
            events_list.append(event_content)
        print("======")
        print(len(events_list))
        
        df.to_csv(categories[i]+'.csv')
        i+=1

    # Close the WebDriver
    driver.quit()
    
entityDataExtract()
        