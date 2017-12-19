# -*- coding: utf-8 -*-
from zb.zb_api import zb_api
from zb.coinnest_api import coinnest_api

compare_arr = ['etc','ink']
sign=''
private_key=''
zbapi = zb_api(sign,private_key)
coinnestapi = coinnest_api(sign,private_key)
for market in compare_arr:
    print market
    zb_tricker = zbapi.get_pub_tricker(market)
    coinnest_tricker = coinnestapi.get_pub_tricker(market)
    print 'zb avg ask:',zb_tricker.ask_ticket.avg_price
    print 'coinnest avg ask:',coinnest_tricker.ask_ticket.avg_price