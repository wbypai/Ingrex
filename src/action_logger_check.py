#coding=utf-8

from ingrex.config import Config
import json
from io import open

guidlist = []
timelist = []
msg = ''
flag = 1

with open(Config.get('Option', 'datapath') + 'msg.json', 'r', encoding='ascii') as file:
    while flag:
        try:
            msg = json.loads(file.readline())
            guidlist.append(msg[0])
            timelist.append(msg[1])
        except Exception as e:
            flag = 0

count = len(list(set(guidlist)))

if count == len(guidlist):
    print('OK')

i = 0

for i in range(0, len(timelist)-2):
    if timelist[i] > timelist[i+1]:
        print('Error')

print('OK')