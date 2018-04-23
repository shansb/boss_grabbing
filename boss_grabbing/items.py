# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BossGrabbingItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    area = scrapy.Field()
    size = scrapy.Field()
    finance = scrapy.Field()
    description = scrapy.Field()
    addresses = scrapy.Field()
    pass
