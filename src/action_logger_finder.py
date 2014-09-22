#coding=utf-8

from __future__ import unicode_literals
from ingrex.config import Config
import json
import datetime
from io import open

target = 'destroyed the Link'
msglist = []
msg = ''
flag = 1

with open(Config.get('Option', 'datapath') + 'msg.json', 'r', encoding='ascii') as file:
    while flag:
        try:
            msg = json.loads(file.readline())
            if msg[2]['plext']['text'].find(target) == -1:
                pass
            else:
                msglist.append(msg)
                print('Catched!')
        except Exception as e:
            flag = 0

with open(target + '.log' ,'w', encoding='utf-8') as file:
    for msg in msglist[::-1]:
        daytime = datetime.datetime.fromtimestamp(msg[1] // 1000)
        daytime += datetime.timedelta(milliseconds = (msg[1] % 1000))
        file.write('{}|{}: {}\n'.format(
            msg[0],
            daytime.strftime('%Y/%m/%d %H:%M:%S,%f')[:-3],
            msg[2]['plext']['text']
        ))

with open(target + '.json', 'w', encoding='ascii') as file:
    for msg in msglist[::-1]:
        file.write(json.dumps(msg) + '\n')

print('Over!')
