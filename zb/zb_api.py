# -*- coding: utf-8 -*-
import json, urllib2, hashlib,struct,sha,time
import sys
class zb_api:
    
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
        
        
if __name__ == '__main__':
    access_key    = ''
    access_secret = ''

    api = zb_api(access_key, access_secret)

#     print api.query_account()
    print api.get_orders_ignore_trade_type('etc_usdt')