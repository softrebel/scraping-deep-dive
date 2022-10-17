import scrapy
from scrapy.crawler import CrawlerProcess
import os

os.chdir(os.path.dirname(__file__))


class NobatDoctorSpider(scrapy.Spider):
    name = 'nobatspider'
    start_urls = ['https://nobat.ir/find/city-1/c-7/page-1', ]
    url_format = 'https://nobat.ir/find/city-1/c-7/page-{page}'
    found_doctors = []
    doctor_url = 'https://nobat.ir{url}'

    def parse(self, response):
        print('url:', response.url)
        page = int(response.url.split('page-')[-1])
        print('test')
        for doctors in response.xpath("//a[@class='drList nicehover']"):
            name = doctors.xpath(
                "div[@class='mainDetail']/div[contains(@class,'drName')]/text()").extract_first().strip()
            profession = doctors.xpath(
                "div[@class='mainDetail']/div[contains(@class,'drSpecialty')]/h3/text()").extract_first().strip()
            self.found_doctors.append(dict(name=name, profession=profession))
            item = dict(name=name, profession=profession)
            yield scrapy.Request(self.doctor_url.format(url=doctors.attrib['href']), callback=self.parse_doctor_page, meta={'item': item})
        last = int(response.xpath(
            "//div[@class='paging']/a[last()]/text()").extract_first())
        if page < last:
            yield scrapy.Request(self.url_format.format(page=page+1), callback=self.parse)

    def parse_doctor_page(self, response):
        print('url', response.url)
        extra = []
        extra_field_xpath = "//li[@class='list-inline-item']/span/text()"
        for field in response.xpath(extra_field_xpath):
            extra.append(field.extract().strip())
        response.request.meta['item']['extra'] = extra

        return response.request.meta['item']


if __name__ == '__main__':
    process = CrawlerProcess({
        'LOG_LEVEL': 'DEBUG',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output_crawl_scrapy.json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'CONCURRENT_REQUESTS': 100,
    })
    process.crawl(NobatDoctorSpider)
    spider = next(iter(process.crawlers)).spider
    process.start()

    # with open('output_scrapy_crawl.json', 'w', encoding='utf-8') as f:
    #     import json
    #     f.write(json.dumps(spider.found_doctors, ensure_ascii=False, indent=4))
