import sys
sys.path.insert(1,'lib')
from datetime import datetime,date
import requests
import json
from urllib.parse import urljoin
from _csv_Ops import *
from _txt_Ops import *
from _Time_Functions import *
from _Binance_Exceptions import *


class Server_Functions():

    def __init__(self):
        pass

    def send_Server_Request(self,url,headers_dict,params_dict):
        data = {}
        try:
            r = requests.get(url,headers=headers_dict,params=params_dict)
            status_code = r.status_code
            if status_code == 200:
                data = r.json()
                print(data)
            else:
                print("Error: Return status code not 200!")
                raise BinanceException(status_code=status_code,data=r.json())
        except:
            print("Error: Bad request!") 
        return data





def check_Module():
    server_functions = Server_Functions()
    send_request = server_functions.send_Server_Request('http://data.fixer.io/api/latest','',\
                                                        {'access_key':'cb412e2a377e47d4a2a30ad1f2101797','symbols':'GBP'})

if __name__== '__main__':
    check_Module()
