import scrapy
from config import *
from scrapy.crawler import CrawlerProcess


class NobatSpider(scrapy.Spider):
    name = 'scrapyspider'
    start_urls = ['https://nobat.ir/', ]
    found_doctors = []

    def parse(self, response):
        print(response.url)
        for doctor in response.xpath("//a[@class='drList nicehover']"):
            name = doctor.xpath(
                "//div[contains(@class,'drName')]/text()").extract_first().strip()
            profession = doctor.xpath(
                "//div[@class='drSpecialty']/h3/text()").extract_first().strip()
            self.found_doctors.append({
                'name': name,
                'profession': profession
            })


if __name__ == '__main__':
    process = CrawlerProcess({'LOG_LEVEL': 'DEBUG'})
    process.crawl(NobatSpider)
    spider = next(iter(process.crawlers)).spider
    process.start()
    with open(f'test_scrapy.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(spider.found_doctors, ensure_ascii=False, indent=4))
