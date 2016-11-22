import base64
import random
import os
import sys

sys.path.append(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from helpers import get_proxy_from_db


class ProxyMiddleware(object):
    PROXY_LIST = []

    # overwrite process request
    def process_request(self, request, spider):
        proxy_list = get_proxy_from_db(proxy_status='Works')
        for k, proxy in proxy_list.iteritems():
            self.PROXY_LIST.append(proxy)

        # Set the location of the proxy
        proxy = self._get_proxy()
        if proxy:
            request.meta['proxy'] = self._get_proxy()
            print request.meta['proxy']

        # Use the following lines if your proxy requires authentication
        # proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        # encoded_user_pass = base64.encodestring(proxy_user_pass)
        # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

    def _get_proxy(self):
        return random.choice(self.PROXY_LIST)
