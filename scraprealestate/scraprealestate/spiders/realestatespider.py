import scrapy
from random import sample
from scrapy.http import HtmlResponse
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options


# How many pages are for each domanins? (get into ramdonly)
# There are 2 different real estates:
#       - Argenprop --> por pag muestra 20 / (250) 14 paginas a consultar
#       - Zonaprop --> por pag muestra 20 / (250) 14 paginas a consultar


class ArgenpropSpider(scrapy.Spider):
    name = "argenprop_spider"
    allowed_domains = ["www.argenprop.com"]
    start_urls = ["https://www.argenprop.com/departamentos/venta/rosario-santa-fe"]
    pages_to_scrape = 13

    def parse(self, response):
        estates = response.css('div.listing__item')
        # amount_pages = response.css('li.pagination__page a::text').getall()[-1]
        # sample(range(amount_pages), 9)

        for estate in estates:
            price = estate.css('.card__monetary-values .card__price ::text').getall()

            yield {
                "price":        price[1] + str.strip(price[2]),
                "url":          estate.css('a').attrib['href']
            }

            # relative_estate = estate.css('a').attrib['href']

            # if relative_estate is not None:
            #     real_estate_url = 'https://www.argenprop.com' + relative_estate
            #     yield response.follow(real_estate_url, callback=self.parse_real_estate_page)

        if self.pages_to_scrape != 0:
            next_page = response.css('li.pagination__page-next.pagination__page a::attr(href)').get()
            next_page_url = 'https://www.argenprop.com' + next_page
            self.pages_to_scrape -=1
            yield response.follow(next_page_url, callback=self.parse)

    def parse_real_estate_page(self, response):
        address = response.css("div.location-container h2::text").get()
        zone_location = response.css("div.location-container p::text").get()
        section_characteristics = response.xpath("//ul[@id='section-caracteristicas']/li")
        sections_properties = response.css("ul.property-features.collapse")


class ZonapropSpider(scrapy.Spider):
    name = "zonaprop_spider"
    allowed_domains = ["www.zonaprop.com.ar"]
    start_urls = ["https://www.zonaprop.com.ar/departamentos-venta-rosario.html"]

    def __init__(self, *args, **kwargs):
        super(ZonapropSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = uc.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        selenium_response = HtmlResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
        cards_container = selenium_response.css(".CardContainer-sc-1tt2vbg-5.fvuHxG")
        self.logger.info(f"ACA: {cards_container}")
        # for card in cards_container:
        #     # price_container = card.find_element(by=By.CSS_SELECTOR, value=".PriceContainer-sc-12dh9kl-2.ePWLec")
        #     # address_location = card.find_element(by=By.CSS_SELECTOR, value=".LocationBlock-sc-ge2uzh-1.cVCbkm").text.split("\n")

        #     yield {
        #         'url'       : card.css('a').attrib['href']
        #         # 'address'   : address_location[0],
        #         # 'location'  : address_location[1],
        #         # 'price'     : price_container.find_element(by=By.CSS_SELECTOR, value=".Price-sc-12dh9kl-3.geYYII").text
        #     }

    #         # relative_estate = estate.css('a').attrib['href']

    #         # if relative_estate is not None:
    #         #     real_estate_url = 'https://www.argenprop.com' + relative_estate
    #         #     yield response.follow(real_estate_url, callback=self.parse_real_estate_page)

    #     next_page = response.css('li.pagination__page-next.pagination__page a::attr(href)').get()

    #     if next_page is not None:
    #         next_page_url = 'https://www.argenprop.com' + next_page
    #         yield response.follow(next_page_url, callback=self.parse)

    # def parse_real_estate_page(self, response):
    #     pass
