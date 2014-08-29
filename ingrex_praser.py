import datetime
import logging
import time

class msgPraser(object):
    def __init__(self):
        self.msglist = []
        self.lastTimestampMs = -1
        self.lastPrintMsgidx = 0
        pass
    
    def load_msg(self, jsondata):
        if 'success' in jsondata:
            self.data = jsondata['success']
        elif 'error' in jsondata:
            if jsondata['error'] == 'out of date':
                logging.warning('API Version out of date')
                raise Exception('v')
        else:
            self.data = []
        
        if self.data:
            self.lastTimestampMs = self.data[0][1] + 1
        
        for item in self.data[::-1]:
            msg = {}
            msg['guid'] = item[0]
            msg['utsm'] = item[1]
            daytime = datetime.datetime.fromtimestamp(item[1] // 1000)
            daytime += datetime.timedelta(milliseconds = (item[1] % 1000))
            msg['time'] = daytime.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]
            msg['text'] = item[2]['plext']['text']
            msg['atom'] = item[2]['plext']['markup']
            msg['type'] = item[2]['plext']['plextType']
            msg['team'] = item[2]['plext']['team']
            self.msglist.append(msg)
        del self.data
    
    def std_print(self):
        for i in range(self.lastPrintMsgidx, len(self.msglist)):
            try:
                print(self.msglist[i]['time'] + ' ')
                print(self.msglist[i]['text'])
                time.sleep(0.1)
            except Exception as e:
                logging.warning(e)
        self.lastPrintMsgidx = len(self.msglist) - 1
    
    def std_save(self):
        with open('comm.log', 'w', encoding='utf-8') as file:
            for i in range(0, len(self.msglist)):
                file.write(self.msglist[i]['time'] + ' ')
                file.write(self.msglist[i]['text'] + '\n')

class mapPraser(object):
    def __init__(self):
        self.polist = []
        pass
    
    def load_json(self, itemlist):
        for item in itemlist:
            if item[0][-2:] in ['16', '11']:
                portal = {
                'guid': item[0],
                'title': item[2]['title'],
                'latE6': item[2]['latE6'],
                'lngE6': item[2]['lngE6']
                }
                if portal in self.polist:
                    pass
                else:
                    self.polist.append(portal)
    
    def std_print(self):
        for portal in self.polist:
            print('%s, %s, %s, %s' % (
                portal['guid'], portal['latE6'], portal['lngE6'],
                portal['title']))
    
    def std_save(self):
        with open('portal.log', 'w', encoding='utf-8') as file:
            for portal in self.polist:
                file.write('%s, %s, %s, %s\n' % (
                    portal['guid'],  portal['latE6'], portal['lngE6'],
                    portal['title']))


class portalPraser(object):
    def __init__(self):
        pass

