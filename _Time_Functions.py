import sys
sys.path.insert(1,'lib')


from _Logins import *
from datetime import datetime,date
import os
import re
import requests
from collections import Counter
#import json
import time
import hmac
import hashlib
from urllib.parse import urljoin, urlencode
from _csv_Ops import *
from _txt_Ops import *
#import email,imaplib
#import calendar
from _txt_Ops import *
txt_ops = txt_Ops()
from _Binance_Exceptions import *





class Time_Functions():


    def __init__(self):
        self.account_no = 1
        self.csv_ops = csv_Ops()
        self.txt_ops = txt_Ops()
        self.api_key = Logins().return_Keys(self.account_no)[0]
        self.secret_key = Logins().return_Keys(self.account_no)[1]

    def convert_Time(self,unix_time):
        fmt = "%H:%M:%S %Y-%m-%d"
        string_length = len(str(unix_time))
        #print('\nConverting timestamp with length', str(string_length) + '...')
        if string_length == 10:
            tm = datetime.fromtimestamp(float(unix_time)/1.)
            converted_time = tm.strftime(fmt)
            #print('\nConverted time:',converted_time)
        elif string_length == 13:
            tm = datetime.fromtimestamp(float(unix_time)/1000.)
            converted_time = tm.strftime(fmt)
            #print('\nConverted time:',converted_time)
        return converted_time



    
    def get_Timestamp(self,length_format):

        final_time = 0

        offset = -0

        get_time = time.time()

        if length_format == 10:
            final_time = int(get_time)



        if length_format == 13:
           
            add_millis = get_time * 1000
            #print(add_millis)
            to_float = float(add_millis)
            to_int = int(to_float)
            #print(to_int)
            final_time = to_int + offset


        return final_time











def check_Module():

    time_functions = Time_Functions()



    get_timestamp = time_functions.get_Timestamp(13)
    print('get_timestamp',get_timestamp)

    converted_time = time_functions.convert_Time(get_timestamp)
    
##    get_timestamp_10 = time_functions.get_Timestamp(10)
##
##    print(get_timestamp_10)
##
##    converted_time_10 = time_functions.convert_Time(get_timestamp_10)
##
##    print(converted_time_10)
##


if __name__=='__main__':


    check_Module()
