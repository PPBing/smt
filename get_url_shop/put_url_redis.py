#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis
import sys
sys.path.append("..")
from conf import config
root_cates = [
    # 'smt_women_clothing.txt',
    # 'smt_men_clothing.txt',
    # 'smt_cellphones.txt',
    # 'smt_computer.txt',
    # 'smt_consumer_electronics.txt',
    # 'smt_jewelry.txt',
    'smt_home_garden.txt',
    # 'smt_luggage_bags.txt',
    # 'smt_shoes.txt',
    # 'smt_mother_kids.txt',
    # 'smt_sports_entertainment.txt',
    # 'smt_beauty_health.txt',
    # 'smt_watches.txt',
    # 'smt_toys_hobbies.txt',
    # 'smt_weddings_events.txt',
    # 'smt_novelty_special.txt',
    # 'smt_automobiles.txt',
    # 'smt_furniture.txt',
    # 'smt_electronic_components.txt',
    # 'smt_office_school.txt',
    # 'smt_home_improvement.txt',
    # 'smt_security.txt',
    # 'smt_tools.txt',
    # 'smt_hair_extensions.txt',
             ]

class PutUrlRedis(object):
    def __init__(self,root_cate,r):
        self.root_cate = root_cate
        self.r = r

    def put_url_redis(self):
        i = 0
        file_name = str(self.root_cate).rstrip(".txt")+"_url.txt"
        key = file_name.rstrip(".txt")
        with open(config.result_path+file_name,"r") as f:
        # with open("/mnt/received_files/result/" + file_name,"r") as f:
            lines = f.readlines()
            for line in lines:
            # for x in range(500):
            #     line = f.readline()
                self.r.sadd(key,line.strip())
                i+=1
                print i

if __name__=="__main__":
    r = redis.Redis(host="192.168.3.233",port="6379",password="123456")
    # r = redis.Redis(host="54.145.149.156",port="6379",password="sz180830")
    # value = r.spop("test")
    # print value
    # root_cates = config.root_cates
    for root_cate in root_cates:
        put_redis = PutUrlRedis(root_cate,r)
        put_redis.put_url_redis()