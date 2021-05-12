import yaml

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

driver.quit()
