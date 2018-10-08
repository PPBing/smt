#!/usr/bin/env python
# -*- coding:utf-8 -*-
from conf import config
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('..')
import MySQLdb

root_path = config.base_path+config.root_path
soure_path = config.source_path

conn = MySQLdb.connect(host='localhost',
                       user='root',
                       passwd='Aa123456',
                       db='Aliexpress')
cursor = conn.cursor()

with open(root_path,'r') as f:
    lines = f.readlines()
    for line in lines:
        line_list = line.strip().split("\t")
        root_id = line_list[0]
        root_name = line_list[1]
        sql = "select category_id from smt_category_tree where  root_id="+root_id
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            with open(soure_path+root_name+".txt","a") as f1:
                for row in rows:
                    row = str(row).lstrip("('").rstrip("',)")
                    f1.write(row+"\n")
        except:
            print "查询失败"



