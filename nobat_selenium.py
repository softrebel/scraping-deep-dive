from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import ui


def get_doctors(url):
    srv=Service('geckodriver.exe')
    driver=webdriver.Firefox(service=srv)
    driver.get(url)
    items=[]
    wait=ui.WebDriverWait(driver,10)
    wait.until(lambda driver:driver.find_element(By.XPATH,"//a[@class='drList nicehover']"))
    doctors=driver.find_elements(By.XPATH,"//a[@class='drList nicehover']")

    for doctor in doctors:
        name=doctor.find_element(By.XPATH,"div[@class='mainDetail']/div[contains(@class,'drName')]").text.strip()
        profession=doctor.find_element(By.XPATH,"div[@class='mainDetail']/div[contains(@class,'drSpecialty')]/h3").text.strip()
        items.append(dict(name=name,profession=profession))
    with open('output_selenium.json','w',encoding='utf-8') as f:
        import json
        f.write(json.dumps(items,ensure_ascii=False,indent=4))

    driver.close()

get_doctors('https://nobat.ir/')