import re
import requests
from bs4 import BeautifulSoup

doctor_list=[]
def parse_item(url):
    res=requests.get(url)
    if res.status_code != 200:
        print('error')
        return
    
    soup=BeautifulSoup(res.text,'lxml')
    doctors=soup.find_all('a',{'class':'drList nicehover'})
    for doctor in doctors:
        doctor_dict= dict()
        doctor_dict['name']=doctor.find('div',{'class':'mainDetail'}).find('div',{'class':'drName'}).text.strip()
        doctor_dict['profession']=doctor.find('div',{'class':'mainDetail'}).find('div',{'class':'drSpecialty'}).find('h3').text.strip()
        doctor_list.append(doctor_dict)


    return doctor_list



url='https://nobat.ir/'
items=parse_item(url)

with open('output_requests.json','w',encoding='utf-8') as f:
    import json
    f.write(json.dumps(items,ensure_ascii=False,indent=4))