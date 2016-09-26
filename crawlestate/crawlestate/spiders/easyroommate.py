# -*- coding: utf-8 -*-
import json

import scrapy

from crawlestate.items import EasyroommateItem


class EasyroommateSpider(scrapy.Spider):
    name = "easyroommate"
    allowed_domains = ["easyroommate.com", "maps.googleapis.com"]
    START_URL = 'https://maps.googleapis.com/maps/api/place/' \
        'autocomplete/json?input=%s&types=geocode&' \
        'key=AIzaSyBywB08oedi9vzk-ZzM-3owyKaMnTvHV_k'

    BASE_URL = 'http://www.easyroommate.com'

    LOCATION_URL = 'https://maps.googleapis.com/maps/api/place/' \
        'details/json?placeid=%s&key=AIzaSyBywB08oedi9vzk-ZzM-3owyKaMnTvHV_k'

    SEARCH_URL = 'http://www.easyroommate.com/Search/' \
        'DynamicRoomSearch/GetResultsByRadius'

    def __init__(self, search_address=None, *args, **kwargs):
        super(EasyroommateSpider, self).__init__(*args, **kwargs)
        self.search_address = search_address
        self.frmdata = {
            "jsonFilter": {
                "limit": 20,
                "radius": "40000",
                "pageNumber": 1
            },
            "locationId": "0"
        }
        self.headers = {'content-type': 'application/json'}

    def start_requests(self):
        url = self.START_URL % self.search_address
        yield scrapy.Request(url)

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        place_id = jsonresponse['predictions'][0]['place_id']
        url = self.LOCATION_URL % place_id
        yield scrapy.Request(url, self._get_pages_by_location)

    def _get_pages_by_location(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        if 'result' in jsonresponse:
            location = jsonresponse['result']['geometry']['location']
            self.frmdata["jsonFilter"]["latitude"] = location['lat']
            self.frmdata["jsonFilter"]["longitude"] = location['lng']

            yield scrapy.Request(
                self.SEARCH_URL, self._get_properties, method="POST",
                body=json.dumps(self.frmdata), headers=self.headers)

    def _get_properties(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

        results = jsonresponse['Results']
        for result in results:
            item = EasyroommateItem()
            item['location'] = result['Location']
            item['price'] = result['RentValue']
            item['image_url'] = result['ImageUrl']
            item['description'] = result['Description']

            url = self.BASE_URL + result['ListingUrl']
            yield scrapy.Request(
                url, self._get_about_place, meta={'item': item})

        if jsonresponse['PageNumber'] < jsonresponse['TotalPages']:
            self.frmdata["jsonFilter"]["pageNumber"] = \
                jsonresponse['PageNumber'] + 1
            yield scrapy.Request(
                self.SEARCH_URL, self._get_properties, method="POST",
                body=json.dumps(self.frmdata), headers=self.headers)

    def _get_about_place(self, response):
        item = response.meta['item']
        item['about_the_flatshare'] = ''

        about_place = response.xpath(
            '//div[contains(@class, "detail__row")]/div/ul/li/text()'
        ).extract()
        for about in about_place:
            item['about_the_flatshare'] += about

        who_lives_there = response.xpath(
            '//div[contains(@data-test, "rd-wholivesthere")]/p/text()'
        ).extract()
        if who_lives_there:
            item['who_lives_there'] = who_lives_there[0]

        ideal_flatmates = response.xpath(
            '//div[@data-test="rd-idealflatmate"]/p/text()').extract()
        if ideal_flatmates:
            item['ideal_flatmates'] = ideal_flatmates[0]

        yield item
