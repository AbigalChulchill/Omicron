print("\nLoading REQUESTS MANAGER...\n")

import sys
sys.path.insert(1,'lib')
import requests
import time
import sched
import os
from _csv_Ops import *
from _Crash_Manager import *
from _Order_Pos_Functions import *
from _Maths_Functions import *
from _Withdraw_Functions import *
from _txt_Ops import *
from _Time_Functions import *
from _Price_Functions import *
from _Balance_Functions import *
from _Signals import *

txt_ops = txt_Ops()
csv_ops = csv_Ops()

#get pid for this process
pid_requests = os.getpid()
txt_ops.quick_write_txt_file('txt/pids/pid_requests.txt',pid_requests)

#refresh function needs import sched,time
s = sched.scheduler(time.time, time.sleep)
client_timeout=30
rec_window = 5000

#System init variables
pair_symbol = ''
loop_cycle = 0




class NetworkError(RuntimeError):
    pass
def retryer(func):
    retry_on_exceptions=(
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError
        )
    def inner(*args,**kwargs):
        for i in range(10):
            try:
                resgold=func(*args,**kwargs)
            except retry_on_exceptions:
                time.sleep(5)
                continue
            else:
                return resgold
        else:
            raise NetworkError
    return inner


@retryer
def Looper(sc):


##    try:
##        c = Crash_Manager()
##        run_check = c.check_Modules_Alive()
##    except:
##        print("\nError: Can't check module health.")

    

    global loop_cycle
    loop_cycle += 1

    
    #get TAB account details
    tab_account = int(txt_ops.quick_read_txt_file('txt/last_tab_account.txt'))

    if tab_account != 0:
        
        print("\n---------------------------------------------")
        print("\nREQUESTS MANAGER | Tab account:",tab_account,"| Scan Cycle:",loop_cycle)
        print("\n---------------------------------------------")

        #load external functions
        price_functions = Price_Functions(tab_account)
        balance_functions = Balance_Functions(tab_account)
        order_pos_functions = Order_Pos_Functions(tab_account)
        maths_functions = Maths_Functions(tab_account)

        #functions that reads pair symbol from relevant combobox (settings or positions)
        def read_Pair_Symbol(combo_name):
            print('\n┌--------------------------- REQUESTS MANAGER | READ SYMBOL ---------------------------┐\n')
            account_dict = {}
            tab_account = int(txt_ops.quick_read_txt_file('txt/last_tab_account.txt'))
            account_path = 'txt/setup/' + str(tab_account) + '/setup_' + str(tab_account) + '.txt'
            account_dict = txt_ops.create_dict_from_txt(account_path,'=')
            if combo_name == 'settings':
                pair_symbol = account_dict['last_combo_settings']
                print("\nRead symbol from positions combo box:",pair_symbol)
            elif combo_name == 'positions':
                pair_symbol = account_dict['last_combo_pos']
                print("\nRead symbol from positions combo box:",pair_symbol)
            else:
                pair_symbol = 'BTCUSDT'
                print("\nUsing default pair symbol BTCUSDT...")
            print('\n\n└------------------------- REQUESTS MANAGER | END READ SYMBOL -------------------------┘\n\n')
            return pair_symbol


        #get pair symbol for chart data
        settings_pair = ''
        try:
            settings_pair = read_Pair_Symbol('settings')
        except:
            settings_pair = 'BTCUSDT'



##        def get_Write_Klines_For_Chart(pair_symbol):
##            all_prices_array_tab = []
##            print('\n┌--------------------------- REQUESTS MANAGER | READ KLINES ---------------------------┐\n')
##            no_of_candles = int(txt_ops.quick_read_txt_file('txt/settings/chart/no_of_candles.txt'))
##            all_prices_array_tab = price_functions.request_Klines_For_Chart(pair_symbol,no_of_candles)[0]
##            print('\n\n└------------------------- REQUESTS MANAGER | END READ KLINES -------------------------┘\n\n')
##
##        try:
##            get_Write_Klines_For_Chart(settings_pair)
##        except:
##            print('\nError fetching klines data for chart, skipping...')
##
##
##
##        def get_Write_Prices_For_Chart(pair_symbol):
##
##            print('\n┌--------------------------- REQUESTS MANAGER | REQUEST PRICES FOR CHART ---------------------------┐\n')
##            get_prices = price_functions.request_Price_Data(settings_pair)
##            get_spot = price_functions.request_Avg_Price_Data(settings_pair)
##            print('\nPrices data array:',get_prices)
##            average = get_prices[0]
##            mark = get_prices[1]
##            hybrid = get_prices[2]
##
##            current_futures_price_str = 'txt/data/chart/price_average.txt'
##            current_mark_price_str = 'txt/data/chart/price_mark.txt'
##            current_hybrid_price_str = 'txt/data/chart/price_hybrid.txt'
##            current_exchange_price_str = 'txt/data/chart/price_spot.txt'
##            
##            txt_ops.quick_write_txt_file_plus(current_futures_price_str,average)
##            txt_ops.quick_write_txt_file_plus(current_mark_price_str,mark)
##            txt_ops.quick_write_txt_file_plus(current_hybrid_price_str,hybrid)
##            txt_ops.quick_write_txt_file_plus(current_exchange_price_str,get_spot)
##            print('\n\n└------------------------- REQUESTS MANAGER | END REQUEST PRICES FOR CHART -------------------------┘\n\n')
##
##        try:
##            get_Write_Prices_For_Chart(settings_pair)
##        except:
##            print('\nError fetching price data for chart, skipping...')
##

