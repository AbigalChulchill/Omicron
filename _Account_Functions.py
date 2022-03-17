import sys
sys.path.insert(1,'lib')

import math
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

from _Price_Functions import *
from _Time_Functions import *




class Account_Functions():

    def __init__(self,account_no):
        self.account_no = account_no
        self.csv_ops = csv_Ops()
        self.txt_ops = txt_Ops()
        self.api_key = Logins().return_Keys(self.account_no)[0]
        self.secret_key = Logins().return_Keys(self.account_no)[1]
        self.time_functions = Time_Functions()



    def get_Account_Information(self):

        url = 'http://fapi.binance.com/fapi/v2/account'

        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        timestamp = self.time_functions.get_Timestamp(13)

        params = {
            'recvWindow':5000,
            'timestamp':timestamp
        }

        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'),query_string.encode('utf-8'),hashlib.sha256).hexdigest()
        
        r = requests.get(url,headers=headers,params=params)

        if r.status_code == 200:
            status_code = r.status_code
            get_data = r.json()
        else:
            print("\nError: Information cannot be fetched for Account",self.account_no)

        return get_data


    def change_Global_Leverage(self,symbol,leverage):

        url = 'http://fapi.binance.com/fapi/v1/leverage'

        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        timestamp = self.time_functions.get_Timestamp(13)

        params = {
            'symbol':symbol,
            'leverage':leverage, #1 to 125
            'recvWindow':5000,
            'timestamp':timestamp
        }

        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'),query_string.encode('utf-8'),hashlib.sha256).hexdigest()
        
        r = requests.post(url,headers=headers,params=params)

        if r.status_code == 200:
            status_code = r.status_code
            get_data = r.json()
            print("\nGlobal leverage changed to",leverage,'\n',status_code,get_data)

            #write the value to a settings txt file
            path_str = 'txt/settings/leverage/current/account_' + str(self.account_no) + '.txt'
            write_new_val = self.txt_ops.quick_write_txt_file(path_str,leverage)
        else:
            status_code = r.status_code
            get_data = r.json()
            print("\nGlobal leverage change error.",status_code,get_data)






def check_Module():

    account_functions = Account_Functions(1)

    #get account information
    get_account = account_functions.get_Account_Information()
    print(get_account)

    #get current account leverage
    #get_lev = account_functions.get_Account_Current_Leverage()
    #print(get_lev)



    #change global leverage
    #change_global_leverage = account_functions.change_Global_Leverage('ETHUSDT',22)

    #change margin type
    #change_margin_type = account_functions.change_Margin_Type('ETHUSDT','CROSSED')
    
    #change margin type
    #change_margin_leverage = account_functions.change_Margin_Leverage('ETHUSDT',35,'increase') #reduce

    #max_amount = account_functions.calculate_Trade_Max_Amount('ETHUSDT',3)
    #print(max_amount)

    

if __name__=='__main__':


    check_Module()
