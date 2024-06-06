import scrapy
from random import sample

# How many pages are for each domanins? (get into ramdonly)
# How many real estates we need to save? --> 500 (2:166) (1:167) Choose pages ramdonly
# There are 3 different real estates:
#       - Argenprop --> por pag muestra 20 / (166) 9 paginas a consultar
#       - Zonaprop --> por pag muestra 20 / (166) 9 paginas a consultar
#       - Propia --> por pag muestra 15 / (166) 12 paginas a consultar

# TRY TO SCRAPE INSIDE real_estate_web_scraping.py INSTEAD

ALLOWED_COUNT_DOMAINS_FIRST = 2
ALLOWED_COUNT_DOMAINS_SECOND = 1
REAL_ESTATES_TO_GET = {
    "hundred_sixty_six": [166, ALLOWED_COUNT_DOMAINS_FIRST],
    "hundred_sixty_seven": [167, ALLOWED_COUNT_DOMAINS_SECOND]
}
RANDOM_DOMAIN_ORDER = sample(range(100), ALLOWED_COUNT_DOMAINS_FIRST + ALLOWED_COUNT_DOMAINS_SECOND)



class Realestatesell_agenprop_Spider(scrapy.Spider):
    name = "realestatesell_argenprop_spider"
    allowed_domains = ["www.argenprop.com"]
    start_urls = ["https://www.argenprop.com/departamentos/venta/rosario-santa-fe"]

    def parse(self, response):
        estates = response.css('div.listing__item')
        # amount_pages = response.css('li.pagination__page a::text').getall()[-1]
        # sample(range(amount_pages), 9)

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
