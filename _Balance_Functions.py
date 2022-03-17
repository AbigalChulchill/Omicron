import sys
from _Logins import *
from datetime import datetime,date
from os import path
import re
import requests
import json
import time
import hmac
import hashlib
from urllib.parse import urlencode
from _csv_Ops import *
from _Binance_Exceptions import *
from _Time_Functions import *
from _txt_Ops import *
from ast import literal_eval
from _Server_Functions import *

class Balance_Functions():

    def __init__(self,account_no):
        #super().__init__()
        self.account_no = account_no
        self.api_key = Logins().return_Keys(self.account_no)[0]
        self.secret_key = Logins().return_Keys(self.account_no)[1]
        self.csv_ops = csv_Ops()
        self.recv_window = 5000
        self.time_functions = Time_Functions()
        self.txt_ops = txt_Ops()
        self.server_functions = Server_Functions()


    def request_Account_Info(self):
        futures_balance = float(0.00)
        futures_margin = float(0.00)
        futures_pnl = float(0.00)
        url = 'http://fapi.binance.com/fapi/v2/account'
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        params = {
            'timestamp':self.time_functions.get_Timestamp(13)
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == 200:
            data = r.json()
            print(data)
            for i in range( len(data)):
                if data[i]['asset']=='USDT':
                    futures_balance = float("%.2f"%(   float(data[i]['balance'])   ))
                    futures_pnl = float("%.2f"%(   float(data[i]['crossUnPnl'])   ))
                    futures_margin = futures_balance + futures_pnl
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())
        return futures_balance,futures_margin,futures_margin-futures_balance    



    def request_Futures_Balances(self):
        futures_balance = float(0.00)
        futures_margin = float(0.00)
        futures_pnl = float(0.00)
        url = 'http://fapi.binance.com/fapi/v2/balance'
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        params = {
            'recvWindow':self.recv_window,
            'timestamp':self.time_functions.get_Timestamp(13)
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == 200:
            data = r.json()
            #print(data)
            for i in range( len(data)):
                if data[i]['asset']=='USDT':
                    futures_balance = float("%.2f"%(   float(data[i]['balance'])   ))
                    futures_pnl = float("%.2f"%(   float(data[i]['crossUnPnl'])   ))
                    futures_margin = futures_balance + futures_pnl
                    break
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())
        return futures_balance,futures_margin,futures_margin-futures_balance

    def request_Spot_Balance_A_Crypto(self,symbol):
        spot_balance = float(0.00)
        url = 'http://api.binance.com/api/v3/account'
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        params = {
            'timestamp':self.time_functions.get_Timestamp(13),
            'recvWindow':self.recv_window
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        r = requests.get(url,headers=headers,params=params)
        if r.status_code == 200:
            data = r.json()
            crypto_balances = data['balances']
            if len(crypto_balances) > 0:
                for i in range(len(crypto_balances)):
                    if crypto_balances[i]['asset'] == str(symbol):
                        spot_balance = spot_balance + float(crypto_balances[i]['free'])
                        print(symbol,"spot balance of account",str(self.account_no),"is:",spot_balance)
            else:
                print(symbol,"spot balance of account",str(self.account_no),"is 0")
        else:
            print("\nError: Spot balance request unsuccessful.")
        return spot_balance

    def request_Futures_Balances_With_Client(self):

        futures_balance = 0
        futures_margin = 0
        spot_usdt_balance = 0
        balance_array = []

        account_settings_path = 'txt/setup/' + str(self.account_no) + '/setup_' + str(self.account_no) + '.txt'

        if os.path.isfile(account_settings_path):

            get_futures_data = self.request_Futures_Balances()
            futures_balance = float(get_futures_data[0])
            futures_margin = float(get_futures_data[1])

            spot_usdt_balance = float( self.request_Spot_Balance_USDT() )

            balance_array = [futures_balance,futures_margin,spot_usdt_balance]
            set_string = 'balance=' + str(balance_array)
            self.txt_ops.replace_Specific_Line(account_settings_path,3,set_string)       

        return futures_balance,futures_margin,spot_usdt_balance

    def read_Futures_Balances(self):

        account_dict = {}
        balance_str = ''
        balance_array = []
        
        account_settings_path = 'txt/setup/' + str(self.account_no) + '/setup_' + str(self.account_no) + '.txt'

        if os.path.isfile(account_settings_path):
            account_dict = self.txt_ops.create_dict_from_txt(account_settings_path,'=')
            try:
                balance_str = account_dict['balance']
                balance_array = literal_eval(balance_str)
            except:
                print("\nError: Balance read error!")
        else:
            print("\nError: Account settings file does not exist!")

        return balance_array

    def request_Spot_Balance_USDT(self):

        spot_balance = 0.00

        url = 'http://api.binance.com/api/v3/account'

        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        params = {
            'timestamp':self.time_functions.get_Timestamp(13),
            'recvWindow':self.recv_window
        }

        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'),query_string.encode('utf-8'),hashlib.sha256).hexdigest()
        r = requests.get(url,headers=headers,params=params)

        if r.status_code == 200:
            crypto_balances = r.json()['balances']
            for i in range(len(crypto_balances),0):
                curr_item = crypto_balances[i]
                if curr_item['asset'] == 'USDT':
                    spot_balance = float(curr_item['free'])
                    #print(spot_balance)
                    break
        return spot_balance


def check_Module():

##    import timeit
##
##    iterations = 1
##
    balance_functions = Balance_Functions(2)
##
##    a = timeit.timeit(lambda:balance_functions.request_Spot_Balance_A_Crypto('USDT'),number=iterations)
##    print(a)

    #b = balance_functions.request_Spot_Balance_USDT()
    #print(b)
##
    get_balances_future = balance_functions.request_Account_Info()#request_Spot_Balance_A_Crypto('XLM')
    print(get_balances_future)

    #get_balances_future = balance_functions.read_Futures_Balances()
    #print(get_balances_future)


    #print(get_balances_spot)

##        
##    balance_functions = Balance_Functions(1)
##    get_balances = balance_functions.request_Spot_Balance_A_Crypto('BNB')
##    get_balances = balance_functions.request_Spot_Balance_A_Crypto('USDT')
##    get_balances = balance_functions.request_Spot_Balance_A_Crypto('ETH')
##    get_balances = balance_functions.request_Spot_Balance_A_Crypto('BTC')
##    get_balances = balance_functions.request_Spot_Balance_A_Crypto('UNI')
##    get_balances = balance_functions.request_Spot_Balance_A_Crypto('BTC')
##    get_balances = balance_functions.request_Spot_Balance_A_Crypto('DOT')
##    get_balances = balance_functions.request_Spot_Balance_A_Crypto('ADA')
##    print("...")


##    #check all futures balances
##    for i in range(12):
##        print(i+1)
##        balance_functions = Balance_Functions(i+1)
##        get_balances = balance_functions.request_Futures_Balances()[2]
##        print(get_balances)
##        print("...")

if __name__== '__main__':
    check_Module()
