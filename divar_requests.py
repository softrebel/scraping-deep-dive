import requests
from lxml import html
url='https://divar.ir/s/tehran/auto'

res=requests.get(url)

ads_list=[]
tree=html.fromstring(res.text)
#  =BeautifulSoup(res.text,'lxml')
# entity=lxml()
xpath="//article[contains(@class,'kt-post-card')]/div[1]"
ads=tree.xpath(xpath)
for ad in ads:
    title=ad.xpath('h2/text()')[0]
    description=ad.xpath('div/text()')[0]
    ads_detail={
        'title':title,
        'description':description 
    }
    ads_list.append(ads_detail)

with open('result.json','w',encoding='utf-8') as f:
    import json
    f.write(json.dumps(ads_list,ensure_ascii=False,indent=4))