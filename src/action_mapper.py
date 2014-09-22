#coding=utf-8

from __future__ import unicode_literals
from ingrex import intel, auth, maplib
from ingrex.config import Config
import json
import os
import datetime
import time
from io import open

def fetch(tileKeys=[]):
    jsondata = intel.fetch_map(tileKeys)
    prtlist = []
    fetched = []
    if 'result' in jsondata:
        for maplist in jsondata['result']['map']:
            if 'error' in jsondata['result']['map'][maplist]:
                pass
            elif 'gameEntities' in jsondata['result']['map'][maplist]:
                prtlist.extend(jsondata['result']['map'][maplist]['gameEntities'])
                fetched.append(maplist)
            else:
                fetched.append(maplist)
    elif 'error' in jsondata:
        if jsondata['error'] == 'out of date':
            auth.verify()
    return prtlist, fetched

def download():
    with open(Config.get('Option', 'datapath') + 'prt.ini', 'r', encoding='ascii') as file:
        tilekeylist = file.read().split('\n')[:-1]
    nowtime = datetime.datetime.now()
    downlist = tilekeylist[0:4]
    if not downlist:
        os.remove('action_mapper.on')
        os.remove(Config.get('Option', 'datapath') + 'prt.ini')
        raise Exception
    print(nowtime.strftime('%Y/%m/%d %H:%M:%S,%f')[:-3] + ' ---- ' + str(len(tilekeylist)) + ' tiles left.')
    prtlist, fetched = fetch(downlist)
    print(str(len(fetched)) + ' tiles fetched!')
    prtcount = 0
    with open(Config.get('Option', 'datapath') + 'prt.json', 'a+', encoding='ascii') as file:
        for prt in prtlist:
            if prt[2]['type'] == 'portal':
                file.write(json.dumps(prt) + '\n')
                prtcount += 1
    print(str(prtcount) + ' portals fetched!')
    with open(Config.get('Option', 'datapath') + 'prt.ini', 'w', encoding='ascii') as file:
        for tilekey in tilekeylist:
            if not tilekey in fetched:
                file.write(tilekey + '\n')

def simplify():
    with open(Config.get('Option', 'datapath') + 'prt.json', 'r', encoding='ascii') as file:
        prts = file.readlines()
    
    guids = []
    prtlist = []
    
    for prtstr in prts[::-1]:
        prt = json.loads(prtstr[:-1])
        if prt[0] in guids:
            pass
        else:
            prtlist.append(json.dumps(prt))
            guids.append(prt[0])
    prtlist.sort()
    with open(Config.get('Option', 'datapath') + 'prt.json', 'w', encoding='ascii') as file:
        for prt in prtlist:
            file.write(prt + '\n')
    
def main():
    if os.path.isfile(Config.get('Option', 'datapath') + 'prt.ini'):
        pass
    else:
        with open(Config.get('Option', 'datapath') + 'prt.ini', 'w', encoding='ascii') as file:
            xtilemax, ytilemin = maplib.fetch_tilekey(Config.getfloat('Bound', 'maxlat'), Config.getfloat('Bound', 'maxlng'))
            xtilemin, ytilemax = maplib.fetch_tilekey(Config.getfloat('Bound', 'minlat'), Config.getfloat('Bound', 'minlng'))
            for x in range(xtilemin, xtilemax + 1):
                for y in range(ytilemin, ytilemax + 1):
                    tileKey = '17_{0}_{1}_0_8_100'.format(x, y)
                    file.write(tileKey + '\n')
    
    if os.path.isfile('action_mapper.on'):
        pass
    else:
        with open('action_mapper.on', 'w', encoding='ascii') as file:
            file.write('\n')
    
    while os.path.isfile('action_mapper.on'):
        try:
            download()
        except Exception as e:
            print('{}{}'.format(type(e), e.args))
    simplify()

if __name__ == '__main__':
    main()
    print('Over!')

