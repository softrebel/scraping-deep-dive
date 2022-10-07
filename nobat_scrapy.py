import scrapy 
from scrapy.crawler import CrawlerProcess

class NobatDoctorSpider(scrapy.Spider):
    name='nobatspider'
    start_urls=['https://nobat.ir/',]
    found_doctors=[]

    def parse(self,response):
        print('url:', response.url)
        print('test')
        for doctors in response.xpath("//a[@class='drList nicehover']"):
            name=doctors.xpath("div[@class='mainDetail']/div[contains(@class,'drName')]/text()").extract_first().strip()
            profession=doctors.xpath("div[@class='mainDetail']/div[contains(@class,'drSpecialty')]/h3/text()").extract_first().strip()
            self.found_doctors.append(dict(name=name,professions=profession))




if __name__=='__main__':
    process=CrawlerProcess({'LOG_LEVEL':'DEBUG'})
    process.crawl(NobatDoctorSpider)
    spider=next(iter(process.crawlers)).spider
    process.start()

    with open('output_scrapy.json','w',encoding='utf-8') as f:
        import json
        f.write(json.dumps(spider.found_doctors,ensure_ascii=False,indent=4))
