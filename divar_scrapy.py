import scrapy
from scrapy.crawler import CrawlerProcess

class PythonEventsSpider(scrapy.Spider):
    name = 'pythoneventsspider'

    start_urls = ['https://divar.ir/s/tehran/auto',]
    found_events = []
    download_delay = 1.5

    def parse(self, response):

        xpath="//article[contains(@class,'kt-post-card')]/div[1]"
        for ads in response.xpath(xpath):
            title=ads.xpath('h2/text()').extract_first()
            description=ads.xpath('div/text()').extract_first()
            ads_detail={
                'title':title,
                'description':description 
            }
            self.found_events.append(ads_detail)



        # for event in response.xpath('//ul[contains(@class, "list-recent-events")]/li'):
        #     event_details = dict()
        #     event_details['name'] = event.xpath('h3[@class="event-title"]/a/text()').extract_first()
        #     event_details['location'] = event.xpath('p/span[@class="event-location"]/text()').extract_first()
        #     event_details['time'] = event.xpath('p/time/text()').extract_first()
        #     self.found_events.append(event_details)

if __name__ == "__main__":
    process = CrawlerProcess({ 'LOG_LEVEL': 'ERROR'})
    process.crawl(PythonEventsSpider)
    spider = next(iter(process.crawlers)).spider
    process.start()

    for event in spider.found_events: print(event)