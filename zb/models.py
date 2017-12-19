# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class tricker():
    
    def __init__(self,ask_ticket,bid_ticket,curr_type):
        self.ask_ticket = ask_ticket
        self.bid_ticket = bid_ticket
        self.curr_type = curr_type
        
class ticket():
    def __init__(self,max_price,min_price,avg_price=0):
        self.max_price = max_price
        self.min_price = min_price
        self.avg_price = avg_price

    