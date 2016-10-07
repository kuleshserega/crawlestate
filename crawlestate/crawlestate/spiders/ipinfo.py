# -*- coding: utf-8 -*-
import scrapy


class IpinfoSpider(scrapy.Spider):
    name = "ipinfo"
    allowed_domains = ["ipinfo.io"]
    start_urls = (
        'http://www.ipinfo.io/',
    )

    def parse(self, response):
        print 'RESPONSE:', response.body_as_unicode()
