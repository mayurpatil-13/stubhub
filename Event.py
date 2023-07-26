import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time
import pymongo

driver = webdriver.Chrome() 

client = pymongo.MongoClient('mongodb+srv://aniketchopade2971:Aniket2971@cluster0.scwcgeh.mongodb.net/')

def getEvent():
 
    db = client['stubhub-database']
    # Collection Name
    collection1 = db["Entity"]
    collection2 = db['Event']
    
    collection2.insert_one({'demo': "start"})
     
    x = collection1.find()
    
    for doc in x:
        eventUrl = doc['entityLink']
        driver.get(eventUrl)

        wait = WebDriverWait(driver, 20)
        script_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'itMvpa')))

        arrow = True

        while(arrow != False):
            WebDriverWait(driver , 20)
            time.sleep(2)
            try:
                element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "Gxbhw", " " ))]'))
            )   
                if element.is_displayed():
                    element.click()
            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                arrow = False

        WebDriverWait(driver , 20)
            
        event_element = driver.find_elements('xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "jUPiq", " " ))]')


        # Extract the content of the script element
        script_content = script_element.get_attribute('innerHTML')

        events_list =[]
        print("======")
        print(len(event_element))
        for element in event_element: 
            event_content = element.get_attribute('href') 
            url_split = event_content.split("/")
            id = url_split[-2]   
            df = df.append({'EventId' : id},
            ignore_index = True)
            
            print(event_content)
            events_list.append(event_content)
        print("======")
        print(len(events_list))
        # Print the script content
        print(script_content)
        print("*******")
        # c = str(category)
        # df.to_csv(c+'Event'+str(eventIndex)+'.csv')
        eventIndex+=1
        break

# Close the WebDriver
driver.quit()


# event name  = hTAheq
# venue = izfGNU
#  city = PDGnu
# date = cixORU
# day = hrVwEA
# time = bbCMQq
# 
        