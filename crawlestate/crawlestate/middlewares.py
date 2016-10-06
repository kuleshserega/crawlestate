import base64
import random

PROXY_LIST = [
    "https://199.200.58.247:27999",
    "https://38.72.72.12:27999",
    "https://38.72.81.186:27999",
    "https://38.72.74.165:27999",
    "https://38.72.89.187:27999",
    # "http://58.176.46.248:80",
    # "http://146.0.73.14:80",
    # "http://45.32.235.247:3128",
    # "http://223.16.231.135:8080",
    # "http://128.199.88.117:8080",
    # "http://202.155.210.2:8080",
    # "http://122.117.79.36:8080",
    # "http://178.22.148.122:3129",
    # "http://124.244.157.209:80",
    # "socks5://128.199.88.117:8080",
    # "socks5://52.43.200.172:1080",
    # "socks5://61.238.32.69:1080",
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
