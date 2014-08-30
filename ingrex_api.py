import requests
import json
import time
import logging
from ingrex_config import config

class Intel(object):
    """ 
    This class include all the api in https://www.ingress.com/intel.
    """
    
    def __init__(self):
        """
        Initialize with the configs.
        Generate E6 forms of Lat/Lng which used in the api's payload.
        xxE6 = int(xx * 10E6) = int(xx * 1000000)
        """
        self.config = config()
        self.config['Bound']['maxLatE6'] = str(int(float(
            self.config['Bound']['maxlat']) * 1000000))
        self.config['Bound']['minLatE6'] = str(int(float(
            self.config['Bound']['minlat']) * 1000000))
        self.config['Bound']['maxLngE6'] = str(int(float(
            self.config['Bound']['maxlng']) * 1000000))
        self.config['Bound']['minLngE6'] = str(int(float(
            self.config['Bound']['minlng']) * 1000000))
        self.config['Local']['LatE6'] = str(int(float(
            self.config['Local']['lat']) * 1000000))
        self.config['Local']['LngE6'] = str(int(float(
            self.config['Local']['lng']) * 1000000))
    
    def fetch_player(self):
        import re
        """
        Fetch player infomations.
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
            cookies=cookies, verify=False)
        reg = 'PLAYER = ({.*});'
        jsondata = json.loads(re.search(reg, request.text).group(1))
        return jsondata
    
    def _request(self, url, params={}):
        """
        Raw request with auto-retry and connection check function
        """
        
        headers = {
        'referer': 'https://www.ingress.com/intel',
        'user-agent': ('Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'),
        'content-type': 'application/json; charset=UTF-8',
        'x-csrftoken': self.config['Token']['CSRFTOKEN']
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
        params['v'] = self.config['Verify']['v']
        params['b'] = self.config['Verify']['b']
        params['c'] = self.config['Verify']['c']
        payload = json.dumps(params)
        i = 0
        while i < 3:
            try:
                request = requests.post(url, data=payload, headers=headers,
                    cookies=cookies, verify=False)
                request.raise_for_status()
                logging.debug('Request: ' + payload)
                logging.debug('Response: ' + request.text)
                break
            except ConnectionError:
                i += 1
                time.sleep(1)
        if i == 3:
            self._check_connection()
        return request.text
    
    def _check_connection(self):
        """
        Check if the connection problem is caused by DNS failure or Auth error.
        Ingress Intel API interface (https://www.ingress.com/r/*) will refused
        connection if authentication failed, but you can still connect to the 
        Intel itself (https://www.ingress.com/r/intel).
        """
        
        url = 'https://www.ingress.com/intel'
        headers = {
        'referer': 'https://www.ingress.com/intel',
        'user-agent': ('Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'),
        }
        try:
            request = requests.get(url, headers=headers, verify=False)
        except:
            logging.warning('Connection Error')
            raise Exception('Connection Error')
        else:
            logging.warning('Authentication Failed')
            raise Exception('Authentication Failed')
    
    def fetch_msg(
        self, ascendingTimestampOrder=False, minTimestampMs=-1,
        maxTimestampMs=-1, tab='all'):
        """
        fetch message from Ingress COMM.
        response dictionary like this: {"success":[messageObj-1, messageObj-2, ...]}
        or {"error":"errorMessage"}
        
        ascendingTimestampOrder:
        - True: sort messageObject by ascending timestamp order
        - False: sort messageObject by descending timestamp order
        
        minTimestampMs,maxTimestampMs:
        - UTC Timestamp in milliseconds.
        
        tab:
        - 'all', 'faction', 'alerts' for different tab.
        """
        
        url = 'https://www.ingress.com/r/getPlexts'
        payload={
        'maxLatE6': int(self.config['Bound']['maxLatE6']),
        'minLatE6': int(self.config['Bound']['minLatE6']),
        'maxLngE6': int(self.config['Bound']['maxLngE6']),
        'minLngE6': int(self.config['Bound']['minLngE6']),
        'maxTimestampMs': maxTimestampMs,
        'minTimestampMs': minTimestampMs,
        'tab': tab
        }
        if ascendingTimestampOrder:
            payload['ascendingTimestampOrder'] = True
        jsondata = json.loads(self._request(url, params=payload))
        return jsondata
    
    def fetch_map(self, tileKeys=[]):
        """
        fetch game entities from Ingress map.
        response dictionary like this:
        {"result":{"map":{"tileKey-1":{x}, "tileKey-2":{x}, ...}}}
        or {"error":"errorMessage"}
        
        tileKeys is a list with less than 5 tileKey.
        tileKey: "zoomLevel_latTile_lngTile_minLevel_maxLevel_100"
        zoomLevel = 17, minLevel = 0, maxLevel = 8 is prefered.
        
        I guess if you try to get all the portal using zoomLevel = 1,
        you will be baned in a moment.
        """
        
        url = 'https://www.ingress.com/r/getEntities'
        payload={
        'tileKeys': tileKeys
        }
        jsondata = json.loads(self._request(url, params=payload))
        return jsondata
    
    def fetch_portal(self, guid):
        """
        fetch portal details from Ingress.
        response a dictionary with keys like "level", "team" and so on.
        """
        
        url = 'https://www.ingress.com/r/getPortalDetails'
        payload={
        'guid': guid
        }
        jsondata = json.loads(self._request(url, params=payload))
        return jsondata
    
    def fetch_score(self):
        """
        fetch the globe score of RESISTANCE and ENLIGHTENED.
        response dictionary like: ["ENLIGHTENED score","RESISTANCE score"].
        """
        
        url = 'https://www.ingress.com/r/getGameScore'
        payload={
        }
        jsondata = json.loads(self._request(url, params=payload))
        return jsondata
    
    def fetch_artifacts(self):
        """
        fetch the artifacts details.
        response dictionary like:
        {"artifacts":[{
            "artifactId": "x"
            "targetInfos": [x],
            "fragmentInfos": [x],
        }]}
        """
        
        url = 'https://www.ingress.com/r/artifacts'
        payload={
        }
        jsondata = json.loads(self._request(url, params=payload))
        return jsondata
    
    def send_msg(self, msg, tab='all'):
        """
        send a message to Ingress COMM.
        response dictionary like: {"result":"success"}.
        
        tab:
        - 'all', 'faction', 'alerts' for different tab.
        """
        
        url = 'https://www.ingress.com/r/sendPlext'
        payload={
        'message': msg,
        'latE6': int(self.config['Local']['LatE6']),
        'lngE6': int(self.config['Local']['LngE6']),
        'tab': tab
        }
        jsondata = json.loads(self._request(url, params=payload))
        return jsondata
    
    def send_invite(self, address):
        """
        send a recruit to an email address.
        response json like: {"error":"NO_INVITES_AVAILABLE"}.
        """
        
        url = 'https://www.ingress.com/r/sendInviteEmail'
        payload={
        'inviteeEmailAddress': address
        }
        jsondata = json.loads(self._request(url, params=payload))
        return jsondata
    
    def redeem_code(self, passcode):
        """
        redeem a passcode in Ingress.
        response json like: {"error":"Invalid passcode."}.
        """
        
        url = 'https://www.ingress.com/r/redeemReward'
        payload={
        'passcode': passcode
        }
        jsondata = json.loads(self._request(url, params=payload))
        return jsondata

