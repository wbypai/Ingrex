#coding=utf-8

from __future__ import unicode_literals
from .packages import requests
import re
import logging
import time
from io import open
from .config import Config

def verify():
    """
    Fetch param v of the ingress api.
    """
    headers = {
    'referer': 'https://www.ingress.com/intel',
    'user-agent': 'Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    }
    flag = 1
    while flag:
        request = requests.get('https://www.ingress.com/jsc/gen_dashboard.js',
            headers=headers, verify=False, proxies=proxies)
        logging.debug('Completed transfers in {:.3f}s'.format(
            request.elapsed.total_seconds()))
        reg = '"([\da-f]{40})"'
        try:
            v = re.search(reg, request.text).group(1)
        except:
            v = 0
        if v:
            flag = 0
        else:
            time.sleep(Config.getint('Option', 'interval'))
    logging.debug('New version detected: ' + v)
    Config.set('Verify', 'v', v)
    Config.write(open('ingrex.ini', 'wb'))
    return True

if __name__ == "__main__":
    pass
else:
    if Config.getboolean('Proxy', 'enable'):
        proxies = {
            'http': Config.get('Proxy', 'http'),
            'https': Config.get('Proxy', 'https')
        }
    else:
        proxies = {}

