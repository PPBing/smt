#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import datetime
import time
from multiprocessing import Lock
import logging
from conf import config
import sys
import os
import random
sys.path.append('..')
if not os.path.exists(config.log_path):
    os.mkdir(config.log_path)
log_file_name = config.log_path + datetime.date.today().strftime("%Y%m%d") + ".log"
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_file_name)
formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class ApiRequest(object):

    def __init__(self):
        self.lock=Lock()
        self.proxies = None
        self.time_out = 20
        self.num = 0
        self.headers = config.headers1

    def answer_the_url(self,url):
        """
        这个方法是所有方法的入口
        :param url:
        :return:
        """
        #传入url
        #返回结果
        use_time = 0
        res = None
        headers = self.headers
        headers["path"]=url.replace('https://www.aliexpress.com', '')
        while True:
            try:
                if self.num >=500:
                    time.sleep(10)
                    self.num=0
                res = requests.get(url,timeout=self.time_out,headers=headers)
                self.num+=1
                break
            except Exception as e:
                time.sleep(random.random() * 2.0 + 0.3)
                logger.warning("<answer_the_url>" + str(e) + url)
                print str(e)
                use_time += 1
                if use_time > 10:
                    config.logger.error("<answer_the_url>" + str(e) + url)
                    break
                time.sleep(60)
                continue
        return res

