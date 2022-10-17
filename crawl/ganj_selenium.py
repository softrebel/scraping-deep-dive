from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import ui
import time


srv=Service('geckodriver.exe')
driver=webdriver.Firefox(service=srv)

base_url="https://ganj.irandoc.ac.ir/#/search?basicscope=5&keywords=%D8%A8%D8%A7%D8%A8%DA%A9%20%D8%AA%DB%8C%D9%85%D9%88%D8%B1%D9%BE%D9%88%D8%B1&sort_by=1&fulltext_status=1&results_per_page=1&year_from=0&year_to=1401&page={page}"

page=1
article_xpath="//div[contains(@ng-repeat,'article in results')]"
header_xpath="div/h5"
article_list=[]
while True:
    url=base_url.format(page=page)
    print('crawling ',url)
    driver.get(url)
    wait=ui.WebDriverWait(driver,20)
    wait.until(lambda driver:driver.find_element(By.XPATH,f'{article_xpath}/{header_xpath}'))
    articles=driver.find_elements(By.XPATH,article_xpath)
    for article in articles:
        header=article.find_element(By.XPATH,header_xpath)
        title=header.text.strip()
        link=header.find_element(By.XPATH,'a').get_attribute('href')
        article_list.append(dict(title=title,link=link))
    last = int(driver.find_elements(By.XPATH,"//li[@ng-repeat='n in preparePaginate() track by $index']")[-1].text.strip())
    if page >= last:
        break
    page+=1
    time.sleep(3)
    

with open('output_ganj_crawl_selenium.json','w',encoding='utf-8') as f:
    import json
    f.write(json.dumps(article_list,ensure_ascii=False,indent=4))

driver.close()
