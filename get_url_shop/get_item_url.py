#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import redis
from multiprocessing.pool import ThreadPool as Pool
import os
import sys
sys.path.append("..")
from conf import config
from api.api_request import ApiRequest
if not os.path.exists(config.result_path):
    os.mkdir(config.result_path)
if not os.path.exists(config.shop_id_path):
    os.mkdir(config.shop_id_path)


class GetItemUrl(ApiRequest):
    """
    获得单个商品的url及对应的卖家id
    """
    def __init__(self,key,r):
        self.key = key
        self.result_file = open(config.result_path+key+"_url.txt","a")
        self.shop_file = open(config.shop_id_path+key+"_shop.txt","a")
        self.r = r
        ApiRequest.__init__(self)

    def get_url(self):
        while True:
            print 100
            lines = []
            for i in range(100):
                url = self.r.rpop(self.key)
                if not url:
                    break
                lines.append(url)
            if not lines:
                break
            pool = Pool(10)
            pool.map(self.get_url_pool, lines)
            pool.close()
            pool.join()
        self.result_file.close()
        self.shop_file.close()

    def get_url_pool(self,url):
        """
        传入根类对应的键,获得链接与卖家id并写入文件
        :param key:
        :return:
        """
        res = self.answer_the_url(url)
        if res:
            soup = BeautifulSoup(res.content, "lxml")
            if soup.find('ul', id='list-items'):
                self.lock.acquire()
                item_ul = soup.find('ul', id='list-items')
                item_li = item_ul.find_all('li')
                for li in item_li:
                    item_h3 = li.find('h3')
                    item_url_a = item_h3.find('a')
                    item_url = 'https:' + str(item_url_a.get('href'))
                    item_url = item_url.split('.html')[0] + '.html'
                    self.result_file.write(item_url + '\n')
                    # print item_url
                    item_shopId_a = li.find('a', class_='store $p4pLog')
                    shop_id = str(item_shopId_a.get('href')).split('/')[-1]
                    self.shop_file.write(shop_id + '\n')
                self.lock.release()
            elif soup.find("ul", class_="util-clearfix son-list"):
                self.lock.acquire()
                item_ul = soup.find('ul', class_='util-clearfix son-list')
                item_li = item_ul.find_all('li')  # 需要处理异常
                for li in item_li:
                    item_h3 = li.find('h3')
                    item_url_a = item_h3.find('a')
                    item_url = 'https:' + str(item_url_a.get('href'))
                    item_url = item_url.split('.html')[0] + '.html'
                    self.result_file.write(item_url + '\n')
                    # print item_url
                    item_shopId_a = li.find('a', class_='store $p4pLog')
                    shop_id = str(item_shopId_a.get('href')).split('/')[-1]
                    self.shop_file.write(shop_id + '\n')
                self.lock.release()
            else:
                return
        else:
            return

if __name__=="__main__":
    r = redis.Redis(host="192.168.3.233",port="6379")
    for root_cate in config.root_cates:
        key = root_cate.strip(".txt")
        get_item_url = GetItemUrl(key, r)
        get_item_url.get_url()