import sys
sys.path.insert(1,'lib')
from _Logins import *
from datetime import datetime,date
import requests
import json
from urllib.parse import urljoin
from _csv_Ops import *
from _txt_Ops import *
from _Time_Functions import *
from _Binance_Exceptions import *
from _Server_Functions import *

class Price_Functions():

    def __init__(self,account_no):
        super().__init__()
        self.account_no = account_no
        self.csv_ops = csv_Ops()
        self.txt_ops = txt_Ops()
        self.time_functions = Time_Functions()
        self.api_key = Logins().return_Keys(self.account_no)[0]
        self.server_functions = Server_Functions()
        


    def request_Price_Data(self,pair_symbol):
        avg_price = 0
        avg_price_str = ''
        mark_price_str = ''
        mark_price = 0
        hybrid_price = 0
        #get futures average price
        get_avg_price_data = self.server_functions.send_Server_Request('http://fapi.binance.com/fapi/v1/ticker/price',\
                                                                  {'X-MBX-APIKEY':self.api_key},{'symbol':pair_symbol})
        if len(get_avg_price_data) > 0:
            avg_price_str = get_avg_price_data['price']
            avg_price = float("%.2f"%(float(avg_price_str)))
        #get futures mark price
        get_mark_price_data = self.server_functions.send_Server_Request('http://fapi.binance.com/fapi/v1/premiumIndex',\
                                                                   {'X-MBX-APIKEY':self.api_key},{'symbol':pair_symbol})
        if len(get_mark_price_data) > 0:
            mark_price_str = get_mark_price_data['markPrice']
            mark_price = float("%.2f"%(float(mark_price_str)))
        hybrid_price = float("%.2f"%(float((avg_price + mark_price) / 2)))
        return avg_price,mark_price,hybrid_price
       



    def request_Avg_Price_Data(self,pair_symbol):
        spot_price = 0
        #get spot price (non-futures)
        get_spot_price_data = self.server_functions.send_Server_Request('https://api.binance.com/api/v3/avgPrice',\
                                                              {'X-MBX-APIKEY':self.api_key},{'symbol':pair_symbol})
        if len(get_spot_price_data) > 0:
            spot_price_str = get_spot_price_data['price']
            spot_price = float("%.2f"%(float(spot_price_str)))
        return spot_price



    def request_Klines(self,pair_symbol,mins_back):

        short_unix_time = ''
        converted_time = ''

        time_range_unix = []
        time_range_real = []
        open_range = []
        high_range = []
        low_range = []
        close_range = []
        open_close_array = []
        all_prices_array = []
        
        timestamp = self.time_functions.get_Timestamp(13)
        to_ms = mins_back * 60 * 1000

        params = {'symbol':pair_symbol,'interval':'1m','startTime':timestamp-to_ms,'endTime':timestamp,'limit':mins_back}

        data = self.server_functions.send_Server_Request('https://api.binance.com/api/v3/klines',\
                                                              {'X-MBX-APIKEY':self.api_key},params)

        data_length = len(data)
   
        if data_length > 0:
            try:
                for i in range(data_length):
                    
                    short_unix_time = str(data[i][0])[0:10] 
                    converted_time = str(self.time_functions.convert_Time(short_unix_time))
                    time_range_unix.append(short_unix_time)
                    time_range_real.append(converted_time)

                    open_range.append(float(data[i][1]))
                    high_range.append(float(data[i][2]))
                    low_range.append(float(data[i][3]))
                    close_range.append(float(data[i][4]))

                    open_close_array.append(float(data[i][1]))
                    open_close_array.append(float(data[i][4]))
                    
                    all_prices_array.append(float(data[i][1]))
                    all_prices_array.append(float(data[i][2]))
                    all_prices_array.append(float(data[i][3]))
                    all_prices_array.append(float(data[i][4]))

            except:
                pass
        return all_prices_array,open_close_array,time_range_unix,time_range_real,open_range,high_range,low_range,close_range






    def request_Klines_For_Chart(self,pair_symbol,mins_back):

        short_unix_time = ''
        converted_time = ''

        time_range_unix = []
        time_range_real = []
        open_range = []
        high_range = []
        low_range = []
        close_range = []
        open_close_array = []
        all_prices_array = []
        
        timestamp = self.time_functions.get_Timestamp(13)
        to_ms = mins_back * 60 * 1000

        params = {'symbol':pair_symbol,'interval':'1m','startTime':timestamp-to_ms,'endTime':timestamp,'limit':mins_back}

        data = self.server_functions.send_Server_Request('https://api.binance.com/api/v3/klines',\
                                                              {'X-MBX-APIKEY':self.api_key},params)

        data_length = len(data)
   
        if data_length > 0:
            try:
                for i in range(data_length):
                    
                    short_unix_time = str(data[i][0])[0:10] 
                    converted_time = str(self.time_functions.convert_Time(short_unix_time))
                    time_range_unix.append(short_unix_time)
                    time_range_real.append(converted_time)

                    open_range.append(float(data[i][1]))
                    high_range.append(float(data[i][2]))
                    low_range.append(float(data[i][3]))
                    close_range.append(float(data[i][4]))

                    open_close_array.append(float(data[i][1]))
                    open_close_array.append(float(data[i][4]))
                    
                    all_prices_array.append(float(data[i][1]))
                    all_prices_array.append(float(data[i][2]))
                    all_prices_array.append(float(data[i][3]))
                    all_prices_array.append(float(data[i][4]))

            except:
                pass
            self.csv_ops.write_to_CSV('csv/chart/time_range_unix.csv',time_range_unix)
            self.csv_ops.write_to_CSV('csv/chart/time_range_real.csv',time_range_real)
            self.csv_ops.write_to_CSV('csv/chart/open_range.csv',open_range)
            self.csv_ops.write_to_CSV('csv/chart/high_range.csv',high_range)
            self.csv_ops.write_to_CSV('csv/chart/low_range.csv',low_range)
            self.csv_ops.write_to_CSV('csv/chart/close_range.csv',close_range)
        return all_prices_array,open_close_array,time_range_unix,time_range_real,open_range,high_range,low_range,close_range





    def read_Klines(self):

        mins_back = int(self.txt_ops.quick_read_txt_file('txt/settings/chart/no_of_candles.txt'))

        all_prices_array = []
        open_close_array = []

        time_range_unix = self.csv_ops.read_Last_CSV_Rows('csv/chart/time_range_unix.csv',mins_back)
        time_range_real = self.csv_ops.read_Last_CSV_Rows('csv/chart/time_range_real.csv',mins_back)
        #
        open_range = self.csv_ops.read_Last_CSV_Rows('csv/chart/open_range.csv',mins_back)
        high_range = self.csv_ops.read_Last_CSV_Rows('csv/chart/high_range.csv',mins_back)
        low_range = self.csv_ops.read_Last_CSV_Rows('csv/chart/low_range.csv',mins_back)
        close_range = self.csv_ops.read_Last_CSV_Rows('csv/chart/close_range.csv',mins_back)

        for i in range(len(open_range[0])):
            all_prices_array.append(float(open_range[0][i]))
        for i in range(len(high_range[0])):
            all_prices_array.append(float(high_range[0][i]))
        for i in range(len(low_range[0])):
            all_prices_array.append(float(low_range[0][i]))
        for i in range(len(close_range[0])):
            all_prices_array.append(float(close_range[0][i]))
        
        return all_prices_array,open_close_array,time_range_unix,time_range_real,open_range,high_range,low_range,close_range









def check_Module():

    price_functions_static = Price_Functions(1)

    #get_futures_prices = price_functions_static.request_Price_Data('BTCUSDT')
    #print('\nget_futures_prices:',get_futures_prices)
        
    #get_spot_price = price_functions_static.request_Avg_Price_Data('ETHUSDT')
    #print('\nget_spot_price:',get_spot_price)

    #-----------------------------------------#

    request_klines = price_functions_static.request_Klines('ETHUSDT',5)
    print('\nrequest_klines:',request_klines)

    read_price = price_functions_static.read_Klines()
    print('\nread_price:',read_price)



if __name__== '__main__':


    check_Module()
