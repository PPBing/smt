#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool as Pool
import re
import datetime
import redis
import json
import os
import sys
sys.path.append("..")
reload(sys)
sys.setdefaultencoding('utf8')
from conf import config
from api.api_request import ApiRequest
import logging
if not os.path.exists(config.log_path):
    os.mkdir(config.log_path)
log_file_name = config.log_path + datetime.date.today().strftime("%Y%m%d") + "info.log"
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_file_name)
formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class GetItemInfo(ApiRequest):
    def __init__(self,key,r):
        """
        创建对象时
        传入redis以及键值，用来获取对应键值中存储的商品url
        :param key:
        :param r:
        """
        self.key = key
        self.r = r
        self.item_info_file = open(config.item_info_path+key.strip("_url")+"_data.txt","a")
        ApiRequest.__init__(self)

    def get_item_info(self,url):
        """
        传入商品链接，返回商品信息
        :param url:
        :return:
        """
        res = self.answer_the_url(url)
        item_info_dic = {}
        if res:
            try:
                soup = BeautifulSoup(res.content, "lxml")
                #获取商品在速卖通上的唯一id
                item_info_dic["item_id"] = re.search(r'.+/(.+)\.html', url).group(1)
                #获取商品的链接
                item_info_dic["item_title_url"] = url
                #获取商品标题
                product_name = soup.find('h1', class_='product-name')
                item_info_dic["item_title"] = product_name.string.decode("ascii").encode("utf-8")
                #获取商品叶子品类
                location = soup.find('div', class_='ui-breadcrumb')
                item_category = location.find_all('a')[-1].get('href')
                item_category = item_category.split('/')[-2]
                item_info_dic['category_id'] = str(item_category)
                #获取商品评分
                product_scores = soup.find('span', class_='percent-num')
                if product_scores:
                    item_info_dic['item_scores'] = float(product_scores.string)
                else:
                    item_info_dic['item_scores'] = 0.0  # 表示原网页没有评分信息
                #获取商品销量
                product_sales = soup.find('span', id='j-order-num')
                if product_sales:
                    item_sales = re.search(r'(\d+)', product_sales.string)
                    item_info_dic['item_sales'] = int(item_sales.group(1))
                else:
                    item_info_dic['item_sales'] = 0  # 表示原网页没有销量信息
                #获取商品价格，如果有折扣价获取的就是折扣价
                #商品最低价
                product_minprice_pattern = re.compile(r'window.runParams.actMinPrice="(.+)"', re.DOTALL)
                product_minprice = re.search(product_minprice_pattern, str(soup))
                if product_minprice:
                    product_minprice = product_minprice.group(1).split(';')[0].split('"')[0]
                else:
                    product_minprice_pattern = re.compile(r'window.runParams.minPrice="(.+)"', re.DOTALL)
                    product_minprice = re.search(product_minprice_pattern, str(soup)).group(1).split(';')[0].split('"')[0]
                #商品最高价
                product_maxprice_pattern = re.compile(r'window.runParams.actMaxPrice="(.+)"', re.DOTALL)
                product_maxprice = re.search(product_maxprice_pattern, str(soup))
                if product_maxprice:
                    product_maxprice = product_maxprice.group(1).split(';')[0].split('"')[0]
                else:
                    product_maxprice_pattern = re.compile(r'window.runParams.maxPrice="(.+)"', re.DOTALL)
                    product_maxprice = re.search(product_maxprice_pattern, str(soup)).group(1).split(';')[0].split('"')[0]
                if product_minprice == product_maxprice:
                    item_info_dic["item_price"] = product_maxprice
                else:
                    item_info_dic["item_price"] = 0

                #获取商品库存
                quantitynum_pattern = re.compile(r'window.runParams.totalAvailQuantity=([0-9]+);', re.DOTALL)
                quantitynum = re.search(quantitynum_pattern, str(soup))
                item_info_dic['item_quantity'] = int(quantitynum.group(1))
                #获取商品的specifics
                product_item_ul = soup.find('ul', class_='product-property-list util-clearfix')
                product_item_li = product_item_ul.find_all('li', class_='property-item')
                item_specifics = []
                for item_li in product_item_li:
                    span_title = item_li.find('span', class_='propery-title').string
                    span_des = item_li.find('span', class_='propery-des').string
                    item_specifics.append({span_title: span_des})
                item_info_dic['item_specifics'] = str(item_specifics)
                #获取商品主图及图片列表
                product_detail_gallery = soup.find_all('span', class_='img-thumb-item')
                product_main_img = product_detail_gallery[0].find('img')  # 获取主图
                item_info_dic['main_image_url'] = product_main_img.get('src').replace('50x50', '640x640')
                # 获取其他图片,存放在列表中，此处就不存主图了
                img_list = []
                for i in range(1, len(product_detail_gallery)):
                    product_other_img = product_detail_gallery[i].find('img')
                    img_list.append(product_other_img.get('src').replace('50x50', '640x640'))
                item_info_dic['other_image_url'] = str(img_list)
                #获取商品包裹信息
                product_pack_ul = soup.find('ul', class_='product-packaging-list util-clearfix')
                item_packaging = []
                product_pack_li = product_pack_ul.find_all('li', class_='packaging-item')
                for item_span in product_pack_li:
                    span_packaging_title = item_span.find('span', class_='packaging-title').string
                    span_packaging_des = item_span.find('span', class_='packaging-des').string
                    item_packaging.append({span_packaging_title: span_packaging_des})
                item_info_dic['item_packaging'] = str(item_packaging)
                # 获取商品细节描述(item_description)，注意：商品链接对应网页中的超链接必须全部清除
                s = requests.session()
                detailDesc_pattern = re.compile(r'window.runParams.detailDesc="(.+)";', re.DOTALL)
                detailDesc = re.search(detailDesc_pattern, str(soup))
                # 获取商品描述的链接
                detailDesc_url = detailDesc.group(1).split('"')[0]
                # 获取描述源码
                # 若该商品的item_description为空，则直接令页面内容为空
                if detailDesc_url == '':
                    ddpage = ''
                else:
                    ddpage = s.get(detailDesc_url).content
                    # 现在把其中的超链接全部清除
                    ddpage = ddpage.replace('href', 'src')
                    s.close()
                    # 数据库中需要存储为字符串格式
                item_info_dic['item_description'] = str({detailDesc_url: ddpage})
                #构造属性字典
                attr_dic = {}
                product_bac = soup.find('div', id='j-product-info-sku')
                product_ul = product_bac.find_all('ul', class_='sku-attr-list util-clearfix')
                for ul in product_ul:
                    li = ul.find_all('li')
                    for x in li:
                        if x.find('span'):
                            value = x.find('span').string
                        else:
                            value = x.a.get('title')
                        key = x.a.get('data-sku-id')
                        attr_dic[key] = value
                #获取产品属性图片
                product_bac = soup.find('div', id='j-product-info-sku')
                pro_dl = product_bac.find_all('dl',class_='p-property-item')
                color_list = []
                attr_name = []
                count = 0
                attr_name.append(count)
                for ul in pro_dl:
                    count += 1 #count为０表示没有属性图片，其他的数字表示为第几个有属性图片
                    attr_name.append(ul.find('dt',class_='p-item-title').string.replace(':',''))
                    if ul.find('img'):
                        pro_li = ul.find_all('li', class_='item-sku-image')
                        for li in pro_li:
                            colro_dic = {}
                            color_link = []
                            color_link.append(li.a.img.get('src'))  # 图片大小50x50
                            color_link.append(li.a.img.get('bigpic'))  # 图片大小640x640
                            attr = str(attr_dic[str(li.a.get('data-sku-id'))])
                            colro_dic[attr] = color_link
                            color_list.append(colro_dic)
                            attr_name[0] = count
                item_info_dic['attr_name'] = str(attr_name)
                item_info_dic['variations_image'] = str(color_list)
                #获取产品属性列表
                attribute = re.search('var skuProducts=(.+)', str(soup), re.DOTALL)
                part = attribute.group(0)
                part = part.split('[')[1]
                part = part.split(']')[0]
                sss = part.split('},')
                attribute_product = []
                for x in sss:
                    x1 = x.split('{')[1]
                    x2 = x.split('{')[2]
                    # x3是属性产品的价格      skuMulitCurrencyDisplayPrice
                    x3 = x2.split('"skuMultiCurrencyDisplayPrice":"')[-1]
                    x3 = x3.replace('"}', '')
                    # x2是属性产品的属性值，以逗号隔开      skuPropIds
                    x2 = x1.split('":"')[-1]
                    x2 = x2.split('","')[0]
                    x3 = x3.strip(',')  # 有些价格中有逗号，这里将逗号去掉
                    # 将data-sku-id替换成英文描述，只用x2和x3，对x2进行切割，用attr_dic翻译
                    x1 = ''
                    for x in x2.split(','):
                        x = str(attr_dic.get(x))
                        x1 = x1 + x + ','
                    x1 = x1.rstrip(',')
                    attribute_product.append('skuAttr:' + x1 + ';' + 'Price:' + x3 + ';')
                # 数据库中需要存储为字符串格式
                item_info_dic['item_variations'] = str(attribute_product)
                return item_info_dic
            except Exception as e:
                # print str(e)
                logger.critical("<parse_the_soup>" + str(e) + "<>" + url + "<>" + str(soup))
                return None

        else:
            logger.critical("<parse_the_res>" + "<>" + url + str(res))
            return None

    def get_url(self):
        """
        从redis中获得url，创建多进程
        :return:
        """
        while True:
            # print 100
            lines = []
            for i in range(100):
                #每次获得100条url,这样设置当程序出现错误时耽误的数据比较少
                url = self.r.spop(self.key)
                # print url
                if not url:
                    break
                lines.append(url)
            if not lines:
                break
            #创建多进程，用来加快爬取的速度
            pool = Pool(10)
            pool.map(self.get_item_info_thread,lines)
            pool.close()
            pool.join()
        self.item_info_file.close()

    def get_item_info_thread(self,url):
        """
        爬取的其他剩余任务
        :param url:
        :return:
        """
        info_dic = self.get_item_info(url)
        if info_dic:
            self.lock.acquire()
            self.item_info_file.write(json.dumps(str(info_dic))+"\n")
            self.lock.release()
        else:
            return

if __name__=="__main__":
    r = redis.Redis(host="192.168.3.233",port="6379",password="123456")
    for root_cate in config.root_cates:
        key = root_cate.strip(".txt") + "_url"
        info = GetItemInfo(key,r)
        info.get_url()

    # key = "smt_toys_hobbies_url"
    # info = GetItemInfo(key,r)
    # info.get_url()
