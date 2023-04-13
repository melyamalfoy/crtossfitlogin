import os
import datetime
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# Website inloggegevens
USERNAME = 'xxx'
PASSWORD = 'xxx'

# Functie om webdriver te starten
def init_driver():
    #chrome_options = Options() # comment this line to see the browser
    #chrome_options.add_argument("--headless") # comment this line to see the browser
   # chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) # zet afbeeldingen uit
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver

# Functie om in te loggen op de website
def login(driver, username, password):
    driver.get("xxx")

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "username"))
    ).send_keys(username)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "password"))
    ).send_keys(password)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//a[@class='button' and contains(@onclick, 'submit()')]"))
    ).click()

# configure logger
logging.basicConfig(filename='logbook.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')



def choose_and_subscribe(driver):
    # Bereken de datum van volgende week
    next_week = datetime.date.today() + datetime.timedelta(days=7)
    next_week_str = next_week.strftime("%d-%m-%Y")

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "next"))
    ).click()

    # lessons = driver.find_elements(By.XPATH,
    #     f"//a[contains(@class, 'box interact') and contains(@class, 'type-1') and contains(@data-date, '{next_week_str}') and contains(@data-time-start, '07:00')]"
    # )
    lessons = driver.find_elements(By.XPATH,
        f"//a[contains(@class, 'box interact') and contains(@class, 'type-1') and contains(@data-date, '{next_week_str}') and contains(@data-time-start, '07:00') or contains(@class, 'selected')]"
    )


    # Loop door alle beschikbare lessen in de lijst
    for lesson in lessons:
        lesson_date = lesson.get_attribute('data-date')
        lesson_classes = lesson.get_attribute("class")

        if lesson_date is None:
            continue

        elif "selected" in lesson_classes:
            message = f"Already registered or waitlisted for {lesson_date} at 07:00"
            print(message)
            logging.info(message)
        elif "full" in lesson_classes:
            lesson.click()

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@onclick, 'aanmelden()') and contains(@class, 'button')]"))
            ).click()

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'javascript:void(0);') and contains(@class, 'button greyed')]"))
            )
            message = f"Waitlisted for {lesson_date} at 07:00"
            print(message)
            logging.info(message)
        else:
            lesson.click()

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@onclick, 'aanmelden()') and contains(@class, 'button')]"))
            ).click()

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'javascript:void(0);') and contains(@class , 'button greyed')]"))
            )
            message = f"Subscribed for {lesson_date} at 07:00"
            print(message)
            logging.info(message)

# Hoofdfunctie om het script uit te voeren
def main():
    driver = init_driver()
    login(driver, USERNAME, PASSWORD)
    choose_and_subscribe(driver)
    message ="Program has run successfully"
    time.sleep(5)
    driver.quit()
    # Log het einde van het programma
    logging.info(message)

if __name__ == "__main__":
    main()
