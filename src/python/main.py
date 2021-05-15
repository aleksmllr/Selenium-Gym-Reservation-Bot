from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import yaml
import time

def reserveGymSlot(timeSlot, name, key_fob_number):
    """
    This function will reserve the desired timeslot at my local Anytime Fitness Location at the furthest day away from the current day.
    You can reserve your gym slot a maximum of three days in before the day you plan to go to the gym. So if you want to book for Wednesday 9:00am 
    the earliest I can go on the Anytime Fitness Website to reserve my slot would be Monday 12:00am.

    I have designed this script this way so that I can put it on AWS and set up a CRON job to run the script at 12:01 AM on Tuesday, Wednesday, Saturday, and Sunday
    to reserve my 9:00 AM slot for Monday, Tuesday, Thursday, and Friday.

    Args:
        timeSlot (String): Pass gym time slot formatted like this "X:XX NN" X:XX is the time of day and NN is either AM or PM
    """
    # initialize webdriver and go to anytime fitness website
    driver = webdriver.Chrome()
    driver.get("https://reserve.anytimefitness.com/clubs/4812")
    # try to reserve gym time
    try:
        # Wait until login button has been located
        login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "user-action"))
        )
        # Click on Log-In Button
        login.click()
        # Wait until Log-In page has loaded and the key fob text bar has been located
        keyfob = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "keyfob"))
        )
        # send the Key Fob number to the appropriate text bar
        keyfob.clear()
        keyfob.send_keys(key_fob_number)
        # find the last name text box
        last_name = driver.find_element_by_name("lastName")
        last_name.clear()
        # send last name to appropriate text bar
        last_name.send_keys(name)
        # find the "look me up!" button and click it
        look_me_up = driver.find_element_by_xpath("/html/body/main/div/section[1]/form/section[2]/div[3]/button").click()

        reservation_content = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "res-content"))
        )

        # Get last reservation day
        last_day = reservation_content.find_elements_by_class_name("res-day")[-1]
        # Get the timeslots available in the last reservation day
        last_day_timeslots = last_day.find_elements_by_class_name("res-timeslot")
        # initialize variable to store the slot we want to select
        my_slot = None
        # for each time slot in the last reservation days available timeslots
        for slot in last_day_timeslots:
            # if the current slot is the desired time, store the time slot in my_slot variable
            if slot.text == timeSlot:
                my_slot = slot
        
        # print the text in the desired time slot

        my_slot_select = my_slot.find_element_by_class_name("res-timeslot-select").click()

        my_slot_confirm = my_slot.find_element_by_class_name("res-timeslot-confirm")

        driver.implicitly_wait(10)

        # the button was being hidden so I used an acction chain to help with the issue
        ActionChains(driver).move_to_element(my_slot_confirm).click(my_slot_confirm).perform()

        # Wait until confirmation screen is open and click finish
        finish = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "res-final-selectnew"))
        )

        finish.click()

    finally:
        driver.quit()


if __name__ == '__main__':
    credentials = open("credentials/creds.yaml")
    parsed_yaml = yaml.load(credentials, Loader=yaml.FullLoader)
    key = parsed_yaml["gymfo"]["aleks"]["key"]
    name = parsed_yaml["gymfo"]["aleks"]["last_name"]
    time_slot = parsed_yaml["gymfo"]["aleks"]["time_slot"]
    reserveGymSlot(time_slot, name, key)
