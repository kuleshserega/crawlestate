# -*- coding: utf-8 -*-
import re
import random

import scrapy

from crawlestate.items import CentdataItem
from crawlestate.settings import USER_AGENT_LIST


class CentadataSpider(scrapy.Spider):
    name = "centadata"
    allowed_domains = ["centadata.com"]
    city_code = None
    city_list = ['HK', 'KL', 'NE', 'NW']

    START_URL = 'http://www1.centadata.com/' \
        'epaddresssearch1.aspx?type=district16&code=%s'

    AREA_LINK = 'http://www1.centadata.com/epaddresssearch1.aspx' \
        '?type=%s&code=%s&page=%s'

    APARTMENTS_URL = 'http://www1.centadata.com/eptest.aspx?' \
        'type=%s&code=%s&info=%s&page=%s'

    def __init__(self, city_code=None, *args, **kwargs):
        super(CentadataSpider, self).__init__(*args, **kwargs)
        self.city_code = city_code

    def start_requests(self):
        if self.city_code:
            url = self.START_URL % self.city_code
            yield scrapy.Request(
                url, headers=self._get_headers(), meta={'city': code})
        else:
            for code in self.city_list:
                url = self.START_URL % code
                yield scrapy.Request(
                    url, headers=self._get_headers(), meta={'city': code})

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
                district = area.xpath(
                    'tr/td[contains(@class, "tdreg1cname")]/span/text()').extract()
                response.meta['district'] = ''
                if district:
                    response.meta['district'] = district[0]
                response.meta['type'] = p[0]
                response.meta['code'] = p[1]
                response.meta['page_number'] = 0
                yield scrapy.Request(
                    area_link, self._get_area_table,
                    meta=response.meta,
                    headers=self._get_headers())

    def _get_area_table(self, response):
        item = CentdataItem()

        sel = response.xpath('//table[contains(@class, "tbscp1")]/tr')

        if sel:
            for prop in sel:
                ct_dstrct = \
                    response.meta['city'] + ', ' + response.meta['district'] + ', '
                item['location'] = ct_dstrct + prop.xpath(
                    'td[contains(@class, "tdscp1addr")]/text()').extract()[0]

                ba_tmpl = 'td[contains(@class, "tdscp1bldgage")]/text()'
                item['building_age'] = prop.xpath(ba_tmpl).extract()[0]

                nu_tmpl = 'td[contains(@class, "tdscp1unitcnt")]/text()'
                item['number_of_units'] = prop.xpath(nu_tmpl).extract()[0]

                item['building_type'] = prop.xpath(
                    'td[contains(@class, "tdscp1type")]/text()').extract()[0]

                aparams = prop.xpath('@onclick').extract()
                if aparams:
                    regex = re.compile(r'javascript:jsfreloadthis4(.*);')
                    p = regex.match(
                        aparams[0]).group(1).replace('\'', '')[1:-1].split(',')
                    apartmens_params = (p[0], p[1], p[2], p[3])
                    url = self.APARTMENTS_URL % apartmens_params
                    yield scrapy.Request(
                        url, self._get_apartmens, meta={'item': item},
                        headers=self._get_headers())

            next_exist = sel.xpath('//a[contains(text(), "Next Page")]')

            if next_exist:
                response.meta['page_number'] += 1
                url = self.AREA_LINK % (
                    response.meta['type'],
                    response.meta['code'],
                    response.meta['page_number'])
                yield scrapy.Request(
                    url, self._get_area_table, meta=response.meta,
                    headers=self._get_headers())

    def _replace_non_numeric(self, repl_str):
        res = re.sub("[^0-9]", "", repl_str)
        if not res:
            return 0

        return re.sub("[^0-9]", "", repl_str)

    def _get_user_agent(self):
        return random.choice(USER_AGENT_LIST)

    def _get_headers(self):
        return {'User-Agent': self._get_user_agent()}

    def _get_apartmens(self, response):
        item = response.meta['item']

        sel = response.xpath(
            '//div[contains(@class, "tabbertab")][1]/table/tr/td/table/tr')
        if sel:
            for prop in sel:
                addr_params = prop.xpath(
                    'td[contains(@class, "tdtr1addr")]/u/text()').extract()
                if addr_params:
                    item['unit_floor'] = ' '.join(addr_params)

                na_tmpl = 'td[contains(@class, "tdtr1area")]/text()'
                net_area = prop.xpath(na_tmpl).extract()
                if net_area:
                    item['net_area'] = net_area[0]

                np_tmpl = 'td[contains(@class, "tdtr1uprice")]/text()'
                net_price = prop.xpath(np_tmpl).extract()
                if net_price:
                    item['net_price'] = net_price[0]

                item['net_per_foot'] = None
                if net_area and net_price:
                    net_price_numb = int(
                        self._replace_non_numeric(item['net_price']))
                    net_area_numb = int(
                        self._replace_non_numeric(item['net_area']))
                    if net_price_numb and net_area_numb:
                        item['net_per_foot'] = net_price_numb/net_area_numb

                ga_tmpl = 'td[contains(@class, "tdtr1area")]/text()'
                gross_area = prop.xpath(ga_tmpl).extract()
                if gross_area:
                    item['gross_area'] = gross_area[1]

                gp_tmpl = 'td[contains(@class, "tdtr1Guprice")]/text()'
                gross_price = prop.xpath(gp_tmpl).extract()
                if gross_price:
                    item['gross_price'] = gross_price[0]

                item['gross_per_foot'] = None
                if gross_area and gross_price:
                    gross_price_numb = int(
                        self._replace_non_numeric(item['gross_price']))
                    gross_area_numb = int(
                        self._replace_non_numeric(item['gross_area']))
                    if gross_price_numb and gross_area_numb:
                        item['gross_per_foot'] = \
                            gross_price_numb/gross_area_numb

                yield item
