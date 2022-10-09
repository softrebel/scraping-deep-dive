import requests
import json
import time 
ads = []



def extract_posts(content):

    posts = content['web_widgets']['post_list']
    for post in posts:
        data = post['data']
        ads.append({
            'title': data['title'],
            'top': data['top_description_text'],
            'middle': data['middle_description_text'],
            'bottom': data['bottom_description_text'],
        })


def get_first_page():
    url = 'https://api.divar.ir/v8/web-search/tehran/vehicles'
    res = requests.get(url)
    content = json.loads(res.text)
    extract_posts(content)
    return content['last_post_date']


def get_other_pages(last_post_date):
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
with open('output_api.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(ads, ensure_ascii=False, indent=4))
