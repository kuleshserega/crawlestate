# -*- coding: utf-8 -*-
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


class MidlandiciItem(scrapy.Item):
    date = scrapy.Field()
    location = scrapy.Field()
    buildling = scrapy.Field()
    size = scrapy.Field()
    ft_price = scrapy.Field()
    op_type = scrapy.Field()
    price = scrapy.Field()
    data_source = scrapy.Field()


class EasyroommateItem(scrapy.Item):
    location = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
    about_the_flatshare = scrapy.Field()
    who_lives_there = scrapy.Field()
    ideal_flatmates = scrapy.Field()
    description = scrapy.Field()
