# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import time
accesskey=''
currency='ink_usdt'

class CZB():
    
    def get_orders(self):
        zb_url = 'https://trade.zb.com/api/getOrdersNew'
        param_map = {'accesskey':accesskey,
                     'currency':currency,
                     'method':'getOrdersNew',
                     'pageIndex':1,
                     'pageSize':15,
                     'tradeType':0,
                     'reqTime':round(time.time() * 1000)}
#         ?accesskey=youraccesskey
# &currency=ltc_btc&method=getOrdersNew&pageIndex=1&pageSize=1&tradeType=1
#     &sign=请求加密签名串&reqTime=当前时间毫秒数】
    
    def combine_url_param(self,url,param_map):
        param_str = ''
        str_and = "&"
        kv_arr = []
        for k,v in param_map.items():
            arr = (str(k),str(v))
            kv_arr.append("=".join(arr))
        
        param_str = str_and.join(kv_arr)
        full_ful = "?".join((url,param_str))
        return full_ful
    
url = "www.baidu.com"
param_map = {'fly':123,
             'name':"haha"}
z = CZB()
print z.combine_url_param(url, param_map)