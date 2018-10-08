#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
# import datetime
# import logging

service_num = 1
proxies_config = "IP_proxy.txt"


base_path = os.path.join(os.getcwd(), os.path.dirname(__file__)).replace("\\", "/").replace("/get_url_shop","").replace("..","").replace("/conf","")

log_path = (base_path + "/log/").replace("//", "/").replace("/test","").replace("/get_item_info","").replace("/get_url_shop","")
result_path = (base_path + "/result/").replace("//", "/")#商品url存放路径
source_path = (base_path + "/source/").replace("//", "/")#叶子id存放路径
shop_id_path = (base_path + "/shop_id/").replace("//", "/")#卖家id存放路径
shop_url_path = (base_path + "/shop_url_result/").replace("//", "/")
item_info_path = (base_path+"/item_info/").replace("//","/").replace("/get_item_info","").replace("/store_info","")#商品信息存放路径

url = "https://www.aliexpress.com/af/category/{leaf_id}.html?SortType=total_tranpro_desc"#获得叶子类产品数及价格区间的网页链接

url_price = "https://www.aliexpress.com/af/category/{leaf_id}.html?SortType=total_tranpro_descc&minPrice={minPrice}&maxPrice={maxPrice}"#获得该价格区间的产品数链接

under4800_page_url = "https://www.aliexpress.com/af/category/{leaf_id}/{page}.html?SortType=total_tranpro_desc"#当叶子类产品数不足4800时页面链接

page_url = "https://www.aliexpress.com/af/category/{leaf_id}/{page}.html?SortType=total_tranpro_desc&minPrice={minPrice}&maxPrice={maxPrice}"#当叶子类产品数超过4800时页面链接

shop_url = "https://www.aliexpress.com/store/{shop_id}/search/1.html"

shop_page_url = "https://www.aliexpress.com/store/{shop_id}/search/{page}.html"

root_path = "/root.txt"#根节点id路径

