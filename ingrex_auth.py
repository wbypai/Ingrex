import requests
import re
from ingrex_config import config

class Auth(object):
    """
    This class include api about the oauth.
    Login with the email and password, and fetch the sacsid, csrftoken and vers.
    """
    
    def __init__(self):
        """
        Initialize with the configs.
        """
        self.config = config()
        if self.config['Proxy']['enable'] == 'True':
            self.proxies = {
                'http': self.config['Proxy']['http'],
                'https': self.config['Proxy']['https']
            }
        else:
            self.proxies = {}
    
    def fetch_v(self):
        """
        Fetch param v of the ingress api.
        """
        headers = {
        'referer': 'https://www.ingress.com/intel',
        'user-agent': ('Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'),
        }
        request = requests.get('https://www.ingress.com/jsc/gen_dashboard.js',
            headers=headers, verify=False, proxies=self.proxies)
        reg = '"([\da-f]{40})"'
        v = re.search(reg, request.text).group(1)
        self.config['Verify']['v'] = v
    
    def fetch_b(self):
        """
        Fetch param b of the ingress api.
        """
        headers = {
        'referer': 'https://www.ingress.com/intel',
        'user-agent': ('Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'),
        }
        cookies = {
        'SACSID': self.config['Token']['sacsid'],
        'csrftoken': self.config['Token']['csrftoken'],
        'GOOGAPPUID': self.config['Verify']['appuid'],
        'ingress.intelmap.shflt': self.config['Local']['shflt'],
        'ingress.intelmap.lat': self.config['Local']['lat'],
        'ingress.intelmap.lng': self.config['Local']['lng'],
        'ingress.intelmap.zoom': self.config['Local']['zoom'],
        }
        request = requests.get('https://www.ingress.com/intel', headers=headers,
            cookies=cookies, verify=False, proxies=self.proxies)
        reg = '"(\w{5}-\w{37})"'
        b = re.search(reg, request.text).group(1)
        self.config['Verify']['b'] = b

