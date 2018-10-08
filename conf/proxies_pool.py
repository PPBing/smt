#!/usr/bin/env python
# -*- coding:utf-8 -*-
import config
import time
import datetime


class ProxiesPool:
    able = []

    def __init__(self):
        csvfile = config.base_path + '/'+config.proxies_config
        proxies = open(csvfile).readlines()
        num = config.service_num
        start = (num-1)*15
        end = num*601
        for proxie in proxies[start:end]:
            self.able.append({'proxie':proxie.strip(),'start':datetime.datetime(2018,8,29)})

    def init_proxies(self):
        self.able[0].update({'start':datetime.datetime.now()})
        return self.able[0].get('proxie')

    def get_proxies(self):
        # current_time = datetime.datetime.now()
        self.able.sort(key=lambda x: x['start'], reverse=False)
        # item = self.able[0]
        # start = item.get('start')
        # second = time.mktime(current_time.timetuple()) - time.mktime(start.timetuple())
        # print second
        # if second <= 1800:
        #     # minite = current_time.minute - start.minute
        #     print "代理要睡", 1800 - second
        #     time.sleep(1800-second)
        use_account = self.able[0]
        use_account.update({'start': datetime.datetime.now()})
        self.able[0] = use_account
        return self.able[0].get('proxie')
