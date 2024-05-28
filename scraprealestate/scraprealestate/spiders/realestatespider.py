import scrapy
from scrapy.crawler import CrawlerProcess


#RealestatespiderSpider
class RealestaterentspiderSpider(scrapy.Spider):
    name = "realestaterentspider"
    allowed_domains = ["www.argenprop.com"]
    start_urls = ["https://www.argenprop.com/departamentos/alquiler/rosario-santa-fe"]

    def parse(self, response):
        estates = response.css('div.listing__item')

        for estate in estates:
            price = estate.css('.card__monetary-values .card__price ::text').getall()

            yield{
                "name":         estate.css('div h2::text').get(),
                "price":        price[1] + str.strip(price[2]),
                "expenses":     estate.css('.card__expenses::attr(title)').get(),
                "url":          estate.css('a').attrib['href']
            }

            # relative_estate = estate.css('a').attrib['href']

            # if relative_estate is not None:
            #     real_estate_url = 'https://www.argenprop.com' + relative_estate
            #     yield response.follow(real_estate_url, callback=self.parse_real_estate_page)

        next_page = response.css('li.pagination__page-next.pagination__page a::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://www.argenprop.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_real_estate_page(self, response):
        pass
