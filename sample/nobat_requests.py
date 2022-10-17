import requests
from bs4 import BeautifulSoup
import json
items = []
url = 'https://nobat.ir/'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')
doctors = soup.find_all('a', {'class': 'drList nicehover'})

for doctor in doctors:
    detail = doctor.find('div', {'class': 'mainDetail'})
    title = detail.find('div', {'class': 'drName font-size-14'}).text.strip()
    profession = detail.find('div', {'class': 'drSpecialty'}).text.strip()
    items.append({
        'title': title,
        'profession': profession
    })

with open('test_request.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(items, ensure_ascii=False, indent=4))