headers = {
        'authority': 'www.aliexpress.com',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie':'ali_apache_id=10.181.239.20.1532396629311.095168.6; cna=WWvTEzvP3wMCAXFmpJ5HeKGe; _ga=GA1.2.1277524822.1532396638; _uab_collina=153242135258565595162801; aep_common_f=HZ1Nz0VL5ytsdjSSZmRfpHyBiKjHMdtPbrUFNxuwbEfo28mSuaKqaQ==; l=AgMDcnzBIPs9NJWvUt-USvDcE8ytSJe6; __utmz=3375712.1533887475.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ym_uid=1535532201161954913; _ym_d=1535532201; aefeMsite=amp-seauV7BLMhZd8KRXvD0XVQ; AMP_ECID_GOOGLE=amp-fO6QUj_ho3gNJFzMaY8N1w; amp-user-notification=amp-WcnmSCm-rC-nnspv3tP65Q; _umdata=65F7F3A2F63DF020E9F2D8A14F0A5B57E8450852BDF19B9D203CF091B2CBB3ACE0A0BCE87341EB38CD43AD3E795C914CC646FD3B7E5274F0FD3672AC4DD56985; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932904534817%0932918492421%0932871227862%0932862728707%0932892926424%0932897878617%0932860038975%0932762722373; _m_h5_tk=b208442f44f2b5725753184a4df323fa_1536545383502; _m_h5_tk_enc=3caaf146f6273e1e043c0c23136d0163; _gid=GA1.2.1208563009.1536543404; __utma=3375712.1277524822.1532396638.1534329255.1536543405.13; __utmt=1; __utmb=3375712.7.10.1536543405; intl_locale=en_US; acs_usuc_t=acs_rt=df09a8953f544ccebf61b445cd5bb225&x_csrf=13z5q0p0zbe4j; _hvn_login=13; xman_us_t=x_lid=cn13331410kmsae&sign=y&x_user=XgIqyrpe/0+255Sj63/gO4/XY6kp+47Wm46qDRxom8c=&ctoken=_t5bfgqb2b6i&need_popup=y&l_source=aliexpress; aep_usuc_t=ber_l=A0; xman_f=uojIcKdR7gkm2g4g7F3/Wu1iLjirKiRXBiUNGhV3F4TMtoaVK+T8fC5oR1D2qr3nhQ072GQgZdeboHb9kwFWUHaF13csdhW7EM4ythVBVqabAiK0fBWG7DXtxqLBYLNIASlFP6zUBMTB75NBqYFR2E9Y4aEcFjrrook/GwagKkGxopxdByYoM0RDzOooTg6Bjs7m1eesziO/lX1H2YexQ/pFPgl+yW5uqPd/84/D3Gq28ixxFS/7Oe4zfe97gpKyhlJWAdzqBdwZDYpjTxsXbhA70TeDWu5n94TPdTgBobMggoIpPTl3j34KPC3Ux0ZcPWV7gEish3ujRvgvialpv651vYWgIAcq/2kPD6Q1Tw07h2KUn6os5DV2EJbEvqCVnhjuZeZ7z+9t7eqbyT+baZ2ZdWed7v/m; xman_us_f=zero_order=y&x_locale=en_US&x_l=1&last_popup_time=1533863595311&x_user=CN|wu|label|ifm|1614962410&no_popup_today=n; aep_usuc_f=site=glo&aep_cet=mobile&c_tp=USD&x_alimid=1614962410&isb=y&region=US&b_locale=en_US; ali_apache_track=ms=|mt=1|mid=cn13331410kmsae; ali_apache_tracktmp=W_signed=Y; _gat=1; isg=BAoK5urQZdB71umFwTAdprXuW_lsU4284xI6QJRDoN3oR6oBfImUZCW1U_M-twbt; xman_t=KkNeCCL+Iy1olTm6FKhnQJUUU82wdyREBJ/d8ES3ziPUM4cfTSj5FceHN9LUdSpldf5o+wFHLPmPutOTNDoDY+jiig5VzsxMbbWHleYdNWF+dmPPbg1KOESYnHRJIEbRtYQyozkRsj8hKxcqWuBwrEzGe1r/hRzjlja0lUaLvZMQ4U8eZ1ZmvmN7KnIYwoHuNMSWc/OlBO9oP7i1Eg1gKsAUgfxv4a31WXLI6xOc24Ke/noPxfmzr8JdqBicXMWef8P948ZEhXocOAIXxMRwkk7Uk4kW1mYg0Ok4JOxKJBsC/pQuRfm77yE3eOsXpAj3lnVp2gCdYIAx+7lYldyw+tzf6sA8WiMWvm1VRezF339DkaZHS82Fp2S8gzDjyq0iRE/AaOxBnUjsfLjNfk4kncbHzCXtf6THYJWbQ7AdrWU34tMy5k3SRdszAEawSvX08pGLHDQnVTvE69Wm2/moC3rhAp8tuSA2U/hr4w/RRzSkNQIu7oqTxdqG7dkTn2hmJebMSVYaWKlsS+YlJzWD3/XEAUzjxg+4EjmeLXgCJQ3pEjW16nyroHg9VjWm8HpaUNf4C7EAl7lzm8w+XH8t6Q3u4lG9HZVBGMq7fy4u4igYGrhxapg3O8HV+H18hOZ+; intl_common_forever=rLYS0H+lJNcNGOXcS/k/5gH73dHEOkWdkRapaLGKnp+W4R+lMkSoEA==; JSESSIONID=AAF76ED7EB2D578730ABB30EEB7CAFE3',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/68.0.3440.75 Chrome/68.0.3440.75 Safari/537.36'
    }
