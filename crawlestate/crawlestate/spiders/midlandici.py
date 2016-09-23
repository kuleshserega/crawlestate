# -*- coding: utf-8 -*-
import scrapy


class MidlandiciSpider(scrapy.Spider):
    name = "midlandici"
    allowed_domains = ["midlandici.com.hk"]

    START_URL = """http://www.midlandici.com.hk/ics/apps/transaction2015/c/
        ajax_controller.jsp?action=search_tx&url=ajax_result_table.jsp&
        buy_sell=N&by_ft=N&min_sell=0&max_sell=9999999999990000&min_rent=0&
        max_rent=100009990000&min_ft_sell=0&max_ft_sell=999999999999&
        min_ft_rent=0&max_ft_rent=999999999999&dist_id=15986&min_area=0&
        max_area=999999&date_from=23%2F09%2F2015&date_to=23%2F09%2F2016&name=&
        offset=1&num_tx_per_page=20&order_by=post_date&ordering=desc&lang=en"""

    def __init__(self, *args, **kwargs):
        super(MidlandiciSpider, self).__init__(*args, **kwargs)
        self.headers = {
            'Cache-Control': 'no-cache',
            'Postman-Token': '5d6d4a39-2618-36cc-56f4-e23e1211da48'
            # 'Accept': "*/*",
            # 'Accept-Encoding': "gzip, deflate",
            # 'Accept-Language': "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            # 'Connection': "keep-alive",
            # 'Origin': "https://www.arbetsformedlingen.se",
            # 'Referer': "https://www.arbetsformedlingen.se/4.7d307efe11ed997680b800058064.html",
            # 'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0",
            # 'X-Requested-With': 'XMLHttpRequest'
            # 'Upgrade-Insecure-Requests': "1",
            # 'Content-Type': "application/x-www-form-urlencoded",
        }

    def start_requests(self):
        yield scrapy.Request(self.START_URL, headers=self.headers)

    def parse(self, response):
        print '::::::::::::::;'
        print response.body_as_unicode()
