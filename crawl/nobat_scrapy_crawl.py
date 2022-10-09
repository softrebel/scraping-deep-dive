import scrapy 
from scrapy.crawler import CrawlerProcess

class NobatDoctorSpider(scrapy.Spider):
    name='nobatspider'
    start_urls=['https://nobat.ir/find/city-1/c-7/page-1',]
    url_format='https://nobat.ir/find/city-1/c-7/page-{page}'
    found_doctors=[]

    def parse(self,response):
        print('url:', response.url)
        page=int(response.url.split('page-')[-1])
        print('test')
        for doctors in response.xpath("//a[@class='drList nicehover']"):
            name=doctors.xpath("div[@class='mainDetail']/div[contains(@class,'drName')]/text()").extract_first().strip()
            profession=doctors.xpath("div[@class='mainDetail']/div[contains(@class,'drSpecialty')]/h3/text()").extract_first().strip()
            self.found_doctors.append(dict(name=name,profession=profession))
        

        last = int(response.xpath("//div[@class='paging']/a[last()]/text()").extract_first())
        if page < last:
            yield response.follow(self.url_format.format(page=page+1), self.parse)
        





if __name__=='__main__':
    process=CrawlerProcess({'LOG_LEVEL':'DEBUG'})
    process.crawl(NobatDoctorSpider)
    spider=next(iter(process.crawlers)).spider
    process.start()

    with open('output_scrapy_crawl.json','w',encoding='utf-8') as f:
        import json
        f.write(json.dumps(spider.found_doctors,ensure_ascii=False,indent=4))
