# -*- coding: utf-8 -*-
import re

import scrapy

from crawlestate.items import CentdataItem


class CentadataSpider(scrapy.Spider):
    name = "centadata"
    allowed_domains = ["centadata.com"]

    START_URL = 'http://www1.centadata.com/' \
        'epaddresssearch1.aspx?type=district16&code=%s'

    AREA_LINK = 'http://www1.centadata.com/epaddresssearch1.aspx' \
        '?type=%s&code=%s&page=%s'

    def __init__(self, city_code=None, city_area=None, *args, **kwargs):
        super(CentadataSpider, self).__init__(*args, **kwargs)
        self.city_code = city_code
        self.city_area = city_area

    def start_requests(self):
        url = self.START_URL % self.city_code
        yield scrapy.Request(url)

    def parse(self, response):
        sel = response.xpath('//table[contains(@class, "tbreg1")]')

        for area in sel:
            params = area.xpath('tr/@onclick').extract()
            if params:
                regex = re.compile(r'javascript:jsfreloadthis5(.*);')
                p = regex.match(
                    params[0]).group(1).replace('\'', '')[1:-1].split(',')
                link_params = (p[0], p[1], '0')
                area_link = self.AREA_LINK % link_params
                yield scrapy.Request(
                    area_link, self._get_area_table,
                    meta={'type': p[0], 'code': p[1], 'page_number': 0})

    def _get_area_table(self, response):
        item = CentdataItem()

        sel = response.xpath('//table[contains(@class, "tbscp1")]/tr')

        if sel:
            for prop in sel:
                item['location'] = prop.xpath(
                    'td[contains(@class, "tdscp1addr")]/text()').extract()[0]
                item['year_duration'] = None
                item['unit_floor'] = None

                ba_tmpl = 'td[contains(@class, "tdscp1bldgage")]/text()'
                item['building_age'] = prop.xpath(ba_tmpl).extract()[0]

                nu_tmpl = 'td[contains(@class, "tdscp1unitcnt")]/text()'
                item['number_of_units'] = prop.xpath(nu_tmpl).extract()[0]

                item['building_type'] = prop.xpath(
                    'td[contains(@class, "tdscp1type")]/text()').extract()[0]

                gp_tmpl = 'td[contains(@class, "tdscp1Guprice")]/text()'
                item['gross_price'] = prop.xpath(gp_tmpl).extract()[0]

                np_tmpl = 'td[contains(@class, "tdscp1Suprice")]/text()'
                item['net_price'] = prop.xpath(np_tmpl).extract()[0]

                yield item

            next_exist = sel.xpath('//a[contains(text(), "Next Page")]')

            if next_exist:
                response.meta['page_number'] = response.meta['page_number'] + 1
                url = self.AREA_LINK % (
                    response.meta['type'],
                    response.meta['code'],
                    response.meta['page_number'])
                yield scrapy.Request(
                    url, self._get_area_table, meta=response.meta)
