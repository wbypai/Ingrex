#coding=utf-8

from __future__ import unicode_literals
from .packages import requests
import json
import time
import logging
from .config import Config

def fetch(url, params={}):
    """
    Raw request with auto-retry and connection check function
    """
    
    headers = {
    'referer': 'https://www.ingress.com/intel',
    'user-agent': 'Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'content-type': 'application/json; charset=UTF-8',
    'x-csrftoken': Config.get('Token', 'CSRFTOKEN'),
    'x-requested-with': 'XMLHttpRequest',
    }
    cookies = {
    'SACSID': Config.get('Token', 'sacsid'),
    'csrftoken': Config.get('Token', 'csrftoken'),
    'GOOGAPPUID': Config.get('Verify', 'appuid'),
    'ingress.intelmap.shflt': Config.get('Local', 'shflt'),
    'ingress.intelmap.lat': Config.get('Local', 'lat'),
    'ingress.intelmap.lng': Config.get('Local', 'lng'),
    'ingress.intelmap.zoom': Config.get('Local', 'zoom'),
    }
    params['v'] = Config.get('Verify', 'v')
    params['b'] = Config.get('Verify', 'b')
    params['c'] = Config.get('Verify', 'c')
    timeout = Config.getint('Option', 'timeout')
    payload = json.dumps(params)
    flag = 1
    while flag:
        try:
            request = requests.post(url, data=payload, headers=headers,
                cookies=cookies, verify=False, proxies=proxies, timeout=timeout)
            request.raise_for_status()
            response = request.text
            logging.debug('Request: ' + payload)
            logging.debug('Response: ' + response)
            logging.debug('Completed transfers in {:.3f}s'.format(
                request.elapsed.total_seconds()))
            flag = 0
        except Exception as e:
            logging.warning(e)
            flag += 1
            if flag > 3:
                logging.error('Too many Connection Error')
                raise Exception
            time.sleep(1)
    try:
        data = json.loads(response)
    except:
        logging.warning('Invalid JSON fetched')
        data = ''
    try:
        del data['a'], data['b'], data['c']
    except:
        pass
    return data

def fetch_msg(ascendingTimestampOrder=False, minTimestampMs=-1,
    maxTimestampMs=-1, tab='all'):
    """
    fetch message from Ingress COMM.
    response dictionary like this:
    {"success":[messageObj-1, messageObj-2, ...]}
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
    'maxLatE6': maxLatE6,
    'minLatE6': minLatE6,
    'maxLngE6': maxLngE6,
    'minLngE6': minLngE6,
    'maxTimestampMs': maxTimestampMs,
    'minTimestampMs': minTimestampMs,
    'tab': tab
    }
    if ascendingTimestampOrder:
        payload['ascendingTimestampOrder'] = True
    data = fetch(url, params=payload)
    return data

def fetch_map(tileKeys=[]):
    """
    fetch game entities from Ingress map.
    response dictionary like this:
    {"result":{"map":{"tileKey-1":{x}, "tileKey-2":{x}, ...}}}
    or {"error":"errorMessage"}
    
    tileKeys is a list with less than 5 tileKey. tileKey0,1,2,3 don't add 4.
    tileKey: "zoomLevel_latTile_lngTile_minLevel_maxLevel_health"
    zoomLevel = 17, minLevel = 0, maxLevel = 8, health = 100 is prefered.
    
    I guess if you try to get all the portal(L0-L8) using zoomLevel = 1,
    you will be baned in a moment.
    """
    
    url = 'https://www.ingress.com/r/getEntities'
    payload={
    'tileKeys': tileKeys
    }
    data = fetch(url, params=payload)
    return data

def fetch_portal(guid):
    """
    fetch portal details from Ingress.
    response a dictionary with keys like "level", "team" and so on.
    """
    
    url = 'https://www.ingress.com/r/getPortalDetails'
    payload={
    'guid': guid
    }
    data = fetch(url, params=payload)
    return data

def fetch_score():
    """
    fetch the globe score of RESISTANCE and ENLIGHTENED.
    response dictionary like: ["ENLIGHTENED score","RESISTANCE score"].
    """
    
    url = 'https://www.ingress.com/r/getGameScore'
    data = fetch(url)
    return data

def fetch_artifacts():
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
    data = fetch(url)
    return data

def send_msg(msg, tab='all'):
    """
    send a message to Ingress COMM.
    response dictionary like: {"result":"success"}.
    
    tab:
    - 'all', 'faction', 'alerts' for different tab.
    """
    
    url = 'https://www.ingress.com/r/sendPlext'
    payload={
    'message': msg,
    'latE6': LatE6,
    'lngE6': LngE6,
    'tab': tab
    }
    data = fetch(url, params=payload)
    return data

def send_invite(address):
    """
    send a recruit to an email address.
    response json like: {"error":"NO_INVITES_AVAILABLE"}.
    """
    
    url = 'https://www.ingress.com/r/sendInviteEmail'
    payload={
    'inviteeEmailAddress': address
    }
    data = fetch(url, params=payload)
    return data

def redeem_code(passcode):
    """
    redeem a passcode in Ingress.
    response json like:
    {
        "ap":"0",
        "xm":"0",
        "other":[],
        "inventory":[
            {
                "awards":[{"count":1,"level":4}],
                "name":"Power Cube"
            }
        ]
    }
    {"error":"Invalid passcode."}
    {"error":"Passcode already redeemed."}
    """
    
    url = 'https://www.ingress.com/r/redeemReward'
    payload={
    'passcode': passcode
    }
    data = fetch(url, params=payload)
    return data

if __name__ == "__main__":
    pass
else:
    maxLatE6 = int(Config.getfloat('Bound', 'maxlat') * 1000000)
    minLatE6 = int(Config.getfloat('Bound', 'minlat') * 1000000)
    maxLngE6 = int(Config.getfloat('Bound', 'maxlng') * 1000000)
    minLngE6 = int(Config.getfloat('Bound', 'minlng') * 1000000)
    LatE6 = int(Config.getfloat('Local', 'lat') * 1000000)
    LngE6 = int(Config.getfloat('Local', 'lng') * 1000000)
    if Config.getboolean('Proxy', 'enable'):
        proxies = {
            'http': Config.get('Proxy', 'http'),
            'https': Config.get('Proxy', 'https'),
        }
    else:
        proxies = {}

