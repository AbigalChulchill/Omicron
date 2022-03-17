#from datetime import datetime
#import os
import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode

from _Logins import *
from _csv_Ops import *
from _txt_Ops import *
from _Order_Pos_Functions import *
from _Price_Functions import *
from _Balance_Functions import *
from _Fetch_Settings import *
from _Time_Functions import *
from _Precision_Manager import *
from _Binance_Exceptions import *


class Withdraw_Functions():

    def __init__(self,account_no):
        super().__init__()
        self.account_no = account_no
        self.csv_ops = csv_Ops()
        self.txt_ops = txt_Ops()
        self.api_key = Logins().return_Keys(self.account_no)[0]
        self.secret_key = Logins().return_Keys(self.account_no)[1]
        self.price_functions_static = Price_Functions(1)
        self.time_functions = Time_Functions()
        self.precision_functions = Precision_Functions(1)

    def transfer_Spot_Cross_Margin(self,asset,amount):

        status_code = 0
        
        url = 'https://api.binance.com/sapi/v1/margin/transfer'

        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        params = {
            'asset': asset,
            'amount': amount,
            'type': 1,
            'recvWindow': 5000,
            'timestamp': self.time_functions.get_Timestamp(13)
        }

        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

        r = requests.post(url, headers=headers, params=params)
        
        if r.status_code == 200:
            data = r.json()
            status_code = r.status_code
            print("Transferred",amount,asset,"from your Main wallet to your Margin wallet.")
        else:
            data = r.json()
            status_code = data

        return status_code



    def transfer_Spot_Futures(self,asset,amount):

        status_code = 0
        
        url = 'https://api.binance.com/sapi/v1/futures/transfer'

        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        params = {
            'asset': asset,
            'amount': amount,
            'type': 1,
            'recvWindow': 5000,
            'timestamp': self.time_functions.get_Timestamp(13)
        }

        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

        r = requests.post(url, headers=headers, params=params)
        
        if r.status_code == 200:
            data = r.json()
            status_code = r.status_code
            print("Transferred",amount,asset,"from your Main wallet to your Futures wallet.")
        else:
            data = r.json()
            status_code = data

        return status_code


    def transfer_Futures_Spot(self,asset,amount):

        status_code = 0
        
        url = 'https://api.binance.com/sapi/v1/futures/transfer'

        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        params = {
            'asset': asset,
            'amount': amount,
            'type': 2,
            'recvWindow': 5000,
            'timestamp': self.time_functions.get_Timestamp(13)
        }

        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

        r = requests.post(url, headers=headers, params=params)

        if r.status_code == 200:
            data = r.json()
            status_code = r.status_code
            print("Transferred",amount,asset,"from the Futures wallet to your Main wallet.")
        else:
            data = r.json()
            status_code = data

        return status_code


    def request_Deposit_Address(self,crypto,network):

        addy = ''
        tag = ''
        url = 'http://api.binance.com/sapi/v1/capital/deposit/address'

        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        params = {
            'coin':crypto,
            'recvWindow':5000,
            'network':network,
            'timestamp':self.time_functions.get_Timestamp(13)
            
        }

        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        
        r = requests.get(url, headers=headers, params=params)
        
        if r.status_code == 200:
            try:
                data = r.json()
                print(data)
                addy = str(data['address'])
                tag = str(data['tag'])
                file_path = 'txt/setup/' + str(self.account_no) + '/setup_' + str(self.account_no) + '.txt'
                make_string = 'dep_address_USDT=' + addy + '_' + tag
                write_dep_address = self.txt_ops.replace_Specific_Line(file_path,6,make_string)
            except:
                print("Error: Cannot fetch deposit address!")
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())

        return addy,tag

        
    def read_Deposit_Address(self):

        dep_row_str = ''
     
        get_account_settings = Settings(self.account_no).load_Account_Variables()
        dep_row_str = get_account_settings[5]

        return dep_row_str
        

    def convert_USDT_To_Crypto_Withdraw(self,symbol,amount,to_address,memo,network):

        to_buy_perc = 0.95
        amount_prec_str = "%.2f"
        pair_symbol = symbol + 'USDT'
        network = symbol
        status_code = 0

        #amount precision i.e. %.2f
        try:
            amount_prec_str = "%." + str(self.precision_functions.read_Asset_Precision(pair_symbol)[1]) + "f"
        except:
            amount_prec_str = "%." + str(self.precision_functions.request_Asset_Precision(pair_symbol)[1]) + "f"

        #calculate how many of the assets can be bought
        current_price = self.price_functions_static.request_Avg_Price_Data(pair_symbol)
        to_buy = float(amount_prec_str%( (amount/current_price)*to_buy_perc ))
        print("\nYou can purchase:",to_buy,symbol)
        print("\nPlacing order...")
        order_pos_dynamic = Order_Pos_Functions(self.account_no)
        status_code = order_pos_dynamic.create_Spot_Order(pair_symbol,'BUY',to_buy)

        time.sleep(2)

        if status_code == 200:
            status_code = self.withdraw(symbol,to_buy,to_address,memo,network)



        return status_code

                    

    def withdraw(self,asset,amount,address,address_tag,network):

        status_code = 0
            
        url = 'https://api.binance.com/sapi/v1/capital/withdraw/apply'

        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        if address_tag != '':

            params = {
                'coin': asset,
                'amount': amount,
                'address': address,
                'addressTag': address_tag,
                'network': network,
                'recvWindow': 5000,
                'timestamp': self.time_functions.get_Timestamp(13)
            }

        else:

            params = {
                'coin': asset,
                'amount': amount,
                'address': address,
                'network': network,
                'recvWindow': 5000,
                'timestamp': self.time_functions.get_Timestamp(13)
            }

        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'),query_string.encode('utf-8'),hashlib.sha256).hexdigest()
       
        r = requests.post(url,headers=headers,params=params)
        
        if r.status_code == 200:
            data = r.json()
            print(data)
            status_code = r.status_code
        else:
            data = r.json()
            status_code = data

        return status_code








def check_Module():

    withdraw_functions = Withdraw_Functions(2)
    a = withdraw_functions.request_Deposit_Address('USDT','BNB')
    print(a)






if __name__=='__main__':


    check_Module()
