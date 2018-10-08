#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('..')
import MySQLdb
from conf import config
import logging
log_file_name = config.log_path+"store.log"
logger = logging.getLogger()
handler = logging.FileHandler(log_file_name)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class StoreInfo(object):
    def __init__(self,key):
        self.key = key

    def store_info(self):
        # conn = MySQLdb.connect(host='192.168.3.211',
        #                        user='root',
        #                        passwd='mingliang',
        #                        db='fqd')
        conn = MySQLdb.connect(host='192.168.3.233',
                               user='root',
                               passwd='Aa123456',
                               db='smt')
        curror = conn.cursor()
        info_file = config.item_info_path + self.key + "_data.txt"
        with open(info_file,"r") as f:
            while 1:
                line = f.readline().strip()
                if line:
                    try:
                        line = json.loads(line)
                        line = eval(line)
                        sql = "replace into "+self.key+" (item_id,item_title,item_title_url,category_id,main_image_url,other_image_url,item_price,item_sales,item_scores,item_description,item_specifics,item_packaging,item_quantity,item_variations,attr_name,variations_image) value ('"+line["item_id"]+"','"+MySQLdb.escape_string(line["item_title"])+"','"+line["item_title_url"]+"',"+ str(line["category_id"]) +",'"+MySQLdb.escape_string(line["main_image_url"])+"','"+MySQLdb.escape_string(line["other_image_url"])+"',"+str(line["item_price"])+","+str(line["item_sales"])+","+str(line["item_scores"])+",'"+MySQLdb.escape_string(line["item_description"])+"','"+MySQLdb.escape_string(line["item_specifics"])+"','"+MySQLdb.escape_string(line["item_packaging"])+"',"+str(line["item_quantity"])+",'"+MySQLdb.escape_string(line["item_variations"])+"','"+MySQLdb.escape_string(line["attr_name"])+"','"+MySQLdb.escape_string(line["variations_image"])+"')"
                        curror.execute(sql)
                        conn.commit()
                    except Exception as e:
                        print str(e)
                        logger.critical('<store>' + str(e) + '<>' + str(line))
                        continue
                else:
                    break


if __name__=="__main__":
    key = "smt_consumer_electronics"
    store = StoreInfo(key)
    store.store_info()
