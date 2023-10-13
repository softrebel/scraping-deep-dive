import requests
from bs4 import BeautifulSoup
import os
import json

import time


start = time.time()
os.chdir(os.path.dirname(__file__))
base_url = "https://nobat.ir/find/city-1/c-7/page-{page}"
doctor_list = []
doctor_url = "https://nobat.ir{url}"
page = 1
for item in range(1, 6):
    page = item
    url = base_url.format(page=page)
    print("crawling ", url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    doctors = soup.find_all("a", {"class": "doctor-ui"})
    # doctors = []
    for doctor in doctors[:10]:
        doctor_dict = dict()
        doctor_dict["name"] = (
            doctor.find("h2", {"class": "doctor-ui-name"}).find("span").text.strip()
        )
        doctor_dict["profession"] = []
        specialties = doctor.find_all("span", {"class": "doctor-ui-specialty"})
        for item in specialties:
            doctor_dict["profession"].append(item.text.strip())

        # doctor_dict["profession"] = (
        #     doctor.find("div", {"class": "doctor-ui-specialty"})
        #     .find("div", {"class": "drSpecialty"})
        #     .find("h3")
        #     .text.strip()
        # )
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
        # comments_soup = BeautifulSoup(res.text, "lxml")

        # comments = []

        # comments_css = doc_soup.find_all(
        #     "div", {"class": "comments_comment_box__2F_q8"}
        # )
        # for comment in comments_css:
        #     text = comment.select("div > span")
        #     date = comment.select("small")
        #     comments.append(dict(text=text, date=date))
        # # for field in doc_soup.select("li[class=list-inline-item]>span"):
        # #     extra.append(field.text.strip())
        # doctor_dict["comments"] = comments
        # doctor_list.append(doctor_dict)

    # last_soup = soup.find_all('li',{'class':'pagination-item'})
    # last = int(soup.find_all("a", {"class": "pagination-item"})[-1].text.strip())
    # last = int(response.xpath("//div[@class='paging']/a[last()]/text()").extract_first())
    # if page >= last:
    #     break
    # page += 1

with open("output_crawl_requests.json", "w", encoding="utf-8") as f:
    import json

    f.write(json.dumps(doctor_list, ensure_ascii=False, indent=4))
end = time.time()
print("time elapsed:")
print(end - start)
