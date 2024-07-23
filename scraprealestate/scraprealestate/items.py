# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraprealestateItem(scrapy.Item):
    # define the fields for your item here like:
    price               = scrapy.Field()
    acceso_condominio   = scrapy.Field()
    condominio          = scrapy.Field()
    avenida             = scrapy.Field()
    vista_rio           = scrapy.Field()
    parque              = scrapy.Field()
    plaza               = scrapy.Field()
    paseo_comercial     = scrapy.Field()
    barrio              = scrapy.Field()
    dormitorios         = scrapy.Field()
    baños               = scrapy.Field()
    cocheras            = scrapy.Field()
    superficie_total    = scrapy.Field()
    pileta              = scrapy.Field()
    amenities           = scrapy.Field()

    url                 = scrapy.Field()
    address             = scrapy.Field()
    calle_cleaning      = scrapy.Field()
    real_estate_coords  = scrapy.Field()
    description         = scrapy.Field()