##        def get_Gold_Silver_For_Chart(pair_symbol):
##            print('\n┌--------------------------- REQUESTS MANAGER | REQUEST GOLD SILVER FOR CHART ---------------------------┐\n')
##            no_of_candles = int(txt_ops.quick_read_txt_file('txt/settings/chart/no_of_candles.txt'))
##            all_prices_array_tab = price_functions.request_Klines_For_Chart(pair_symbol,no_of_candles)[0]
##            get_gold_data_tab = maths_functions.calc_Gold_Silver(pair_symbol,all_prices_array_tab)
##            print(get_gold_data_tab)
##            print('\n\n└------------------------- REQUESTS MANAGER | END REQUEST GOLD SILVER FOR CHART -------------------------┘\n\n')
##
##        try:
##            get_Gold_Silver_For_Chart(settings_pair)
##        except:
##            print('\nError fetching gold/silver data for chart, skipping...')





    ###### FOR OMICRON GUI #############################################################################################################




        positions_pair = ''
        try:
            positions_pair = read_Pair_Symbol('positions')
        except:
            print('\nError reading positions pair symbol, skipping... (BTCUSDT default)')
            positions_pair = 'BTCUSDT'

 

        def get_Write_Price_Data_For_UI(pair_symbol):

            print('\n┌-------------------------- REQUESTS | GET PRICE DATA --------------------------┐')
            
            get_tab_prices = price_functions.request_Price_Data(pair_symbol)

            print('\nPrices data array:',get_tab_prices)
            
            average = get_tab_prices[0]
            mark = get_tab_prices[1]
            hybrid = get_tab_prices[2]

            #current_exchange_price_str = 'txt/tab_data/prices/price_spot.txt'
            
            txt_ops.quick_write_txt_file_plus('txt/tab_data/prices/price_average.txt',average)
            txt_ops.quick_write_txt_file_plus('txt/tab_data/prices/price_mark.txt',mark)
            txt_ops.quick_write_txt_file_plus('txt/tab_data/prices/price_hybrid.txt',hybrid)

            print('\n└------------------------ REQUESTS | END GET PRICE DATA ------------------------┘\n\n')


        try:
            get_Write_Price_Data_For_UI(positions_pair)
        except:
            print('\nError fetching price data for UI, skipping...')



        def get_Write_Balance_Data_For_UI():
            print('\n┌-------------------------- REQUESTS | GET BALANCE DATA --------------------------┐')
            get_tab_balances = balance_functions.request_Futures_Balances_With_Client()
            futures_balance = get_tab_balances[0]
            margin_balance = get_tab_balances[1]
            spot_balance = get_tab_balances[2]#balance_functions.request_Spot_Balance_USDT()
            print("\nFetching balances for account",str(tab_account) + "...")
            print("-- Futures balance:",float("%.2f"%(futures_balance)))
            print("-- Futures margin:",float("%.2f"%(margin_balance)))
            print("-- Spot balance:",float("%.2f"%(spot_balance)))
            txt_ops.quick_write_txt_file_plus('txt/tab_data/balances/tab_futures_balance.txt',futures_balance)
            txt_ops.quick_write_txt_file_plus('txt/tab_data/balances/tab_futures_margin.txt',margin_balance)
            txt_ops.quick_write_txt_file_plus('txt/tab_data/balances/tab_spot_balance.txt',spot_balance)
            print('\n└------------------------ REQUESTS | END GET BALANCE DATA ------------------------┘\n\n')


        try:
            get_Write_Balance_Data_For_UI()
        except:
            print('\nError fetching balance data for UI, skipping...')





        def get_Write_Position_PNL_For_UI():
            print('\n┌-------------------------- REQUESTS | GET POSITION PNL --------------------------┐')
            get_pos_pnl = order_pos_functions.request_Position_PNL(positions_pair)
            print("\nPosition PNL:",get_pos_pnl)
            txt_ops.quick_write_txt_file_plus('txt/auto_data/pos_pnl/pos_pnl.txt',get_pos_pnl)
            print('\n└------------------------ REQUESTS | END GET POSITION PNL ------------------------┘\n\n')

        try:
            get_Write_Position_PNL_For_UI()
        except:
            print('\nError fetching position PNL data for UI, skipping...')



        def get_Position_Data_For_UI():
            get_position_data = order_pos_functions.request_Position_Information()

        def get_Open_Orders_Data_For_UI():
            get_open_orders_data = order_pos_functions.request_Open_Orders_Data()


        try:
            get_Position_Data_For_UI()
        except:
            print('\nError fetching positions data for UI, skipping...')

        try:
            get_Open_Orders_Data_For_UI()
        except:
            print('\nError fetching open orders data for UI, skipping...')

        try:
            #add/sub pos recommends
            signal_functions = Signals(1)
            a = signal_functions.simple_Mode_Safety('BTCUSDT','SHORT')
            b = signal_functions.simple_Mode_Safety('BTCUSDT','LONG')
            #
            c = signal_functions.simple_Mode_Safety('ETHUSDT','SHORT')
            d = signal_functions.simple_Mode_Safety('ETHUSDT','LONG')
            #
            e = signal_functions.simple_Mode_Safety('LTCUSDT','SHORT')
            f = signal_functions.simple_Mode_Safety('LTCUSDT','LONG')
            #
            g = signal_functions.simple_Mode_Safety('BNBUSDT','SHORT')
            h = signal_functions.simple_Mode_Safety('BNBUSDT','LONG')
            #
            i = signal_functions.simple_Mode_Safety('ADAUSDT','SHORT')
            j = signal_functions.simple_Mode_Safety('ADAUSDT','LONG')
        except:
            print('\nError fetching signals data for UI, skipping...')



    

    s.enter(4, 1, Looper, (sc,)) #refresh function wrapper

s.enter(4, 1, Looper, (s,)) #execute the refresh function



if __name__== ('__main__'):
    s.run()
    


