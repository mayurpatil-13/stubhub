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

print("done")
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


driver = webdriver.Chrome(options=chrome_options)




urls_list = ['https://www.stubhub.com/sports-tickets/category/28/' , 'https://www.stubhub.com/concert-tickets/category/1/' , 'https://www.stubhub.com/theater-and-arts-tickets/category/174/']

categories =[ 'Sports' , 'Concerts' ,'TheatreAndArts']
i=0

for url in urls_list:
    # url ='https://www.stubhub.com/sports-tickets/category/28/'
    df = pd.DataFrame(columns = ['name' ,'stubhub_entity_id' ,'category_name','entityLink' , 'type'])

    driver.get(url)

    wait = WebDriverWait(driver, 20)
    # script_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'jsnpzz')))


    arrow = True

    while(arrow != False):
        print("fetching...")
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


    # Extract the content of the script element
    # script_content = script_element.get_attribute('innerHTML')

    events_list =[]
    print("======")
    print(len(event_element))
    for element in event_element: 
        event_content = element.get_attribute('href')
        splitted_link = event_content.split("/")
        name =splitted_link[len(splitted_link)-3]
        stubhub_entity_id = splitted_link[len(splitted_link)-1]
        type =splitted_link[len(splitted_link)-2] 
        row_data = {'name':name , 'stubhub_entity_id':stubhub_entity_id ,'category_name':categories[i]  ,'entityLink' : event_content , 'type':type}  
        # 'name' ,'stubhub_entity_id' ,'category_name','entityLink' , 'type'
        pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)    
        df = df.append(row_data,ignore_index = True)
        cat_collection.insert_one(row_data)
        print(event_content)
        events_list.append(event_content)
    print("======")
    print(len(events_list))
    # Print the script content
    # print(script_content)

    df.to_csv(categories[i]+'.csv')
    i+=1
    break

# Close the WebDriver
driver.quit()

