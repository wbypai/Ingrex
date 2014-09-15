from ingrex import intel, auth
from ingrex.config import Config
import json
import os
import datetime

def fetch(minTimestampMs, maxTimestampMs=-1, ascendingTimestampOrder=True):
    jsondata = intel.fetch_msg(ascendingTimestampOrder, minTimestampMs, maxTimestampMs)
    msglist = []
    if 'success' in jsondata:
        msglist = jsondata['success']
    elif 'error' in jsondata:
        if jsondata['error'] == 'out of date':
            auth.verify()
    return msglist

def download():
    with open(Config.get('Option', 'datapath') + 'msg.ini') as file:
        minTimestampMs = int(file.readline())
        lastguid = file.readline()
    daytime = datetime.datetime.fromtimestamp(minTimestampMs // 1000)
    daytime += datetime.timedelta(milliseconds = (minTimestampMs % 1000))
    nowtime = datetime.datetime.now()
    tdelta = nowtime - daytime
    dd = tdelta.days
    dh, rem = divmod(tdelta.seconds, 3600)
    dm, ds = divmod(rem, 60)
    print(nowtime.strftime('%Y/%m/%d %H:%M:%S,%f')[:-3] + ' ---- ' + 
        daytime.strftime('%Y/%m/%d %H:%M:%S,%f')[:-3] + ' ---- ' + 
        '{} days {:0>2d}:{:0>2d}:{:0>2d} left.'.format(dd, dh, dm, ds))
    msglist = fetch(minTimestampMs)
    if not msglist:
        os.remove('action_logger.on')
        raise Exception
    file = open(Config.get('Option', 'datapath') + 'msg.json', 'a+')
    sysbc = 0
    if lastguid:
        flag = 0
    else:
        flag = 1
    for msg in msglist:
        if flag:
            if msg[2]['plext']['plextType'] == 'SYSTEM_BROADCAST':
                file.write(json.dumps(msg) + '\n')
                sysbc += 1
        if msg[0] == lastguid:
            flag = 1
    file.close
    print(str(sysbc) + ' messages fetched!')
    try:
        lastguid = msglist[-1][0]
        if minTimestampMs == msglist[-1][1]:
            minTimestampMs += 1
            lastguid = ''
        else:
            minTimestampMs = msglist[-1][1]
    except:
        pass
    with open(Config.get('Option', 'datapath') + 'msg.ini', 'w') as file:
        file.write(str(minTimestampMs) + '\n')
        file.write(lastguid)

def main():
    if os.path.isfile(Config.get('Option', 'datapath') + 'msg.ini'):
        pass
    else:
        with open(Config.get('Option', 'datapath') + 'msg.ini', 'w') as file:
            file.write(str(1396310400000) + '\n')
    
    if os.path.isfile('action_logger.on'):
        pass
    else:
        with open('action_logger.on', 'w') as file:
            file.write('\n')
    
    while os.path.isfile('action_logger.on'):
        try:
            download()
        except Exception as e:
            print('{}{}'.format(type(e), e.args))

if __name__ == '__main__':
    main()

