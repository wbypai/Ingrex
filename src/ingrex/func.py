#coding=utf-8

from __future__ import print_function
from __future__ import unicode_literals
from . import auth
from . import intel

def _check(data):
    if data:
        if 'error' in data:
            auth.verify()
            return False
        else:
            return True
    else:
        return False

def load_portal(tileKeys):
    if isinstance(tileKeys, list):
        data = intel.fetch_map(tileKeys)
        prtlist = []
        fetched = []
    else:
        raise TypeError
    
    if _check(data):
        for maplist, mapdata in data['result']['map']:
            if 'error' in mapdata:
                pass
            elif 'gameEntities' in mapdata:
                prtlist.extend(mapdata['gameEntities'])
                fetched.append(maplist)
            else:
                pass
    return prtlist, fetched

