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
from _Precision_Manager import *
from _Maths_Functions import *
from _Time_Functions import *
from _Signals import *
from _Binance_Exceptions import *
from _Record_Stats import *
from _Balance_Functions import *
from _Array_Functions import *
from os import walk
from ast import literal_eval
from _Fetch_Settings import *

class Order_Pos_Functions():

    def __init__(self,account_no):
        #super().__init__()
        self.account_no = account_no
        self.account_settings_path = 'txt/setup/' + str(self.account_no) + '/setup_' + str(self.account_no) + '.txt'
        self.csv_ops = csv_Ops()
        self.txt_ops = txt_Ops()
        self.api_key = Logins().return_Keys(account_no)[0]
        self.secret_key = Logins().return_Keys(account_no)[1]
        self.balance_functions = Balance_Functions(account_no)
        self.maths_functions = Maths_Functions(1)
        self.price_functions = Price_Functions(1)
        self.time_functions = Time_Functions()
        self.average_sleep = 0.5
        self.check_filled_status = ''
        self.avg_fill_price = 0
        self.precision_functions = Precision_Functions(1)
        self.signal_functions = Signals(account_no)
        self.array_functions = Array_Functions()
        self.settings = Settings(account_no)


    def makeBeep(self,frequency,duration,play_times):
        for i in range(play_times):
            winsound.Beep(frequency, duration)

            



