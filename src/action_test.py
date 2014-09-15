#coding=utf-8

from __future__ import unicode_literals
from ingrex import intel, auth, praser
import json

def test_intel():
    intel.fetch_msg()
    print('OK!')
    intel.fetch_map(['17_7407_3407_0_8_100'])
    print('OK!')
    intel.fetch_portal('8eba50b8aca24938809514c50de5bcd3.11')
    print('OK!')
    intel.fetch_score()
    print('OK!')
    intel.fetch_artifacts()
    print('OK!')
    print('module Intel test OK')

def test_auth():
    if auth.verify():
        print('OK!')
        print('module Auth test OK')

def test_praser():
    raw_msg_object = json.loads('["857656ca8de141bab251c8f2b79db833.d",1410149359274,{"plext":{"text":"wadetseng destroyed an L1 Resonator on \u4f5f\u56ed (Wanquanhe Road Side Road, Haidian, Beijing, China, 100091)","markup":[["PLAYER",{"plain":"wadetseng","team":"ENLIGHTENED"}],["TEXT",{"plain":" destroyed an "}],["TEXT",{"plain":"L1"}],["TEXT",{"plain":" Resonator on "}],["PORTAL",{"name":"\u4f5f\u56ed","plain":"\u4f5f\u56ed (Wanquanhe Road Side Road, Haidian, Beijing, China, 100091)","team":"RESISTANCE","latE6":39989578,"address":"Wanquanhe Road Side Road, Haidian, Beijing, China, 100091","lngE6":116300508,"guid":"b0fdb711bcf244f6a998d993a2470c43.16"}]],"plextType":"SYSTEM_BROADCAST","categories":1,"team":"ENLIGHTENED"}}]')
    msg = praser.message(raw_msg_object)
    print('module Praser test OK')


def main():
    #test_intel()
    test_auth()
    test_praser()

if __name__ == '__main__':
    main()
    pass

