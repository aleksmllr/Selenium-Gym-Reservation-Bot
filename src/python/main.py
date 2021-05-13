from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import yaml
import time
# Goal: Reserve 9:00am Gym Slot three days from the current day

# Need a function that acquires the correct day based on current day

# Need a function to select the 9:00am time slot

def getDay():
    pass

def reserve(time):
    pass

# Get log-in information from the YAML file
credentials = open("credentials/creds.yaml")
parsed_yaml = yaml.load(credentials, Loader=yaml.FullLoader)
key = parsed_yaml["gymfo"]["key"]
last_name = parsed_yaml["gymfo"]["last_name"]

driver = webdriver.Chrome()
driver.get("https://reserve.anytimefitness.com/clubs/4812")

try:
    # Wait until login button has been located
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "user-action"))
    )
    # Click on Log-In Button
    element.click()
    # Wait until Log-In page has loaded and the key fob text bar has been located
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "keyfob"))
    )
    # send the Key Fob number to the appropriate text bar
    element.clear()
    element.send_keys(key)
    # find the last name text box
    element = driver.find_element_by_name("lastName")
    element.clear()
    # send last name to appropriate text bar
    element.send_keys(last_name)
    # find the "look me up!" button and click it
    element = driver.find_element_by_xpath("/html/body/main/div/section[1]/form/section[2]/div[3]/button").click()

    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "res-content"))
    )
    days = element.find_elements_by_class_name("res-day")

    for day in days:
        print(day)

    time.sleep(5)

    

finally:
    driver.quit()



