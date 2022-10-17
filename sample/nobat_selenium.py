from config import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import ui
srv = Service('geckodriver.exe')
driver = webdriver.Firefox(service=srv)
url = 'https://nobat.ir/'
driver.get(url)
items = []
wait = ui.WebDriverWait(driver, 10)
wait.until(lambda driver: driver.find_element(
    By.XPATH, "//a[contains(@class,'drList')]"))

doctors = driver.find_elements(By.XPATH, "//a[contains(@class,'drList')]")
for doctor in doctors:
    detail = doctor.find_element(By.XPATH, "//div[@class='mainDetail']")
    name = detail.find_element(
        By.XPATH, "//div[contains(@class,'drName')]").text.strip()
    profession = detail.find_element(
        By.XPATH, "//div[@class='drSpecialty']/h3").text.strip()
    items.append({
        'name': name,
        'profession': profession
    })


write_json(items, 'test_selenium')
