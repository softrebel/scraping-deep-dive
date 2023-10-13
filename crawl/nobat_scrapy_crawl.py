import scrapy
from scrapy.crawler import CrawlerProcess
import os
import time

start = time.time()

os.chdir(os.path.dirname(__file__))
LAST_PAGE = 5


class NobatDoctorSpider(scrapy.Spider):
    name = "nobatspider"
    start_urls = [
        "https://nobat.ir/find/city-1/c-7/page-1",
    ]
    url_format = "https://nobat.ir/find/city-1/c-7/page-{page}"

    def parse(self, response):
        print("url:", response.url)
        if "page-" not in response.url:
            page = 1
        else:
            page = int(response.url.split("page-")[-1])
        print("test")
        for doctors in response.xpath("//a[@class='doctor-ui']"):
            name = doctors.xpath("div/div/h2/span/text()").extract_first().strip()
            professions = []
            specialties = doctors.xpath(
                'div/div/span[@class="doctor-ui-specialty"]/text()'
            )
            for item in specialties:
                professions.append(item.extract().strip())
            item = dict(name=name, professions=professions)
            yield scrapy.Request(
                doctors.attrib["href"],
                callback=self.parse_doctor_page,
                meta={"item": item},
            )

        if page <= LAST_PAGE:
            yield scrapy.Request(
                self.url_format.format(page=page + 1), callback=self.parse
            )

    def parse_doctor_page(self, response):
        print("url", response.url)

        comment_popup = response.xpath("//a[@data-role='comments-popup']")
        if not comment_popup or len(comment_popup) == 0:
            response.request.meta["item"]["comments"] = []
            yield response.request.meta["item"]

        comments_url = comment_popup.attrib["href"]
        comments_id = comments_url.split("/")[-1]
        comment_api_url = (
            f"https://nobat.ir/api/public/doctor/comments/all/{comments_id}/0"
        )
        yield scrapy.Request(
            comment_api_url,
            callback=self.parse_doctor_comment_page,
            meta={"item": response.request.meta["item"]},
        )

    def parse_doctor_comment_page(self, response):
        import json

        comments = json.loads(response.text)[0]
        response.request.meta["item"]["comments"] = comments
        return response.request.meta["item"]


if __name__ == "__main__":
    process = CrawlerProcess(
        {
            "LOG_LEVEL": "DEBUG",
            "FEED_FORMAT": "json",
            "FEED_URI": "result.json",
            "FEED_EXPORT_ENCODING": "utf-8",
            "CONCURRENT_REQUESTS": 100,
        }
    )
    process.crawl(NobatDoctorSpider)
    spider = next(iter(process.crawlers)).spider
    process.start()

    end = time.time()
    print("time elapsed:")
    print(end - start)