headers1 = {
        'authority': 'www.aliexpress.com',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        # 'cookie':'ali_apache_id=10.181.239.20.1532396629311.095168.6; cna=WWvTEzvP3wMCAXFmpJ5HeKGe; _ga=GA1.2.1277524822.1532396638; _uab_collina=153242135258565595162801; aep_common_f=HZ1Nz0VL5ytsdjSSZmRfpHyBiKjHMdtPbrUFNxuwbEfo28mSuaKqaQ==; l=AgMDcnzBIPs9NJWvUt-USvDcE8ytSJe6; __utmz=3375712.1533887475.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=3375712.1277524822.1532396638.1534326024.1534329255.12; _ym_uid=1535532201161954913; _ym_d=1535532201; aefeMsite=amp-seauV7BLMhZd8KRXvD0XVQ; AMP_ECID_GOOGLE=amp-fO6QUj_ho3gNJFzMaY8N1w; amp-user-notification=amp-WcnmSCm-rC-nnspv3tP65Q; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932905173582%0932875359179%0932903961264%0932911623894%0932830254249%0932878620202%0932821420751%0932762722373; _umdata=65F7F3A2F63DF020E9F2D8A14F0A5B57E8450852BDF19B9D203CF091B2CBB3ACE0A0BCE87341EB38CD43AD3E795C914C30EB058C1196EAE0E0341C7A8D074C40; intl_locale=en_US; _gid=GA1.2.2041737998.1535945452; acs_usuc_t=acs_rt=5067dd02d7994a2990524d0b04b06360&x_csrf=fbay3bx770z_; _hvn_login=13; xman_us_t=x_lid=cn13088817odhae&sign=y&x_user=vBzm2+gNTRiTVEXMUVvq+r63y/MM8fBOv+OX3fTcT78=&ctoken=h5qgaarcpeo4&need_popup=y&l_source=aliexpress; aep_usuc_t=ber_l=A0; xman_f=Au0jC9k9lhvHnHypswEC8g6epwMhuvHe/lf4VJa8rKcxfMLK/ovpV1LMH+nB/Lk2iNTY4fzLOoaqQLPwnTi02mzkrbmUjtEEFS9zLEnaNShgmGnQt9UODUg8iJ31209V0xi3zi6CBGLCu1hJJ8EnKYG7q0ClwASePiPhxmpAEmya+942fAmzpAUAFu1qLgqVpiIdHkyrRG+rdb0VuasbT1A8n40suoJNroMLkMot3eTBCakEHynE0oSagZGCUOiRVVJeJX5RzfAzJpqvaoEcVTGVzOpAb0C/lBSTsNQQZZKOMpW6QCbZuRpva1E52yJMX9HsjybHwgAewyFEpg79K0Hr+zVeYr3VGkOTAyuto7ckOKy1cesqXHPvfifcO0/v1zuf/4VYbuxNPoop+bW+mA==; xman_us_f=zero_order=y&x_locale=en_US&x_l=1&last_popup_time=1533863595311&x_user=CN|Huge|bing|ifm|1614579817&no_popup_today=n; aep_usuc_f=site=glo&c_tp=USD&x_alimid=1614579817&isb=y&region=US&b_locale=en_US; ali_apache_tracktmp=W_signed=Y; _m_h5_tk=e659a0185f394fbde48cebaf44183689_1535969625257; _m_h5_tk_enc=5e949d25a24b34126e49f3f0af2f4e9c; _gat=1; ali_apache_track=mt=1|ms=|mid=cn13088817odhae; isg=BEFBtivT_hywTxLIFsVWk7pjUISbxraJvI9hzaOWUMinimFc6ry1MX2oaL5pgk2Y; xman_t=SBcucOSL1L/rh60gQ3kkmdRCMNc9O3iDSVy25RexdYfOXxxtmvUWp/zhAp5dtfshQ7d7n3gytoAXdcZQMU0rrkKoL6q3TjNJV3qn8YPE3K6vcaAq8utYQVvih9lNJsvuS07KH/nsS+yxxVuV3jsqwXp1q2OjdqZAoDaxf74ny1Pujgr0JShoeylrkz9TVWbN54piE8UBoz8jOFRqxrBlS6PCu5xP73Qm/lFvQiU7GrXCaXZIGeK1cMJ6T+L/y+U5siuLVcm0taIXjB2WoJ2zN1AyIUbsKmErX+CiXGDxu2pEz8IH0f/WN2yuyT1pglL2ixN6s7Z6kUYkmwlf7Tsh8q3u7pZXbdHn7h2oIyNFuwzDDAQApIrgIIsIrZo5lueWlpK+U5BtV/U1fRU2Kq0ZbOVHQJWkl4U4HnCqQITNFHt521Ke5eugO+rj2W94J3TkLJ6fhMUpAu1noIW1J0LQRujm3t+TqnBLw6t4UJYZTVJt6UpZFHpkRBuJeHsxaQdlUASiYsVntOsuuq7W1zQm3bDS9FEDzqFuPrjoqLPwxFpK9BhFPLr2xfnvaoSRQXTs1Y6voi7f99kH14YB3D7udOSAh2WfHrjE9gOCvmibKuhEjM82CjkVKg==; intl_common_forever=HfC7n9XQMmdb0jlzT4rTw3VDFauh3QRSXWIGWemQVLlG5vjZFVWCuA==; JSESSIONID=EE9669DB3C1A6382E1FAB210A4EE006D',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/68.0.3440.75 Chrome/68.0.3440.75 Safari/537.36'
    }

root_cates = [
    'smt_women_clothing.txt',
    'smt_men_clothing.txt',
    'smt_cellphones.txt',
    'smt_computer.txt',
    'smt_consumer_electronics.txt',
    'smt_jewelry.txt',
    'smt_home_garden.txt',
    'smt_luggage_bags.txt',
    'smt_shoes.txt',
    'smt_mother_kids.txt',
    'smt_sports_entertainment.txt',
    'smt_beauty_health.txt',
    'smt_watches.txt',
    'smt_toys_hobbies.txt',
    'smt_weddings_events.txt',
    'smt_novelty_special.txt',
    'smt_automobiles.txt',
    'smt_furniture.txt',
    'smt_electronic_components.txt',
    'smt_office_school.txt',
    'smt_home_improvement.txt',
    'smt_security.txt',
    'smt_tools.txt',
    'smt_hair_extensions.txt',
             ]


