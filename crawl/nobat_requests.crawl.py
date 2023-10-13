import requests
from bs4 import BeautifulSoup
import os
import json

import time
# pip install requests

start = time.time()
os.chdir(os.path.dirname(__file__))
base_url = "https://nobat.ir/find/city-1/c-7/page-{page}"
doctor_list = []
page = 1
for item in range(1, 6):
    page = item
    url = base_url.format(page=page)
    print("crawling ", url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    doctors = soup.find_all("a", {"class": "doctor-ui"})
    for doctor in doctors[:10]:
        doctor_dict = dict()
        doctor_dict["name"] = (
            doctor.find("h2", {"class": "doctor-ui-name"}).find("span").text.strip()
        )
        doctor_dict["profession"] = []
        specialties = doctor.find_all("span", {"class": "doctor-ui-specialty"})
        for item in specialties:
            doctor_dict["profession"].append(item.text.strip())

        print("crawling", doctor_dict["name"])
        res = requests.get(doctor["href"])
        doc_soup = BeautifulSoup(res.text, "lxml")

        comment_popup = doc_soup.find("a", {"data-role": "comments-popup"})
        doctor_dict["comments"] = []
        if comment_popup:
            comments_url = comment_popup.attrs["href"]
            comments_id = comments_url.split("/")[-1]
            comment_api_url = (
                f"https://nobat.ir/api/public/doctor/comments/all/{comments_id}/0"
            )

            res = requests.get(comment_api_url)
            comments = json.loads(res.text)[0]
            doctor_dict["comments"] = comments
        doctor_list.append(doctor_dict)

with open("output_crawl_requests.json", "w", encoding="utf-8") as f:
    import json

    f.write(json.dumps(doctor_list, ensure_ascii=False, indent=4))
end = time.time()
print("time elapsed:")
print(end - start)