# CREATE ------------------------------------------------------------------------------------------------------------------------
    def create_Spot_Order(self,symbol,side,quantity):
        status_code = 0
        url = 'https://api.binance.com/api/v3/order'
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        params = {
            'symbol': symbol,
            'side': side,
            'type': "MARKET",
            'quantity':quantity,
            'timestamp': self.time_functions.get_Timestamp(13)
        }
        print("\nCreating a",side,"Spot MARKET order for",symbol,"| Amount:",quantity)
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'),query_string.encode('utf-8'),hashlib.sha256).hexdigest()
        r = requests.post(url, headers=headers, params=params)
        if r.status_code == 200:
            status_code=r.status_code
            data = r.json()
            print("\nSuccess: Spot order created!")
        elif r.json()['code'] == -2010:
            print(r.json()['code'])
            print("\nError: Account has insufficient balance for spot order creation!")
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())
            #print("\nSpot order creation error.")
        return status_code


        
    def create_Futures_Order(self,symbol,side,order_type,tif,price,stop_price,quantity):

        try:
            get_precision_data = self.precision_functions.read_Asset_Precision(symbol)
        except:
            get_precision_data = self.precision_functions.request_Asset_Precision(symbol)

        make_price_str = "%." + str(get_precision_data[0]) + "f"
        make_quant_str = "%." + str(get_precision_data[1]) + "f"

        #apply correct precisions
        price = float( make_price_str%(price) )
        stop_price = float( make_price_str%(stop_price) )
        quantity = float( make_quant_str%(quantity) )

        order_ID = 1

        url = 'https://fapi.binance.com/fapi/v1/order'

        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        if order_type == 'LIMIT':
            params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'timeInForce':tif,
                'price':price,
                'quantity':quantity,
                'timestamp': self.time_functions.get_Timestamp(13)
            }
            print("\nCreating LIMIT order for Account",self.account_no)

        if order_type == 'STOP':
            params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'timeInForce':tif,
                'price':price,
                'stopPrice':stop_price,
                'quantity':quantity,
                'timestamp': self.time_functions.get_Timestamp(13)
            }
            print("\nCreating STOP LOSS order for Account",self.account_no)

        if order_type == 'MARKET':
            params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity':quantity,
                'timestamp': self.time_functions.get_Timestamp(13)
            }
            print("\nCreating MARKET order for Account",self.account_no)

        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        r = requests.post(url, headers=headers, params=params)
        data = r.json()
        status_code = r.status_code
        print(data,status_code)

        if status_code == 200:

            print(order_type,"order creation successful.")
            order_ID = data['orderId']

        else:

            print(order_type,"order creation error.")

        return order_ID,data,status_code




    def create_TP_and_SL(self,pair_symbol):

        try:
            get_precision_data = self.precision_functions.read_Asset_Precision(pair_symbol)
        except:
            get_precision_data = self.precision_functions.request_Asset_Precision(pair_symbol)

        make_price_str = "%." + str(get_precision_data[0]) + "f"
        make_quant_str = "%." + str(get_precision_data[1]) + "f"


        #apply correct precisions
        #price = float( make_price_str%(price) )

        #local vars
        pos_entered = float(0.00)
        get_first_position = []
        open_pos_num = 0

        get_pos_data = self.request_Position_Information()
        print("\nget_pos_data",get_pos_data)
        
        open_pos_num = len(get_pos_data)

        if open_pos_num > 0:

            for i in range(open_pos_num):
                if pair_symbol == get_pos_data[i][0]:
                    get_first_position = get_pos_data[i]
        
            get_settings = Settings(self.account_no)
            settings = get_settings.load_Trade_Variables(pair_symbol)
            #
            split_order_segments = settings[3]
            take_profit = settings[5]
            stop_loss = settings[6]
            stop_to_limit_spread = settings[7]
            auto_sl_breach = settings[30]
            tp_type = settings[31]
            sl_type = settings[32]
            dynamic_tp = settings[19]
            dynamic_sl = settings[27]
            use_liq_sl = settings[18]

            print("\nget_first_position",get_first_position)

            if len(get_first_position) > 0:
       
                pos_amount = float(get_first_position[1])
                pos_entered = float(get_first_position[2])
                pos_side = str(get_first_position[3])
                #print("\ncreate_TP_and_SL |",get_first_position)
                #get current price
                get_price_data = self.price_functions.request_Price_Data(pair_symbol)
                current_price = get_price_data[0] #| 0 avg | 1 mark | 2 hybrid
                #print("\nCurrent price for",pair_symbol,"is",current_price)
                #LONG SIDE
                if pos_side == 'LONG':
                    #long will tp with a sell
                    enter_side = 'SELL'
                    #get mode safety and targets
                    get_long_data = self.signal_functions.mode_Safety(pair_symbol,pos_side)
                    #
                    #get_long_safe_status = get_long_data[0]
                    get_long_target = get_long_data[1]
                    min_scalp = get_long_data[3]
                    top_line = get_long_data[4]
                    bottom_line = get_long_data[5]
                    #generic fixed variable for TP/SL targets
                    take_profit_price = float(make_price_str%(pos_entered + take_profit)) 
                    stop_loss_price = float(make_price_str%(pos_entered - stop_loss))
                    if dynamic_sl == 1:
                        if current_price > gold_line:
                            stop_loss_price = float(make_price_str%(gold_line - (current_price * auto_sl_breach) ))#2 because just below avg win ratio
                    if use_liq_sl == 1:
                        liq_price = float(get_first_position[4])
                        if liq_price > 0:
                            stop_loss_price = float(make_price_str%(liq_price + (liq_price * stop_to_limit_spread))) #small increment above
                    if dynamic_tp == 1:
                        if current_price < get_long_target and get_long_target > take_profit_price:
                            take_profit_price = get_long_target
                    #applies to all
                    stop_loss_limit_price = float(make_price_str%(stop_loss_price - (pos_entered * stop_to_limit_spread)))
                #LONG SIDE
                if pos_side == 'SHORT':
                    enter_side = 'BUY'
                    #get mode safety and targets
                   
                    get_short_data = self.signal_functions.mode_Safety(pair_symbol,'SHORT')
                    #get_short_safe_status = get_short_data[0]
                    get_short_target = get_short_data[1]
                    min_scalp = get_short_data[3]
                    top_line = get_short_data[4]
                    bottom_line = get_short_data[5]
                    #generic fix variable TP/SL
                    take_profit_price = float(make_price_str%(pos_entered - take_profit)) 
                    stop_loss_price = float(make_price_str%(pos_entered + stop_loss))
                    if dynamic_sl == 1:
                        if current_price < gold_line:
                            stop_loss_price = float(make_price_str%(gold_line + (current_price * auto_sl_breach))) #2 because just below avg win ratio
                    if use_liq_sl == 1:
                        liq_price = float(get_first_position[4])
                        if liq_price > 0:
                            stop_loss_price = float(make_price_str%(liq_price-(liq_price * stop_to_limit_spread))) #small increment above
                    if dynamic_tp == 1:
                        if current_price > get_short_target and get_short_target < take_profit_price:
                            take_profit_price = get_short_target
                    #universal
                    stop_loss_limit_price = float(make_price_str%(stop_loss_price + (pos_entered * stop_to_limit_spread)))
                #create take profit
                if tp_type == 'FULL':
                    self.create_Futures_Order(pair_symbol,enter_side,'LIMIT','GTC',take_profit_price,0,float(make_quant_str%(pos_amount)))
                elif tp_type == 'HALF':
                    self.create_Futures_Order(pair_symbol,enter_side,'LIMIT','GTC',take_profit_price,0,float(make_quant_str%(pos_amount/2)))
                elif tp_type == 'NONE':
                    pass
                else:
                    self.create_Futures_Order(pair_symbol,enter_side,'LIMIT','GTC',take_profit_price,0,float(make_quant_str%(pos_amount)))
                #time.sleep(0.1)
                if sl_type == 'FULL':
                    self.create_Futures_Order(pair_symbol,enter_side,'STOP','GTC',stop_loss_price,stop_loss_limit_price,float(make_quant_str%(pos_amount)))
                elif sl_type == 'HALF':
                    self.create_Futures_Order(pair_symbol,enter_side,'STOP','GTC',stop_loss_price,stop_loss_limit_price,float(make_quant_str%(pos_amount/2)))
                elif sl_type == 'NONE':
                    pass
                else:
                    self.create_Futures_Order(pair_symbol,enter_side,'STOP','GTC',stop_loss_price,stop_loss_limit_price,float(make_quant_str%(pos_amount)))

                print(take_profit_price,stop_loss_price,pos_amount)


                busy_str_pair = 'txt/setup/' + str(self.account_no) + '/setup_' + str(self.account_no) + '_' + str(pair_symbol) + '.txt'
                self.txt_ops.replace_Specific_Line(busy_str_pair,2,'busy=0')      

                busy_str_account = 'txt/setup/' + str(self.account_no) + '/setup_' + str(self.account_no) + '.txt'
                self.txt_ops.replace_Specific_Line(busy_str_account,2,'busy=0')

            
