#from datetime import datetime,date
import requests
import json
from urllib.parse import urljoin

class Currency_Functions():

    def __init__(self):
        self.access_key = 'cb412e2a377e47d4a2a30ad1f2101797'

    def get_Currency_Rate(self,base_symbol,target_symbol):
        rate = 1
        url = 'http://data.fixer.io/api/latest'
        headers_dict = {}
        params_dict = {'access_key':self.access_key,\
                       'base':base_symbol,
                       'symbols':target_symbol}
        try:
            r = requests.get(url,headers=headers_dict,params=params_dict)
            status_code = r.status_code
            if status_code == 200:
                data = r.json()
                rates_list = data['rates']
                #rate = float(rate)

                #dict1 = {'CNN': '0.000002'}

                for k, v in rates_list.items():
                    rates_list[k] = float(v)

                rate = rates_list[target_symbol]
                print(rate)


            else:
                print("Error: Return status code not 200!")
        except:
            print("Error: Bad server request!")
        return rate



def check_Module():
    c = Currency_Functions()
    get_rate_cedis = c.get_Currency_Rate('USD','GHS')
    get_rate_pounds = c.get_Currency_Rate('USD','GBP')

if __name__== '__main__':
    check_Module()
