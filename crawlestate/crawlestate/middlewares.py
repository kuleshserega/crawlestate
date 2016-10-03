import base64
import random

PROXY_LIST = [
    # "http://45.32.235.247:3128",
    # "http://223.16.231.135:8080",
    "http://52.43.200.172:1080",
    "http://202.155.210.2:8080",
    # "http://178.22.148.122:3129",
    # "http://124.244.157.209:80",
    # "http://58.176.46.248:80",
]


class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] = self._get_proxy()
        print 'PROXY:', request.meta['proxy']

        # Use the following lines if your proxy requires authentication
        proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        encoded_user_pass = base64.encodestring(proxy_user_pass)
        # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

    def _get_proxy(self):
        return random.choice(PROXY_LIST)
