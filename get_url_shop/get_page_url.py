#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import re
import redis
import sys
sys.path.append("..")
from conf import config
from api.api_request import ApiRequest

class GetPageUrl(ApiRequest):
    """
    获得获取商品url的链接
    """
    def __init__(self,root_cate,r):
        self.resultCount_pattern = re.compile(r'"resultCount":"(.*)"', re.DOTALL)
        self.root_cate = root_cate
        self.r = r
        ApiRequest.__init__(self)

    def get_result(self,soup):
        """
        传入源码，返回商品个数
        :param res:
        :return:
        """
        resultCount = int(re.search(self.resultCount_pattern, str(soup)).group(1).split('"')[0])
        return resultCount

    def get_price_range(self,soup):
        """
        传入网页源码，返回价格区间
        :return:
        """
        item_ul = soup.find('ul', id="price-range-list")
        item_div = item_ul.find_all('div', id='histogram-height-rate')
        price_list = []
        for i in item_div:
            price_from = str(i.get('price-range-from'))
            price_to = str(i.get('price-range-to'))
            price_list.append(price_from)
            price_list.append(price_to)
        price_list_list = [price_list[_index:_index + 2] for _index in range(0, 10, 2)]
        return price_list_list

    def get_page_url(self):
        """
        传入叶子id的文件，返回该根类对应的页面链接
        :param root_cate:
        :return:
        """
        file_name = config.source_path+self.root_cate
        key = str(root_cate).rstrip(".txt")
        with open(file_name,"r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                url = config.url.format(leaf_id=line)
                res = self.answer_the_url(url)
                if res:
                    soup = BeautifulSoup(res.content,"lxml")
                    total_result = self.get_result(soup)
                    if total_result >4800:
                        price_list_list = self.get_price_range(soup)
                        for price_range in price_list_list:
                            url_price  = config.url_price.format(leaf_id=line,minPrice=price_range[0],maxPrice=price_range[1])
                            price_res = self.answer_the_url(url_price)
                            price_soup = BeautifulSoup(price_res.content,"lxml")
                            result_count = self.get_result(price_soup)
                            if result_count >4800:
                                for x in range(1,101):
                                    page_url = config.page_url.format(leaf_id=line,page=x,minPrice=price_range[0],maxPrice=price_range[1])
                                    self.r.lpush(key,page_url)
                            else:
                                page = result_count/48 +2
                                for x in range(1,page):
                                    page_url = config.page_url.format(leaf_id=line,page=x,minPrice=price_range[0],maxPrice=price_range[1])
                                    self.r.lpush(key,page_url)
                    else:
                        page = total_result/48 +2
                        for x in range(1,page):
                            page_url = config.under4800_page_url.format(leaf_id=line,page=x)
                            self.r.lpush(key,page_url)




if __name__=="__main__":
    r = redis.Redis(host="192.168.3.233",port="6379")
    for root_cate in config.root_cates:
        get_page = GetPageUrl(root_cate,r)
        get_page.get_page_url()


