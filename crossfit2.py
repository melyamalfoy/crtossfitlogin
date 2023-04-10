import os
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Website inloggegevens
USERNAME = 'username'
PASSWORD = 'password'

# Functie om webdriver te starten
def init_driver():
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver

# Functie om in te loggen op de website
def login(driver, username, password):
    driver.get("crossfitwebsite")

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "username"))
    ).send_keys(username)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "password"))
    ).send_keys(password)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//a[@class='button' and contains(@onclick, 'submit()')]"))
    ).click()

# Functie om de juiste les te kiezen en in te schrijven of te wachtlijsten
def choose_and_subscribe(driver):
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "next"))
    ).click()

    time.sleep(5)

    lessons = driver.find_elements(By.XPATH,
        "//a[contains(@class, 'box interact') and contains(@class, 'type-1') and contains(@data-time-start, '07:00')]"
    )

    # Loop door alle beschikbare lessen in de lijst
    for lesson in lessons:
        lesson_date = lesson.get_attribute('data-date')

         # Controleer of de les vol is door te zoeken naar het woord "full" in de class-attribuut van de les-element
        if "full" in lesson.get_attribute("class"):
            lesson.click()

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@onclick, 'aanmelden()') and contains(@class, 'button')]"))
            ).click()

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'javascript:void(0);') and contains(@class, 'button greyed')]"))
            )
            print(f"Waitlisted for {lesson_date} at 07:00")
        else:
            lesson.click()

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@onclick, 'aanmelden()') and contains(@class, 'button')]"))
            ).click()

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'javascript:void(0);') and contains(@class , 'button greyed')]"))
                )
            print(f"Subscribed for {lesson_date} at 07:00")

# Hoofdfunctie om het script uit te voeren
def main():
    driver = init_driver()
    login(driver, USERNAME, PASSWORD)
    choose_and_subscribe(driver)
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()
