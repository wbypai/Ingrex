import requests
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
    
    def fetch_version(self):
        """
        Fetch the version of the ingress api.
        """
        headers = {
        'referer': 'https://www.ingress.com/intel',
        'user-agent': ('Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'),
        }
        request = requests.get('https://www.ingress.com/jsc/gen_dashboard.js', headers=headers, verify=False)
        offset = request.text.index('b.v="') + 5
        self.config['Verify']['v'] = request.text[offset:offset + 40]