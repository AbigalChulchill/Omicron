import sys
sys.path.insert(1,'lib')
from _Logins import *
import winsound
import requests
import time
import hmac
import hashlib
import math
from urllib.parse import urlencode
from _csv_Ops import *
from _txt_Ops import *
import os
from _Price_Functions import *
#from _Fetch_Settings import *
from _Maths_Functions import *
from _Time_Functions import *
from _Signals import *
from _Binance_Exceptions import *
from _Balance_Functions import *
from os import walk
from ast import literal_eval


class Precision_Functions():

    def __init__(self,account_no):
        self.account_no = account_no
        self.csv_ops = csv_Ops()
        self.txt_ops = txt_Ops()
        self.api_key = Logins().return_Keys(self.account_no)[0]
        self.secret_key = Logins().return_Keys(self.account_no)[1]
        self.balance_functions = Balance_Functions(self.account_no)
        self.maths_functions = Maths_Functions(1)
        self.price_functions = Price_Functions(1)
        self.time_functions = Time_Functions()



    def read_Asset_Precision(self,symbol):

        precise_price = 2
        quant_precise = 3

        if symbol == 'BNBUSDT':
            precise_price = 3
            quant_precise = 2
        elif symbol == 'ADAUSDT':
            precise_price = 5
            quant_precise = 0
        elif symbol == 'XLMUSDT':
            precise_price = 5
            quant_precise = 0

        return precise_price,quant_precise





    def request_Asset_Precision(self,symbol):
            
        url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'

        headers = {}

        params = {
            'timestamp': self.time_functions.get_Timestamp(13)
        }

        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'),query_string.encode('utf-8'),hashlib.sha256).hexdigest()
        r = requests.get(url,headers=headers,params=params)

        if r.status_code == 200:

            data = r.json()
            symbols_list = data['symbols']
            symbols_list_len = len(symbols_list)

            for i in range(symbols_list_len):
                if symbols_list[i]['symbol'] == str(symbol):
                    quant_precise = symbols_list[i]['quantityPrecision']
                    price_precise = symbols_list[i]['pricePrecision']
                    print(price_precise,quant_precise)
                    return price_precise,quant_precise
                    
        else:
            print("\nPrecision Manager | Error: Unable to fetch data!")
            #raise BinanceException(status_code=r.status_code,data=r.json())

    



def check_Module():
    precise_list = ['BTCUSDT','ETHUSDT','LTCUSDT','BNBUSDT','ADAUSDT']
    functions = Precision_Functions(1)
    for i in range(len(precise_list)):
        get_precise = functions.request_Asset_Precision(precise_list[i])
        print(precise_list[i],get_precise)


    

if __name__== '__main__':


    check_Module()
