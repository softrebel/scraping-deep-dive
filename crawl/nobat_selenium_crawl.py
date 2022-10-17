from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import ui
import time


srv=Service('geckodriver.exe')
driver=webdriver.Firefox(service=srv)


base_url='https://nobat.ir/find/city-1/c-7/page-{page}'
doctor_list=[]

page=1
while True:
    url=base_url.format(page=page)
    print('crawling ',url)
    driver.get(url)
    wait=ui.WebDriverWait(driver,10)
    wait.until(lambda driver:driver.find_element(By.XPATH,"//a[@class='drList nicehover']"))
    doctors=driver.find_elements(By.XPATH,"//a[@class='drList nicehover']")
    for doctor in doctors:
        name=doctor.find_element(By.XPATH,"div[@class='mainDetail']/div[contains(@class,'drName')]").text.strip()
        profession=doctor.find_element(By.XPATH,"div[@class='mainDetail']/div[contains(@class,'drSpecialty')]/h3").text.strip()
        doctor_list.append(dict(name=name,profession=profession))
    last = int(driver.find_element(By.XPATH,"//div[@class='paging']/a[last()]").text.strip())
    if page >= last:
        break
    page+=1
    time.sleep(3)

with open('output_crawl_selenium.json','w',encoding='utf-8') as f:
    import json
    f.write(json.dumps(doctor_list,ensure_ascii=False,indent=4))

driver.close()