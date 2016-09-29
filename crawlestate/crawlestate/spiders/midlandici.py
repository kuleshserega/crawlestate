# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import scrapy

from crawlestate.items import MidlandiciItem


class MidlandiciSpider(scrapy.Spider):
    name = "midlandici"
    allowed_domains = ["midlandici.com.hk"]

    START_URL = 'http://www.midlandici.com.hk/ics/' \
        'index.jsp?app=c_tx&env=&lang=en'

    PROPERTY_LIST_URL = 'http://www.midlandici.com.hk/ics/apps/' \
        'transaction2015/c/ajax_controller.jsp?action=search_tx&' \
        'url=ajax_result_table.jsp&buy_sell=%s&by_ft=%s&min_sell=0&' \
        'max_sell=9999999999990000&min_rent=0&max_rent=100009990000&' \
        'min_ft_sell=0&max_ft_sell=999999999999&min_ft_rent=0&' \
        'max_ft_rent=999999999999&dist_id=%s&min_area=0&'\
        'max_area=999999&date_from=%s&date_to=%s&name=&' \
        'offset=%d&num_tx_per_page=20&order_by=post_date&ordering=desc&' \
        'lang=en'

    def __init__(
            self, search_district=None,
            start_date=None, end_date=None,
            *args, **kwargs):
        super(MidlandiciSpider, self).__init__(*args, **kwargs)
        self.search_district = search_district
        self.start_date = start_date
        if not self.start_date:
            self.start_date = (
                datetime.now() - timedelta(days=365)).strftime("%d-%m-%Y")

        self.end_date = end_date
        if not self.end_date:
            self.end_date = datetime.now().strftime("%d-%m-%Y")

    def start_requests(self):
        yield scrapy.Request(self.START_URL)

    def parse(self, response):
        districts_info_path = '//select[@id="district_select"]/optgroup' \
            '/div/option|//select[@id="district_select"]/optgroup/option'
        sel = response.xpath(districts_info_path)

        self.dlist = {}
        for district in sel:
            print district
            dname = district.xpath('text()').extract()[0]
            did = district.xpath('@value').extract()[0]
            self.dlist[dname.strip()] = did

        if self.search_district:
            district_id = self.dlist[self.search_district]
            self.dlist = {}
            self.dlist[self.search_district] = district_id

        url_rent_list, url_sell_list = self._get_url_lists(self.dlist)

        for url_rent in url_rent_list:
            yield scrapy.Request(
                url_rent, self._get_property_items, meta={'current_page': 0})

        for url_sell in url_sell_list:
            yield scrapy.Request(
                url_sell, self._get_property_items, meta={'current_page': 0})

    def _get_url_lists(self, districts, offset=1):
        url_rent_list = []
        url_sell_list = []
        for district_id in districts.itervalues():
            search_rent_params = (
                'N', 'Y', district_id, self.start_date, self.end_date, offset)
            search_sell_params = (
                'Y', 'N', district_id, self.start_date, self.end_date, offset)

            url_rent_list.append(self.PROPERTY_LIST_URL % search_rent_params)
            url_sell_list.append(self.PROPERTY_LIST_URL % search_sell_params)

        return url_rent_list, url_sell_list

    def _get_property_items(self, response):
        item = MidlandiciItem()

        sel = response.xpath('//tr[contains(@class, "record_row")]')

        repls = {'\r': '', '\t': ''}
        for record in sel:
            date = record.xpath('td[2]/text()').extract()[0]
            district = record.xpath('td[3]/div/text()').extract()[0]
            buildling = record.xpath('td[4]/a/text()').extract()[0]
            size = record.xpath('td[5]/text()').extract()[0]
            ft_price = record.xpath('td[6]/text()').extract()[0]
            op_type = record.xpath('td[7]/span/text()').extract()[0]
            price = record.xpath('td[7]/text()').extract()[0]
            data_source = record.xpath('td[8]/text()').extract()[0]

            for k, v in repls.iteritems():
                date = date.replace(k, v)
                district = district.replace(k, v)
                buildling = buildling.replace(k, v)
                size = size.replace(k, v)
                ft_price = ft_price.replace(k, v)
                op_type = op_type.replace(k, v)
                price = price.replace(k, v)
                data_source = data_source.replace(k, v)

            item['date'] = date.strip()
            item['location'] = district.strip()
            item['buildling'] = buildling.strip()
            item['size'] = size.strip()
            item['ft_price'] = ft_price.strip()
            item['op_type'] = op_type.strip()
            item['price'] = price.strip()
            item['data_source'] = data_source.strip()

            yield item

        current_page = response.meta['current_page']

        num_records = response.xpath(
            '//div[@id="result_pagination"]/@data-num-record').extract()
        if num_records:
            results_count = int(num_records[0])
            if results_count > current_page*20:
                response.meta['current_page'] += 1
                offset = response.meta['current_page']*20 + 1
                url_rent_list, url_sell_list = self._get_url_lists(
                    self.dlist, offset)
                for url_rent in url_rent_list:
                    yield scrapy.Request(
                        url_rent,
                        self._get_property_items,
                        meta=response.meta)

                for url_sell in url_sell_list:
                    yield scrapy.Request(
                        url_sell,
                        self._get_property_items,
                        meta=response.meta)
