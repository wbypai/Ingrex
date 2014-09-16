#coding=utf-8

from __future__ import unicode_literals
from ingrex import praser
from ingrex.config import Config
import json
import datetime
from io import open

user = 'Tokenizer'
msglist = []
msg = ''
flag = 1

with open(Config.get('Option', 'datapath') + 'msg.json', 'r', encoding='ascii') as file:
    while flag:
        try:
            msg = praser.message(json.loads(file.readline()))
            if msg['user'] == user:
                msglist.append(msg)
        except Exception as e:
            flag = 0

