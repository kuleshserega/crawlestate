# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CentdataItem(scrapy.Item):
    location = scrapy.Field()
    year_duration = scrapy.Field()
    unit_floor = scrapy.Field()
    building_age = scrapy.Field()
    number_of_units = scrapy.Field()
    building_type = scrapy.Field()
    gross_price = scrapy.Field()
    net_price = scrapy.Field()
