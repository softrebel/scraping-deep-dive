import requests
import json
import time 
ads = []
import random
from os.path import exists

def extract_posts(content):
    base_url="https://api.divar.ir/v8/posts-v2/web/{token}"
    posts = content['web_widgets']['post_list']
    for post in posts:
        data = post['data']
        token=data['action']['payload']['token']
        print('crawling',token)
        if exists(f'files/{token}.json'):
            print('exists')
            continue
        post={
            'title': data['title'],
            'top': data['top_description_text'],
            'middle': data['middle_description_text'],
            'bottom': data['bottom_description_text'],
            'token':data['action']['payload']['token'],
            'description':'',
            'info':[]
        }
        res=requests.get(base_url.format(token=post['token']))
        content=json.loads(res.text)
        for section in content['sections']:
            if section['section_name']=='DESCRIPTION':
                post['description']=section['widgets'][-1]['data']['text']
            elif section['section_name']=='LIST_DATA':
                for widget in section['widgets']:
                    if widget['widget_type']=='GROUP_INFO_ROW':
                        post['info'].extend(widget['data']['items'])
                    elif widget['widget_type']=='UNEXPANDABLE_ROW':
                        post['info'].append({
                            'title':widget['data']['title'],
                            'value':widget['data']['value'],
                        })
        with open(f"files/{post['token']}.json", 'w', encoding='utf-8') as f:
            f.write(json.dumps(post, ensure_ascii=False, indent=4))
        seconds=random.randint(3,10)
        time.sleep(seconds)



def get_first_page():
    print('crawling first page')
    url = 'https://api.divar.ir/v8/web-search/tehran/vehicles'
    res = requests.get(url)
    content = json.loads(res.text)
    extract_posts(content)
    return content['last_post_date']


def get_other_pages(last_post_date):
    print('crawling other pages')
    for i in range(4):
        url = 'https://api.divar.ir/v8/web-search/tehran/vehicles'
        payload = json.dumps({
            "json_schema": {
                "category": {
                    "value": "vehicles"
                },
                "cities": [
                    "1"
                ]
            },
            "last-post-date": last_post_date
        })
        headers = {
            'Content-Type': 'application/json'
        }
        res = requests.post(url, headers=headers, data=payload)
        content = json.loads(res.text)
        extract_posts(content)

        last_post_date = content['last_post_date']
        time.sleep(4)



last_post_date=get_first_page()
get_other_pages(last_post_date)

