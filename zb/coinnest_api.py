# -*- coding: utf-8 -*-
import json, urllib,urllib2, hashlib,struct,sha,time
import sys
from zb.models import tricker, ticket

USDT_KORAN_RATE = 0.0009221    
class coinnest_api:
    def __init__(self, mykey, mysecret):
        self.mykey    = mykey
        self.mysecret = mysecret
        
    def get_pub_tricker(self,market):   
        doc = self.get_pub_depth(market)
        bid_arr = doc.get('bids')
        ask_arr = doc.get('asks')
        bid_ticket = self.__get_ticket(bid_arr)
        ask_ticket = self.__get_ticket(ask_arr)
        zb_tricker = tricker(ask_ticket, bid_ticket,market)
        return zb_tricker
    
    def get_pub_depth(self,market):    
        try:
            url = 'https://api.coinnest.co.kr/api/pub/depth?coin='+market;

            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            request = urllib2.Request(url,headers = headers)
            response = urllib2.urlopen(request, timeout=10)
            doc = json.loads(response.read())
            return doc
        except Exception, ex:   
            print sys.stderr, 'coinnest query_pub info exception,',ex
            return None
        
    def __get_ticket(self,ticket_arr):
#         sample data:
#         ticket_arr[0] = [870, 7107.3704]
        
        first_bid = float(ticket_arr[0][0])
        last_bid = float(ticket_arr[4][0])
        bid_ticket_amount = 0
        bid_price_total = 0
        t_ticket = ticket(last_bid*USDT_KORAN_RATE, first_bid*USDT_KORAN_RATE)
        index = 0;
        while index < 5:
            bid = ticket_arr[index]
            print bid[0]* USDT_KORAN_RATE ,':',bid[1]
            bid_price_total = bid_price_total + bid[0] * bid[1]
            bid_ticket_amount = bid_ticket_amount+bid[1]
            index = index + 1
        t_ticket.avg_price = (bid_price_total / bid_ticket_amount) * USDT_KORAN_RATE
        return t_ticket
    
# print 'ink'
# coin_api = coinnest_api('','')
# tricker = coin_api.get_pub_tricker('ink')
# print 'bid:'
# print tricker.bid_ticket.avg_price
#  
# print 'ask:'
# print tricker.ask_ticket.avg_price

    