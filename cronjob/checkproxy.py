import urllib2
import requests


def check_proxies(url):
    proxy_handler = urllib2.ProxyHandler(
        {'http': 'https://199.200.57.231:27999'})
    opener = urllib2.build_opener(
        proxy_handler, urllib2.HTTPHandler(debuglevel=1))
    urllib2.install_opener(opener)

    try:
        response = opener.open(url, timeout=30)
        return response.read()
    except:
        print "Can't connect with proxy"

    requests.get(
        'https://google.com',
        proxies={'https': 'https://199.200.57.130:27999'},
        timeout=15)


def test():
    url = 'https://google.com'
    print fetch(url)