# REQUEST ------------------------------------------------------------------------------------------------------------------------




            

    def request_Open_Orders_Data(self):

        account_settings_path = 'txt/setup/' + str(self.account_no) + '/setup_' + str(self.account_no) + '.txt'

        open_array = []

        url = 'http://fapi.binance.com/fapi/v1/openOrders'

        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        params = {
            'limit':16,
            'recvWindow':5000,
            'timestamp':self.time_functions.get_Timestamp(13)
        }

        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'),query_string.encode('utf-8'),hashlib.sha256).hexdigest()
        r = requests.get(url,headers=headers,params=params)

        if r.status_code == 200:

            data = r.json()
            open_orders_num = len(data)

            if open_orders_num > 0:

                for i in range(open_orders_num):
                    open_order_id = data[i]['orderId']
                    symbol = data[i]['symbol']
                    side = data[i]['side']
                    amount = data[i]['origQty']
                    price = data[i]['price']
                    stop_price = data[i]['stopPrice']
                    status = data[i]['status']
                    order_type = data[i]['type']
                    row = [open_order_id,symbol,side,amount,price,stop_price,status,order_type]
                    open_array.append(row)

                set_string = 'open_orders=' + str(open_array)
                self.txt_ops.replace_Specific_Line(account_settings_path,7,set_string)

            else:

                set_string = 'open_orders=[]'
                self.txt_ops.replace_Specific_Line(account_settings_path,7,set_string)  
          
        else:
            print("\nRequest open orders error, skipping...")
        return open_array



    def request_Open_Orders_Data_Symbol(self,symbol):
        #clear CSV file
        file_path = 'txt/setup/' + str(self.account_no) + '/setup_' + str(self.account_no) + '_' + str(pair_symbol) + '.txt'
        open_array = []
        url = 'http://fapi.binance.com/fapi/v1/openOrders'
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        params = {
            'limit':16,
            'recvWindow':5000,
            'symbol':symbol,
            'timestamp':self.time_functions.get_Timestamp(13)
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'),query_string.encode('utf-8'),hashlib.sha256).hexdigest()
        r = requests.get(url,headers=headers,params=params)
        if r.status_code == 200:
            data = r.json()
            open_orders_num = len(data)
            if open_orders_num > 0:
                for i in range(open_orders_num):
                    open_order_id = data[i]['orderId']
                    symbol = data[i]['symbol']
                    side = data[i]['side']
                    amount = data[i]['origQty']
                    price = data[i]['price']
                    stop_price = data[i]['stopPrice']
                    status = data[i]['status']
                    order_type = data[i]['type']
                    row = [open_order_id,symbol,side,amount,price,stop_price,status,order_type]
                    open_array.append(row)

                set_string = 'open_orders=' + str(open_array)
                self.txt_ops.replace_Specific_Line(pair_settings_path,36,set_string)

            elif open_orders_num == 0:
                set_string = 'open_orders=[]'
                self.txt_ops.replace_Specific_Line(pair_settings_path,36,set_string)





                   
        else:
            print("\nRequest open orders error, skipping...")
        return open_array



    def check_Order_Filled_Status(self,pair_symbol,my_order_id):
        url = 'http://fapi.binance.com/fapi/v1/order'
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        params = {
            'symbol':pair_symbol,
            'orderId':my_order_id,
            'timestamp':self.time_functions.get_Timestamp(13)
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'),query_string.encode('utf-8'),hashlib.sha256).hexdigest()
        r = requests.get(url,headers=headers,params=params)
        if r.status_code == 200:
            data = r.json()
            self.check_filled_status = data['status']
            self.avg_fill_price = float(data['avgPrice'])
        print("\nChecking fill status of order:",my_order_id,"|",pair_symbol,"| Status:",self.check_filled_status)
        return self.check_filled_status,self.avg_fill_price

    def request_Last_Orders_Data(self,symbol):
        time.sleep(self.average_sleep)
        last_orders_array = []
        url = 'http://fapi.binance.com/fapi/v1/allOrders'
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        params = {
            'limit':1,
            'symbol':symbol,
            'recvWindow':5000,
            'timestamp':self.time_functions.get_Timestamp(13)
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'),query_string.encode('utf-8'),hashlib.sha256).hexdigest()
        r = requests.get(url,headers=headers,params=params)
        if r.status_code == 200:
            data = r.json()
            data_length = len(data)
            if data_length > 0:
                for i in range(data_length):
                    last_order_id = data[i]['orderId']
                    last_order_status = data[i]['status']
                    last_order_amount = data[i]['origQty']                        
                    last_order_side = data[i]['side']
                    last_order_price = data[i]['price']
                    last_order_time = data[i]['time']
                    last_order_avg_price = data[i]['avgPrice']
                    row = [last_order_time,last_order_id,last_order_status,last_order_amount,last_order_side,last_order_price,last_order_avg_price]
                    last_orders_array.append(row)
        else:
            print("\nError: Request last orders fetch.")

        return last_orders_array




    def fetch_Last_Order_Status(self,symbol):
        last_order_status = ''
        get_data = self.request_Last_Orders_Data(symbol)
        if len(get_data) > 0:
            last_order_array = get_data[-1]
            last_order_status = last_order_array[2]
        return last_order_status




    def request_Position_PNL(self,symbol):

        #vars
       
        pnl_str = ''
        pnl = 0
        #
        url = 'http://fapi.binance.com/fapi/v2/positionRisk'

        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        params = {
            'timestamp':self.time_functions.get_Timestamp(13),
            'recvWindow':5000,
            'limit':1,
            'symbol':symbol
        }

        query_string = urlencode(params)

        params['signature'] = hmac.new(self.secret_key.encode('utf-8'),query_string.encode('utf-8'),hashlib.sha256).hexdigest()

        r = requests.get(url,headers=headers,params=params)

        if r.status_code == 200:

            data = r.json()

            if len(data)>0:

                #print(data)

            

                pnl_str = data[-1]['unRealizedProfit']
                pnl = float(pnl_str)
                pnl = float("%.2f"%(pnl))

        
        

        return pnl






    def check_Position_With_Symbol_Active(self,symbol):
        found = 0
        get_pos_array = self.request_Position_Information()
        no_of_active_positions = len(get_pos_array)
        for i in range(no_of_active_positions):
            if get_pos_array[i][0] == symbol:
                print("Position with symbol already active!")
                found = 1
                break
            else:
                found = 0
        return found





    def cancel_All_Open_Orders_Symbol(self,pair_symbol):
        url = 'http://fapi.binance.com/fapi/v1/allOpenOrders'
        headers = {
            'X-MBX-APIKEY':self.api_key
        }
        print("\nCancelling all open orders with pair symbol",pair_symbol + str('...'))
        params = {
            'symbol':pair_symbol,
            'timestamp':self.time_functions.get_Timestamp(13)
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'),query_string.encode('utf-8'),hashlib.sha256).hexdigest()
        r = requests.delete(url,headers=headers,params=params)
        if r.status_code == 200:
            print("\nSuccess: Cancelled all open orders for Account:",self.account_no,"|",pair_symbol)
        else:
            print("\nError: Unknown cancel open orders issue in Account:",self.account_no,"|",pair_symbol)



    def cancel_All_Open_Orders(self):

        self.cancel_All_Open_Orders_Symbol('BTCUSDT')
        self.cancel_All_Open_Orders_Symbol('ADAUSDT')
        self.cancel_All_Open_Orders_Symbol('ETHUSDT')
        self.cancel_All_Open_Orders_Symbol('LTCUSDT')
        self.cancel_All_Open_Orders_Symbol('BNBUSDT')

    def force_Close_Position(self,pair_symbol):

        self.cancel_All_Open_Orders_Symbol(pair_symbol)

        
        #count positions
        get_pos_data = self.request_Position_Information()
        pos_num = len(get_pos_data)
        if pos_num > 0:


            for i in range(pos_num):

                if get_pos_data[i][0] == pair_symbol:
        
         
                    pos_amount = float(get_pos_data[i][1])
                    pos_entry = float(get_pos_data[i][2])
                    pos_side = str(get_pos_data[i][3])

                    if pos_side == 'LONG':
                        enter_side = 'SELL'
                    elif pos_side == 'SHORT':
                        enter_side = 'BUY'
                    #create market order for immediate sell/buy
                    self.create_Futures_Order(pair_symbol,enter_side,'MARKET','null',0,0,abs(pos_amount))
                    break
                else:
                    print("\nWarning: There are no open positions to force close, ignoring...")


    
# READ ------------------------------------------------------------------------------------------------------------------------

    def convert_String_Array_To_Real(self,input_string):
        filtered_array = literal_eval(input_string)
        return filtered_array

    

    def process_Open_Orders_Data(self,pair_symbol):

        print('\n┌----------------------------- ORDER POS FUNCTIONS | Process Order Data -----------------------------┐')
        open_orders_num = 0
        make_tp_string = ''
        make_sl_string = ''
        make_entry_string = ''
        TP_amount = float(0.00)
        TP_price = float(0.00)
        SL_amount = float(0.00)
        SL_price = float(0.00)
        ENT_amount = float(0.00)
        ENT_price = float(0.00)
        busy_val = 0
        settings_dict = {}
        pos_amount = 0
        
        #get open_orders_num via read
        read_orders_data = self.read_Open_Orders_Data_Symbol(pair_symbol)
        open_orders_num = len(read_orders_data)

        settings_path = 'txt/setup/' + str(self.account_no) + '/setup_' + str(self.account_no) + '_' + str(pair_symbol) + '.txt'

        if os.path.isfile(settings_path):
            settings_dict = self.txt_ops.create_dict_from_txt(settings_path,'=')
            #print(settings_array)
            busy_val = int(settings_dict['busy'])
            pos_amount = float(settings_dict['quantity_to_trade'])
            #print(settings_array)

            if open_orders_num > 0:

                for i in range(open_orders_num):  #row = [open_order_id,symbol,side,amount,price,stop_price,status,order_type]
                    if read_orders_data[i][1] == pair_symbol:

                        if read_orders_data[i][7] == 'STOP':
                            SL_amount = float("%.4f"%(float(read_orders_data[i][3])))
                            SL_price = float("%.4f"%(float(read_orders_data[i][4])))
                        if read_orders_data[i][7] == 'LIMIT':
                            get_this_order_amount = float("%.4f"%(float(read_orders_data[i][3])))
                            if busy_val == 0: #get_this_order_amount >= pos_amount:
                                TP_amount = float("%.4f"%(float(read_orders_data[i][3])))
                                TP_price = float("%.4f"%(float(read_orders_data[i][4])))
                            elif busy_val == 1:
                                ENT_amount = float("%.4f"%(float(read_orders_data[i][3])))
                                ENT_price = float("%.4f"%(float(read_orders_data[i][4])))


            #make TP/Max order string
            make_tp_string = str(TP_amount) + ' @ ' + str(TP_price)
            make_sl_string = str(SL_amount) + ' @ ' + str(SL_price)
            make_entry_string = str(ENT_amount) + ' @ ' + str(ENT_price)
            if TP_amount == 0:
                make_tp_string = ''
            if SL_amount == 0:
                make_sl_string = ''
            if ENT_amount == 0:
                make_entry_string = ''
        else:

            print("\nError: Pair symbol settings file does not exist!")


        print('\n└--------------------------- ORDER POS FUNCTIONS | END Process Order Data ---------------------------┘\n\n')
        return open_orders_num,make_tp_string,make_sl_string,make_entry_string








    def check_Afford(self,symbol):
        print('\n┌----------------------------- ORDER POS FUNCTIONS | Check Afford -----------------------------┐')
        #1 get account balance, margin
        #2 check max symbol that can be bought, check if it is more than Binance min
        get_amount_dict = {}
        leverage = 6
        can_afford = 0
        can_afford_amount = 0
        min_allowed = 0
        get_amount_from_settings = 0
        get_account_balances = 0

        get_amount_from_settings_str = 'txt/setup/' + str(self.account_no) + '/setup_' + str(self.account_no) + '_' + str(symbol) + '.txt'

        get_amount_dict = self.txt_ops.create_dict_from_txt(get_amount_from_settings_str,'=')


        get_amount_from_settings = float(  get_amount_dict['quantity_to_trade']   )



        print('\nget_amount_from_settings',get_amount_from_settings)


        try:
            get_account_balances = self.balance_functions.request_Futures_Balances()
            get_margin = get_account_balances[1]
        except:
            get_margin = 0


        
        balance = get_margin * 0.99
        balance = balance * leverage
        print('\nbalance with lev',balance)

        cur_symbol_prices = self.price_functions.request_Price_Data(symbol)
        hybrid_price = cur_symbol_prices[2]
        cur_price = hybrid_price
        print('\ncur_price',cur_price)

        can_afford_amount = balance / cur_price
        can_afford_amount = float("%.2f"%(can_afford_amount))
        print('\ncan_afford_amount',can_afford_amount)

        if can_afford_amount >= get_amount_from_settings:
            can_afford = 1

        print('\ncan_afford',can_afford)
        print('\n└--------------------------- ORDER POS FUNCTIONS | END Check Afford ---------------------------┘\n\n')
        return can_afford, get_amount_from_settings



    def check_Symbol_Entering(self):
        is_busy = 0
        make_str = ''
        symbols_array = ['BTCUSDT','ETHUSDT','BNBUSDT','LTCUSDT','ADAUSDT']
        for i in range(len(symbols_array)):
            is_busy = int(self.settings.load_Trade_Variables(symbols_array[i])[1])
            print(symbols_array[i],is_busy)
            if is_busy == 1:
                make_str = 'Creating ' + symbols_array[i] + ' position...'
                break
        print(make_str)
        return make_str
                


        
        

  

    def check_Order_Clash(self,pair_symbol):
        print('\n┌----------------------------- ORDER POS FUNCTIONS | Check Open Order Symbol Clash -----------------------------┐')
        order_exists = 0
        other_symbol = ''
        order_array = []
        no_of_open_match = 0

        #check if a position with symbol already exists and is running...
       
        request_order_data = self.request_Open_Orders_Data()

        #print(request_order_data)

        
        order_num = len(request_order_data)
        print("\nCurrently open order symbols:\n")
        if order_num > 0:
            
            for i in range(order_num):

                cur_symbol = request_order_data[i][1]
                print(cur_symbol)
                
                if cur_symbol == pair_symbol:
                    print("\nAn order with the symbol",pair_symbol,"is already open, waiting for fill...")
                    order_exists = 1
                    break

        elif order_num == 0:
            order_exists = 0
        print('\n└--------------------------- ORDER POS FUNCTIONS | END Check Open Order Symbol Clash ---------------------------┘\n\n')
        return order_exists



    def find_Max_Pos(self):
        pass

        


          
    def check_Sides_Balance(self,side):
        print('\n┌--------------------------- ORDER POS FUNCTIONS | Sides Balance ---------------------------┐')
        #ensures a balance between long and short positions is maintained
        max_pos = 5 #should come from no of setup files

       
        side_limit = math.ceil(max_pos / 2)
        print('\n\nAUTO SAME SIDE LIMIT:',side_limit,'\n\n')
        
        

        side_array = []
        cur_side = ''
        str_long = 'LONG'
        str_short = 'SHORT'
        short_count = 0
        long_count = 0
        duplicateFrequencies = {}
        clash = 0

        #request currently open position data
        request_pos_data = self.request_Position_Information()
        pos_num = len(request_pos_data)
        #print('\nrequest_pos_data',request_pos_data)

        if pos_num > 0:
        
            for j in range(pos_num):
               
                cur_side = request_pos_data[j][3]

                side_array.append(cur_side)

            print('\n\nSide array:',side_array)


           
            
            for i in set(side_array):
                duplicateFrequencies[i] = side_array.count(i)



            try:
                short_count = duplicateFrequencies['SHORT']
            except:
                short_count = 0
                



            try:
                long_count = duplicateFrequencies['LONG']
            except:
                long_count = 0


                


            if side == 'LONG' and long_count >= side_limit:
                clash = 1
                print('\nUNSAFE: There are too many LONG positions open already, waiting...\n')
            elif side == 'LONG' and long_count < side_limit:
                print('\nSAFE: LONG positions are go...\n')
            if side == 'SHORT' and short_count >= side_limit:
                clash = 1
                print('\nUNSAFE: There are too many SHORT positions open already, waiting...\n')
            elif side == 'SHORT' and short_count < side_limit:
                print('\nSAFE: SHORT positions are go...\n')

        
        print('\n└------------------------- ORDER POS FUNCTIONS | END Sides Balance -------------------------┘\n\n')
        return clash

                


        

    def filter_All_Active_Symbols_In_Folder(self):
        filtered_array = []
        filtered_array_2 = []
        folder_path = 'txt/setup/' + str(self.account_no) + '/'
        list_array = self.maths_functions.list_All_Files_In_Folder(folder_path)
        length = len(list_array)
        for i in range(length):
            make_str = list_array[i]
            if make_str.find('USD') > 0:
                r_string = str(re.findall('([A-Z]+)', make_str))
                valids = re.sub(r"[^A-Za-z]+", '', r_string)
                filtered_array.append(valids)
        for i in range(len(filtered_array)):
            full_path = folder_path + 'setup_' + str(self.account_no) + '_' + filtered_array[i] + '.txt'
            create_dict = self.txt_ops.create_dict_from_txt(full_path,'=')
            active_value = int(create_dict['active'])
            #print(full_path,active_value)
            if active_value == 1:
                filtered_array_2.append(filtered_array[i])
        print("\nAllowed symbols list as defined by User:",filtered_array_2)
        return filtered_array_2
            








    def determine_Position_Next(self):


        print('\n┌--------------------------- ORDER POS FUNCTIONS | Determine Next Position ---------------------------┐')


        def difference(lst1, lst2):
            lst3 = [value for value in lst1 if value not in lst2]
            return lst3

        #within a single account

        #1 Check if a position is already open, if it is, find next available pair symbol, try and enter
        #2 If no positions are open, grab first position allowed from list, try and enter
        #3 If all positions exist and are currently active, return 'all_occupied' and wait
        #4 return symbol, file_path to settings

        file_path = ''
        next_symbol = 'NONE'
        current_open_array = []
        all_symbols_array = []
        allowed_symbols_array = []
        intersect_array = []
        filtered_array = []
        init_dict = {}
        
        can_afford = 0

        #request currently open position data
        request_pos_data = self.request_Position_Information()
        pos_num = len(request_pos_data)
        #print('\nrequest_pos_data',request_pos_data)


        #gather allowed symbols, reads txt/setup folders
        #if a settings file exists for a pair symbol, it means it is allowed
        folder_path = 'txt/setup/' + str(self.account_no) + '/'
        all_symbols_array = self.maths_functions.filter_All_Symbols_In_Folder(folder_path)
        print('\nAll symbols with settings files:',all_symbols_array)
        allowed_symbols_array = self.filter_All_Active_Symbols_In_Folder()


        if pos_num == 0:
            if len(allowed_symbols_array) > 0:
                next_symbol = allowed_symbols_array[0]
                file_path = folder_path + 'setup_' + str(self.account_no) + '_' + next_symbol + '.txt'
                can_afford = self.check_Afford(next_symbol)[0]

        if pos_num > 0:
            
            for i in range(pos_num):
                cur_pos_symbol = request_pos_data[i][0]
                current_open_array.append(cur_pos_symbol)

            print('\nCurrently running symbols:',current_open_array)

            #find intersect with allowed
            
            intersect_array = difference(all_symbols_array,current_open_array)

            print('\nSymbols free for entry pending user permissions:',intersect_array)


            if len(intersect_array) > 0:
                for i in range(len(intersect_array)):
                    symbol_name = intersect_array[i]
                    file_name_path = folder_path + 'setup_' + str(self.account_no) + '_' + symbol_name + '.txt'
                    init_dict = self.txt_ops.create_dict_from_txt(file_name_path,'=')
                    active_val = int(init_dict['active'])
                    if active_val == 1:
                        filtered_array.append(symbol_name)


            
            print('\nSymbols free for entry, with permission from user:',filtered_array)


           
         

            if len(filtered_array) > 0:
                next_symbol = filtered_array[0]
                file_path = folder_path + 'setup_' + str(self.account_no) + '_' + next_symbol + '.txt'
                can_afford = self.check_Afford(next_symbol)[0]



        print('\n└------------------------- ORDER POS FUNCTIONS | END Determine Next Position -------------------------┘\n\n')
        return next_symbol,can_afford,file_path











    def request_Position_Information(self):
        #print("\n\n┌-------- ORDER POS FUNCTIONS | REQUESTING POSITION DATA --------┐\n\n")
        row = []
        pos_array = []
        symbol = ''
        amount = 0
        entry_price = 0
        pos_side = ''
        liq_price = 0
        file_path = 'txt/setup/' + str(self.account_no) + '/setup_' + str(self.account_no) + '.txt'
        url = 'http://fapi.binance.com/fapi/v2/positionRisk'
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        params = {
            'timestamp':self.time_functions.get_Timestamp(13),
            'recvWindow':5000,
            'limit':6
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.secret_key.encode('utf-8'),query_string.encode('utf-8'),hashlib.sha256).hexdigest()
        r = requests.get(url,headers=headers,params=params)
        if r.status_code == 200:
            data = r.json()
            if len(data) == 0:
                set_string = 'open_positions=[]'
                self.txt_ops.replace_Specific_Line(file_path,10,set_string)
            if len(data) > 0:
                for i in range(len(data)):
                    #grab relevant fields
                    amount = float(data[i]['positionAmt'])
                    #abs forces positive integers
                    abs_amount = abs(amount)
                    #check if amount is not zero
                    if abs_amount > 0:
                    #if the amount is negative side is short, vice versa
                        if amount < 0:
                            pos_side = 'SHORT'
                        elif amount > 0:
                            pos_side = 'LONG'
                        #now we load the rest of the fields
                        symbol = str(data[i]['symbol'])
                        entry_price = float("%.2f"%(float(data[i]['entryPrice'])))
                        liq_price = float("%.2f"%(float(data[i]['liquidationPrice'])))
                        #create a row from vars
                        row = [symbol,abs_amount,entry_price,pos_side,liq_price]
                        #append to pos_array
                        pos_array.append(row)
                        #print("Active position:",abs_amount,symbol,pos_side,"since",entry_price,"\n")
                set_string = 'open_positions=' + str(pos_array)
                self.txt_ops.replace_Specific_Line(file_path,8,set_string)
        #print("\n└------ ORDER POS FUNCTIONS | END REQUESTING POSITION DATA ------┘\n\n")
        return pos_array


    def read_Position_Data(self):
        cell_id = 'open_positions'
        orders_array = self.txt_ops.get_Array_From_Txt_Dict(self.account_settings_path,cell_id,'=')
        return orders_array


    def determine_Max_Pos_For_Account(self):
        print("┌-------- ORDER POS FUNCTIONS | FIND MAX POS --------┐\n\n")
        folder_path = 'txt/setup/' + str(self.account_no) + '/'
        f = []
        counter = 0
        for (dirpath, dirnames, filenames) in walk(folder_path):
            f.extend(filenames)
            break
        for i in range(len(f)):
            if 'ADA' in f[i]:
                counter += 1
            if 'ETH' in f[i]:
                counter += 1
            if 'BTC' in f[i]:
                counter += 1
            if 'LTC' in f[i]:
                counter += 1
            if 'BNB' in f[i]:
                counter += 1
        print("\nThe max positions value for account",self.account_no,"is",counter)
        print("\n\n\n└------ ORDER POS FUNCTIONS | END FIND MAX POS ------┘")
        return counter






    def reset_All_Busy_Vars(self):

        print("┌-------- ORDER POS FUNCTIONS | RESET ALL BUSY --------┐\n\n")
        
        def replace_In_Folder(account_no):

            folder_path = 'txt/setup/' + str(account_no) + '/'
            file_array = []
            for (dirpath, dirnames, filenames) in walk(folder_path):
                file_array.extend(filenames)
                break
            for i in range(len(file_array)):
                file_path = file_array[i]
                self.txt_ops.replace_Specific_Line(folder_path+file_path,2,'busy=0')
                print("\nReset busy to 0 in",folder_path+file_path)

        #single use:
        #replace_In_Folder(self.account_no)
        
        #apply to all folders (accounts)
        folder_count = self.maths_functions.count_Folders('txt/setup/')
        for h in range(folder_count):
            replace_In_Folder(h+1)
            

            
       


        print("\n\n\n└------ ORDER POS FUNCTIONS | END RESET ALL BUSY ------┘")
      



    def read_Open_Orders_Data(self):
        cell_id = 'open_orders'
        orders_array = self.txt_ops.get_Array_From_Txt_Dict(self.account_settings_path,cell_id,'=')
        return orders_array
        

    def read_Open_Orders_Data_Symbol(self,pair_symbol):

        filtered_array = []
        row = []
        
        orders_array = self.read_Open_Orders_Data()
        #print('orders_array',orders_array)
        length = len(orders_array)
        
        if length > 0:
            for i in range(length):
                order_symbol = orders_array[i][1]
                #print('order_symbol',order_symbol)
                if order_symbol == pair_symbol:
                    order_id = orders_array[i][0]
                    order_side = orders_array[i][2]
                    order_amount = orders_array[i][3]
                    order_price = orders_array[i][4]
                    order_stop_price = orders_array[i][5]
                    order_status = orders_array[i][6]
                    order_type = orders_array[i][7]
                    row = [order_id,order_symbol,order_side,order_amount,order_price,order_stop_price,order_status,order_type]
                    filtered_array.append(row)
        print('\n\nfiltered_array',filtered_array)
        return filtered_array


    def remove_Orphan_Orders(self):

        print('\n┌-------------------- ORDER POS FUNCTIONS | Remove Orphan Orders --------------------┐')

        #the difference between these two arrays will be the orphan order symbol
        orders_symbols_array = []
        pos_symbols_array = []

        #busy_val ensures that entry orders are not treated as orphans
        busy_val = 0

        #count orphan orders
        counter = 0
        order_num = 0
        pos_num = 0
        intersect_array = []

        #get global account settings
        account_settings_path = 'txt/setup/' + str(self.account_no) + '/setup_' + str(self.account_no) + '.txt'
        settings_dict = self.txt_ops.create_dict_from_txt(account_settings_path,'=')
        
        #fill busy_val
        busy_val = int(settings_dict['busy'])

        if busy_val == 0:

            get_open_orders_data = self.request_Open_Orders_Data()
            open_orders_num = len(get_open_orders_data)

            #collect all open order symbols
            if open_orders_num > 0:
                for j in range(open_orders_num):
                    order_symbol = get_open_orders_data[j][1]
                    orders_symbols_array.append(order_symbol)

                #remove duplicates
                orders_symbols_array = list(dict.fromkeys(orders_symbols_array))

                order_num = len(orders_symbols_array)

                #print("\nOpen order symbols:",orders_symbols_array,len(orders_symbols_array))

                #now get the positions array
                request_pos_data = self.request_Position_Information()
                pos_num = len(request_pos_data)

                #again, append all position sumbols to new array pos_symbols_array
                if pos_num > 0:
                    for k in range(pos_num):
                        pos_symbol = request_pos_data[k][0]
                        pos_symbols_array.append(pos_symbol)
                    
                print("\n Position symbols:",pos_symbols_array,len(pos_symbols_array))
                print("\n Open order symbols:",orders_symbols_array,len(orders_symbols_array))

                #only attempt removal if orders exist 
                if order_num > 0:
                    intersect_array = self.array_functions.difference(pos_symbols_array,orders_symbols_array)
                    if len(intersect_array) > 0:
                        for i in range(len(intersect_array)):
                            current_symbol = intersect_array[i]
                            cancel_order = self.cancel_All_Open_Orders_Symbol(current_symbol)
                            counter += 1
                            self.makeBeep(2500,140,4)
                            print("\n -- Orphan order",current_symbol,"cancelled!")
                    else:
                        print("\n -- No orphan orders found...")

        record_stats = Record_Stats(self.account_no)
        record_stats.request_Write_USDT_Balance()

        print('\n└------------------ ORDER POS FUNCTIONS | END Remove Orphan Orders ------------------┘\n\n')

        return counter




def check_Module():
    #precise_list = ['BTCUSDT','ETHUSDT','LTCUSDT','BNBUSDT','ADAUSDT']
    order_pos_functions = Order_Pos_Functions(2)
    a = order_pos_functions.check_Symbol_Entering()
    #print(a)


    #a = order_pos_functions.create_TP_and_SL('BTCUSDT')    
    #for i in range(len(precise_list)):
        #get_precise = order_pos_functions.get_Asset_Precision(precise_list[i])
        #print(precise_list[i],get_precise)


    

if __name__== '__main__':


    check_Module()
