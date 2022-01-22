import scrapy
from scrapy.crawler import CrawlerProcess


class MainSpider(scrapy.Spider):
    name = 'main'

    def start_requests(self):
        yield scrapy.Request('https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky?psize=120&sort=pasc')

    def parse(self, response, **kwargs):
        products = response.css('li.product-grid__item')
        for item in products:
            yield {
                'title': item.css('p.product-card__name::text').get(),
                'meta': item.css('p.product-card__meta::text').get(),
                'price': item.css('p.product-card__price::text').get()
            }

        for x in range(2, 25):
            yield (scrapy.Request(
                f'https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky?pg={x}&psize=120&sort=pasc',
                callback=self.parse))


process = CrawlerProcess(settings={
    'FEED_URI': 'main.csv',
    'FEED_FORMAT': 'csv'
})

process.crawl(MainSpider)
process.start()
