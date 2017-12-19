# -*- coding: utf-8 -*-
import json, urllib2, hashlib,struct,sha,time
import sys
from zb.models import tricker, ticket
class zb_api:
    
    curr_usdt_map = {'ink':'ink_usdt',
                     'etc':'etc_usdt',
                     'eth':'eth_usdt',
                     'btc':'btc_usdt',
                     'qtum':'qtum_usdt'}
    
    def __init__(self, mykey, mysecret):
        self.mykey    = mykey
        self.mysecret = mysecret

    def __fill(self, value, lenght, fillByte):
        if len(value) >= lenght:
            return value
        else:
            fillSize = lenght - len(value)
        return value + chr(fillByte) * fillSize

    def __doXOr(self, s, value):
        slist = list(s)
        for index in xrange(len(slist)):
            slist[index] = chr(ord(slist[index]) ^ value)
        return "".join(slist)

    def __hmacSign(self, aValue, aKey):
        keyb   = struct.pack("%ds" % len(aKey), aKey)
        value  = struct.pack("%ds" % len(aValue), aValue)
        k_ipad = self.__doXOr(keyb, 0x36)
        k_opad = self.__doXOr(keyb, 0x5c)
        k_ipad = self.__fill(k_ipad, 64, 54)
        k_opad = self.__fill(k_opad, 64, 92)
        m = hashlib.md5()
        m.update(k_ipad)
        m.update(value)
        dg = m.digest()
        
        m = hashlib.md5()
        m.update(k_opad)
        subStr = dg[0:16]
        m.update(subStr)
        dg = m.hexdigest()
        return dg

    def __digest(self, aValue):
        value  = struct.pack("%ds" % len(aValue), aValue)
        print value
        h = sha.new()
        h.update(value)
        dg = h.hexdigest()
        return dg

    def __api_call(self, path, params = ''):
        try:
            SHA_secret = self.__digest(self.mysecret)
            sign = self.__hmacSign(params, SHA_secret)
            reqTime = (int)(time.time()*1000)
            params+= '&sign=%s&reqTime=%d'%(sign, reqTime)
            url = 'https://trade.zb.com/api/' + path + '?' + params
            print 'url:',url
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=2)
            doc = json.loads(response.read())
            return doc
        except Exception,ex:
            print sys.stderr, 'zb request ex: ', ex
            return None
    
    def combine_url_param(self,param_map):
#         param_str = ''
        str_and = "&"
        kv_arr = []
        for k,v in param_map.items():
            arr = (str(k),str(v))
            kv_arr.append("=".join(arr))
        
        param_str = str_and.join(kv_arr)
        return param_str    
    
    def query_account(self):
        try:
            params = "accesskey="+self.mykey+"&method=getAccountInfo"
            path = 'getAccountInfo'
            
            obj = self.__api_call(path, params)
            return obj
        except Exception,ex:
            print sys.stderr, 'zb query_account exception,',ex
            return None
        
    def get_orders_new(self,currency):
        '''
            交易类型1/0[buy/sell]
        '''
        try:
            path = 'getOrdersNew'
            params = "accesskey="+self.mykey+"&currency="+currency+"&method=getOrdersNew&pageIndex=0&pageSize=15&status=0&tradeType=0"
            obj = self.__api_call(path, params)
            print json.dumps(obj)
            
            return obj
        except Exception,ex:
            print sys.stderr, 'zb query_account exception,',ex
            return None
        
    def get_orders_ignore_trade_type(self,currency):
        '''
            交易类型1/0[buy/sell]
        '''
        try:
            path = 'getOrdersIgnoreTradeType'
            method = path
            params = "accesskey="+self.mykey+"&currency="+currency+"&method="+method+"&pageIndex=0&pageSize=15"
            obj = self.__api_call(path, params)
            print json.dumps(obj)
            
            return obj
        except Exception,ex:
            print sys.stderr, 'zb query_account exception,',ex
            return None
    
    def get_pub_depth(self,market):    
        try:
            url = 'http://api.zb.com/data/v1/depth?market='+market+'&size=5'
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=2)
            doc = json.loads(response.read())
#             print type(doc)
#             print doc
            return doc
        except Exception, ex:   
            print sys.stderr, 'zb query_pub info exception,',ex
            return None
    
    def get_pub_tricker(self,market):   
        market = self.curr_usdt_map.get(market,'btc')
        doc = self.get_pub_depth(market)
        bid_arr = doc.get('bids')
        ask_arr = doc.get('asks')
        bid_ticket = self.__get_ticket(bid_arr)
        ask_ticket = self.__get_ticket(ask_arr)
        zb_tricker = tricker(ask_ticket, bid_ticket, 'etc')
        return zb_tricker
    
    def __get_ticket(self,ticket_arr):
        first_bid = ticket_arr[0]
        last_bid = ticket_arr[-1]
        bid_ticket_amount = 0
        bid_price_total = 0
        t_ticket = ticket(first_bid[0], last_bid[0], 0)
        for bid in ticket_arr:
            print bid[0] ,':',bid[1]
            bid_price_total = bid_price_total + bid[0] * bid[1]
            bid_ticket_amount = bid_ticket_amount+bid[1]
            t_ticket.avg_price = bid_price_total / bid_ticket_amount
        return t_ticket
    
#         
# if __name__ == '__main__':
#     access_key    = ''
#     access_secret = ''
# 
#     api = zb_api(access_key, access_secret)
# 
# #     print api.query_account()
# #     print api.get_orders_ignore_trade_type('etc_usdt')
# 
#     print 'ink_usdt'
#     zb_tricker = api.get_pub_tricker('ink_usdt')
#     print zb_tricker.bid_ticket.avg_price
#     print zb_tricker.ask_ticket.avg_price
#     
#     print 'qtum_usdt'
#     zb_tricker = api.get_pub_tricker('qtum_usdt')
#     print zb_tricker.bid_ticket.avg_price
#     print zb_tricker.ask_ticket.avg_price
#     
#         