"""
Following code will read the name and birth date from the csv files and wish the person based on current system date
"""

# importing libs for general use
import time
import logging
from colorama import Fore
from os import path, mkdir, system, getcwd
from datetime import datetime as dt
from color_print import *

# generic log function for logging the following App logs
def log(msg):
    log_folder = r"D:\abhi_work\all_py\birthday_greeter\LOGS\WA_auto.log"
    if not path.exists(log_folder):
        mkdir(log_folder)
    # log_file = path.join(log_folder, "WA_auto.log")
    with open(log_folder, 'a') as logfile:
        print(f"{dt.now()} : {msg}")
        logfile.write(f"{dt.now()} : {msg}")
        logfile.write("\n")


# Importing the Libraries to be used
try:
    import csv
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.firefox.options import Options as Foptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
    import pyperclip as pc
except Exception as ex:
    log(f"Import Issue - {str(ex)}")


WA_URL = "https://web.whatsapp.com/"

# Comparing the date in csv with current date
def get_person_bday():
    # opening the csv as dictionary
    today = dt.now()
    day = today.day
    month = today.month
    try:
        # file_path = path.join(getcwd(), 'CSV', "b_day.csv")
        file_path = r"D:\abhi_work\all_py\birthday_greeter\CSV\b_day.csv"
        # print_green(file_path)
        with open(file_path, 'r') as bday_file:
            try:
                bday_data = csv.DictReader(bday_file)
                count = 0
                for data in bday_data:
                    if dt.strptime(data['Date'], "%d-%m").day == day and dt.strptime(data['Date'], 
                    "%d-%m").month == month :
                        count += 1  
                        intialize_driver(data['Name'])
                    else:
                        continue
                if count <= 0:
                    log(f"No B-Day today")
            except Exception as ex:
                log(f"Internal CSV File data Error : {str(ex)}")
    except Exception as ex:
        log(f"CSV opening issue : {str(ex)}")


# Initialising chrome driver based on current date
def intialize_driver(person):
    try:
        chrome_options = Options()
        chrome_options.add_argument("user-data-dir=C:\\Users\\DELL\\AppData\\Local\\Google\\Chrome\\User Data\\Default")   
        # chrome_options.add_argument("--headless")
    except Exception as ex:
        log(f"Chrome Options Error : {str(ex)}")

    try:
        exec_path = GeckoDriverManager().install()
        chrome = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        log(f"Driver Initialised for {person} B-Day")
        send_message(driver=chrome, person=person)
    except Exception as ex:
        log(f"Driver Initiliazation Issue : {str(ex)}")


# sends message using the passed driver to the passed person in the argument
def send_message(driver, person):
    # going to the web-site
    try:
        driver.get(WA_URL)
        log("Website Called")
        driver.implicitly_wait(30)
        log("Website Loaded")
        # waiting till whatsapp initialised and getting the person chat
        try:
            # max time the driver will wait is for 1min
            wait = WebDriverWait(driver, 60)
            
            chat = wait.until(EC.visibility_of_element_located((By.XPATH, f"//span[@title='{person}']")))
            # chat = driver.find_element(By.XPATH, f"//span[@title='{person}']")
            driver.implicitly_wait(30)
            chat.click()
            try:
                text_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@title='Type a message']")))
                # text_box = driver.find_element(By.XPATH, "//div[@title='Type a message']")
                # driver.implicitly_wait(30)
                
                text_box.send_keys("Happy Birthday")
                text_box.send_keys(Keys.ENTER)

                image_path = r"D:\abhi_work\all_py\birthday_greeter\Bday_Image\#1.jpg"
                
                log(f"Sent text Msg to : {person}")
                log(f"Attachment Path : {image_path}")

                # Sending Attachment Image Process
                attach = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Attach']")))
                # attach = driver.find_element(By.XPATH, "//div[@title='Attach']")
                # driver.implicitly_wait(30)
                attach.click()


                add_image = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")))
                # add_image = driver.find_element(By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")
                # driver.implicitly_wait(30)
                # print_green(f"Image Attach : {add_image}")
                try:
                    add_image.send_keys(image_path)
                    log("Attachment Added")
                    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Send']"))).click()
                    # driver.find_element(By.XPATH, "//div[@aria-label='Send']").click()
                    time.sleep(2)
                    wait.until(EC.presence_of_element_located((By.XPATH, "//img[@class='jciay5ix tvf2evcx oq44ahr5 lb5m6g5c']")))
                    # driver.find_element(By.XPATH, "//img[@class='jciay5ix tvf2evcx oq44ahr5 lb5m6g5c']")
                    # time.sleep(5)
                    log(f"Attachment Successfully Sent to {person}")
                except Exception as ex:
                    driver.save_screenshot(f".\\SS\\Attaching Error : {str(ex)}.png")
                    log(f"Attaching Error : {str(ex)}")

                log(f"Wished {person} successfully")
                print(f"Wished {person} successfully")
                driver.quit()
            except Exception as ex:
                driver.save_screenshot(f"Accessing_Text-Box_Error_of_{person}-{str(ex)}.png")
                log(f"Accessing Text-Box Error of {person} : {str(ex)}")

        except Exception as ex:
            driver.save_screenshot(f"Accessing_chat_Error_of_{person}-{str(ex)}.png")
            log(f"Accessing chat Error of {person} : {str(ex)}")

    except Exception as ex:
        driver.save_screenshot(f".\\SS\\Querying Website Error : {str(ex)}.png")
        log(f"Querying Website Error : {str(ex)}")

        


if __name__ == "__main__":
    system("cls")
    log(f"------------------ Execution Begun ------------------")
    get_person_bday()
    log(f"------------------ Execution Ended ------------------")

