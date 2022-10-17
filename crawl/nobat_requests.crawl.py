import requests
from bs4 import BeautifulSoup
import os

os.chdir(os.path.dirname(__file__))
base_url='https://nobat.ir/find/city-1/c-7/page-{page}'
doctor_list=[]
doctor_url = 'https://nobat.ir{url}'
page=1
while True:
    url=base_url.format(page=page)
    print('crawling ',url)
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'lxml')
    doctors=soup.find_all('a',{'class':'drList nicehover'})
    for doctor in doctors[:10]:
        doctor_dict= dict()
        doctor_dict['name']=doctor.find('div',{'class':'mainDetail'}).find('div',{'class':'drName'}).text.strip()
        doctor_dict['profession']=doctor.find('div',{'class':'mainDetail'}).find('div',{'class':'drSpecialty'}).find('h3').text.strip()
        print('crawling',doctor_dict['name'])
        res=requests.get(doctor_url.format(url=doctor['href']))
        doc_soup=BeautifulSoup(res.text,'lxml')
        extra = []
        for field in doc_soup.select('li[class=list-inline-item]>span'):
            extra.append(field.text.strip())
        doctor_dict['extra']=extra
        doctor_list.append(doctor_dict)

    
    last=int(soup.find_all('a',{'class':'pageButton'})[-1].text.strip())
    # last = int(response.xpath("//div[@class='paging']/a[last()]/text()").extract_first())
    if page >= last:
        break
    page+=1
 
with open('output_crawl_requests.json','w',encoding='utf-8') as f:
    import json
    f.write(json.dumps(doctor_list,ensure_ascii=False,indent=4))