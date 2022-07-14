# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WarsItem(scrapy.Item):
    date = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()

class ProKifItem(scrapy.Item):
    data = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()