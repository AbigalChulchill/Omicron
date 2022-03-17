print("\nLoading OMICRON | ENTRY MANAGER...\n")

import sys
sys.path.insert(1,'lib')

import requests
import time
import sched
from playsound import playsound
import os
from os.path import exists
import winsound
import subprocess as s
from datetime import datetime
from _Crash_Manager import *

#from _Email_Signals import *
from _Maths_Functions import *

from _Fetch_Settings import *
#from _Signals import *
from _Time_Functions import *
from _Account_Functions import *
from _Order_Pos_Functions import *
from _Record_Stats import *
from _Balance_Functions import *
from _txt_Ops import *
txt_ops = txt_Ops()
from _csv_Ops import *
csv_ops = csv_Ops()

#assign a Windows PID
pid_backend = os.getpid()
txt_ops.quick_write_txt_file('txt/pids/pid_backend.txt',pid_backend)
s = sched.scheduler(time.time, time.sleep)






#Keep running even when Internet connection temporarily breaks
class NetworkError(RuntimeError):
    pass
def retryer(func):
    retry_on_exceptions=(
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError
        )
    def inner(*args,**kwargs):
        for i in range(200):
            try:
                resgold=func(*args,**kwargs)
            except retry_on_exceptions:
                time.sleep(30)
                continue
            else:
                return resgold
        else:
            print("\nError: Unknown Network connection timeout issue.")
            raise NetworkError
    return inner


def make_Beep(frequency,duration,play_times):
    for i in range(play_times):
        winsound.Beep(frequency, duration)


def login_Counter():
    maths_functions = Maths_Functions(1)
    login_count = maths_functions.count_Files('txt/login/')[0]
    return login_count

    
#reset all busy status
#login_counter = login_Counter()

##for i in range(login_counter):
##    busy_str = 'txt/busy/busy_' + str(i+1) + '.txt'
##    print('acc busy reset:',i+1)
##    txt_ops.quick_write_txt_file(busy_str,0)
##
##    busy_str = 'txt/busy/busy_' + str(i+1) + '_ADAUSDT.txt'
##    print('acc busy reset:',i+1)
##    txt_ops.quick_write_txt_file(busy_str,0)
##
##
##    busy_str = 'txt/busy/busy_' + str(i+1) + '_BTCUSDT.txt'
##    print('acc busy reset:',i+1)
##    txt_ops.quick_write_txt_file(busy_str,0)
##
##
##    busy_str = 'txt/busy/busy_' + str(i+1) + '_ETHUSDT.txt'
##    print('acc busy reset:',i+1)
##    txt_ops.quick_write_txt_file(busy_str,0)
##


reset_busy = Order_Pos_Functions(1).reset_All_Busy_Vars()




def determine_Auto_Account():

    free_available = [0]
    auto_account = 0
    settings_dict = {}
    active_flag = 0


    for i in range( login_Counter() ):


        #get active flag
        try:
            account_settings_path = 'txt/setup/' + str(i+1) + '/setup_' + str(i+1) + '.txt'
            settings_dict = txt_ops.create_dict_from_txt(account_settings_path,'=')

            #print(settings_dict)
           
            active_flag = int(settings_dict['active'])
            #print(active_flag)
        except:
            pass

        if active_flag == 1:

            
            order_pos_dynamic = Order_Pos_Functions(i+1)
            get_next_symbol_data = order_pos_dynamic.determine_Position_Next() #next_symbol,can_afford,file_path
            next_symbol = get_next_symbol_data[0]

            if next_symbol != 'NONE':
                free_available.append(i+1)
                

        if len(free_available) > 0:
            auto_account = free_available[-1]
            write_auto = txt_ops.quick_write_txt_file("txt/full_auto_account.txt",auto_account)


    return auto_account


def reset_Manual_Triggers(account_no):

    folder_string = 'txt/setup/' + str(account_no) + '/'
    maths_functions = Maths_Functions(1)
    all_symbols_array = maths_functions.filter_All_Symbols_In_Folder(folder_string)
    length = len(all_symbols_array)

    if length > 0:
        for i in range(length):
           
            make_str = folder_string + 'setup_' + str(account_no) + '_' + all_symbols_array[i] + '.txt'
            txt_ops.replace_Specific_Line(make_str,12,'manual_trigger_long=0')
            txt_ops.replace_Specific_Line(make_str,13,'manual_trigger_short=0')
            


def get_Current_Price_Man(pair_symbol):
    price_functions = Price_Functions(1)
    get_price_data = price_functions.request_Price_Data(pair_symbol)
    # 0 avg | 1 mark | 2 hybrid
    current_price = get_price_data[0]
    return current_price




def entry_Assistant_Audio(entry_side,trigger_source):
    if trigger_source == 'manual_long':
        allow_voice = int(txt_ops.quick_read_txt_file('txt/jenny_toggle.txt'))
        if allow_voice == 1:
            playsound('audio/manual_long.wav')
    elif trigger_source == 'manual_short':
        allow_voice = int(txt_ops.quick_read_txt_file('txt/jenny_toggle.txt'))
        if allow_voice == 1:
            playsound('audio/manual_short.wav')
    elif trigger_source != 'manual_short' and trigger_source != 'manual_long':
        if entry_side == 'LONG':
            allow_voice = int(txt_ops.quick_read_txt_file('txt/jenny_toggle.txt'))
            if allow_voice == 1:
                playsound('audio/auto_long.wav')
        elif entry_side == 'SHORT':
            allow_voice = int(txt_ops.quick_read_txt_file('txt/jenny_toggle.txt'))
            if allow_voice == 1:
                playsound('audio/auto_short.wav')




            


def enter_Position(tab_account,pair_symbol,entry_side,trigger_source):

    print("\nENTRY MANAGER | Entering a",entry_side,"position (" + str(pair_symbol) + ") for account",tab_account)
    
    #write to busy files, general and pair_symbol specific
    #prevents orphan removal from clashing with entry orders
    busy_str_pair = 'txt/setup/' + str(tab_account) + '/setup_' + str(tab_account) + '_' + str(pair_symbol) + '.txt'
    txt_ops.replace_Specific_Line(busy_str_pair,2,'busy=1')      

    busy_str_account = 'txt/setup/' + str(tab_account) + '/setup_' + str(tab_account) + '.txt'
    txt_ops.replace_Specific_Line(busy_str_account,2,'busy=1')

    #audio
    entry_Assistant_Audio(entry_side,trigger_source)

    #init vars
    array_entry_amounts = []
    purchase_stage = 0
    waiting_order_id = 0
    waiting_order_time = 0
    order_pos_dynamic = Order_Pos_Functions(tab_account)

    if entry_side == 'LONG':
        side_type = 'BUY'
    elif entry_side == 'SHORT':
        side_type = 'SELL'

    #settings for account
    get_settings = Settings(tab_account)
    settings = get_settings.load_Trade_Variables(pair_symbol)
    #
    quantity_to_trade = settings[2]
    split_order_segments = settings[3]
    order_split_time_range = settings[4]
    taper_in_wait = order_split_time_range / split_order_segments
    trade_amount = quantity_to_trade / split_order_segments

    #check if orders with symbol already exist - 1
    check_order_clash = order_pos_dynamic.check_Order_Clash(pair_symbol)
   
    if check_order_clash == 0:

        print("\nENTRY MANAGER | Starting entry, purchase stage:",purchase_stage)
        reset_Manual_Triggers(tab_account)
        
        record_stats = Record_Stats(tab_account)
        record_stats.request_Write_USDT_Balance()

        while True:

            #Allows you to change limit/market, bid settings real-time during position creation process
            is_limit_entry = settings[8]
            initial_bid = settings[9]
            bids = settings[10]
            
            #check if orders with symbol already exist - 2
            check_order_clash = order_pos_dynamic.check_Order_Clash(pair_symbol)
            
            #proceed to next order if following conditions are satisfied
            if check_order_clash == 0 and purchase_stage < split_order_segments:
            
                make_Beep(5900,100,2)

                #reduce waiting time to 1 sec at final stage, or waits too long afterwards
                if split_order_segments - purchase_stage < 2:
                    taper_in_wait = 1

                #CREATE ORDER LIMIT
                if is_limit_entry == 1:

                    make_Beep(5500,100,1)

                    #Get current price - hybrid
                    current_price = get_Current_Price_Man(pair_symbol)

                    #initial bid
                    if purchase_stage == 0:
                        if entry_side == 'LONG':
                            bid_enter = current_price - initial_bid
                        if entry_side == 'SHORT':
                            bid_enter = current_price + initial_bid
                        print("\nENTRY MANAGER | Current price for",pair_symbol,"is:",current_price,"\nEntry bid:",initial_bid,'@',bid_enter)

                    #subsequent bids
                    else:
                        if entry_side == 'LONG':
                            bid_enter = current_price - bids
                        if entry_side == 'SHORT':
                            bid_enter = current_price + bids
                        print("\nENTRY MANAGER | Current price for",pair_symbol,"is:",current_price,"\nBid:",bids,'@',bid_enter)

                    if pair_symbol == 'BTCUSDT':
                        bid_enter = float("%.2f"%(bid_enter))
                    if pair_symbol == 'ETHUSDT':
                        bid_enter = float("%.2f"%(bid_enter))
                    if pair_symbol == 'ADAUSDT':
                        bid_enter = float("%.3f"%(bid_enter))
                    if pair_symbol == 'LTCUSDT':
                        bid_enter = float("%.2f"%(bid_enter))
                    if pair_symbol == 'BNBUSDT':
                        bid_enter = float("%.2f"%(bid_enter))

                    #CREATE THE LIMIT ORDER
                    create_futures = order_pos_dynamic.create_Futures_Order(pair_symbol,side_type,'LIMIT','GTC',bid_enter,0,trade_amount)

                    

                    waiting_order_id = create_futures[0]

                    #time_functions = Time_Functions()
                    #waiting_order_time = time_functions.get_Timestamp(13)

                    print("\nENTRY MANAGER | NEW Limit Order created with ID:",waiting_order_id)

                    make_Beep(5500,100,1)
                    time.sleep(taper_in_wait)

                #CREATE ORDER MARKET
                if is_limit_entry == 0:
                    make_Beep(5500,100,1)
                    create_market = order_pos_dynamic.create_Futures_Order(pair_symbol,side_type,'MARKET','null',0,0, trade_amount  )
                    waiting_order_id = create_market[0]
                    print("\nENTRY MANAGER | NEW Market Order created with ID:",waiting_order_id)
                    make_Beep(5500,100,1)
                    time.sleep(taper_in_wait)





                while True:

                    
                    print("\n-t--waiting_order_id:",waiting_order_id)

                    #check if the order has been filled
                    get_order_data_by_id = order_pos_dynamic.check_Order_Filled_Status(pair_symbol,waiting_order_id)
                    print("\n-t--get_order_data_by_id:",get_order_data_by_id)

                    post_check_filled = get_order_data_by_id[0]
                    print("\n-t--post_check_filled:",post_check_filled)

                    time.sleep(1)

          

                    print("\nENTRY MANAGER | Order ID:",waiting_order_id,"| Status:",post_check_filled,"\n")

                    #get number of open orders
                    #open_orders_num = len(order_pos_dynamic.request_Open_Orders_Data())
                    check_order_clash = order_pos_dynamic.check_Order_Clash(pair_symbol)
                    print("\nENTRY MANAGER | check_order_clash:",check_order_clash)
                   

                    #ID 1 is error
                    if waiting_order_id == 1:

                        break
                        #double break
                        #purchase stages completed, head to TP/SL creation

                    if check_order_clash == 0 and post_check_filled == 'FILLED':

                        print('BACKEND | Order',waiting_order_id,'has filled!')

                        #get amounts
                        get_avg_entry = get_order_data_by_id[1]

                        array_entry_amounts.append(get_avg_entry)
                        print('\nENTRY MANAGER | Fragment entry price list:',array_entry_amounts)
                        purchase_stage = purchase_stage + 1
                        print('\nENTRY MANAGER | Purchase stage completed:',purchase_stage,"/",split_order_segments)
                        break



                    if check_order_clash == 0 and (post_check_filled == 'CANCELED' or post_check_filled == 'CANCELLED'):

                       

                       
                        break

                #purchase stages completed, head to TP/SL creation
                if (purchase_stage == split_order_segments) or waiting_order_id == 1:

                    #reset purchase stage
                    purchase_stage = 0

                    #create_TP_and_SL
                    order_pos_functions = Order_Pos_Functions(tab_account)
                    c = order_pos_functions.create_TP_and_SL(pair_symbol)

                    break









loop_cycle = 0
session_start_time = Time_Functions().get_Timestamp(13)

@retryer
def Looper(sc):

    global loop_cycle
    global session_start_time

    loop_cycle += 1
   
    final_status = 'UNSAFE'
    
    


##    try:
##        c = Crash_Manager()
##        run_check = c.check_Modules_Alive()
##    except:
##        print("\nError: Can't check module health.")

    #get time and crash detection
   
    print("\n*****************************************************")
    print("\nENTRY MANAGER | Scan Cycle:",loop_cycle)
    print("\n*****************************************************")

    auto_account = determine_Auto_Account()
    #record current auto account to a txt file
    txt_ops.quick_write_txt_file('txt/full_auto_account.txt',auto_account)


#######################################################################################################################################
#######################################################################################################################################

    def attempt_Entry(account_to_use,auto_flag,side):

        if account_to_use > 0:

            #init vars
            account_permitted = 0
            can_afford = 0
            final_status = ''
            check_open_exist = 1
            check_long_clash = 0
            check_short_clash = 0
            longs_allowed = 0
            shorts_allowed = 0
            maintain_balance = 1
            next_symbol = 'NONE'
            check_pos_exist = 1
            #determine next symbol, and if enough funds exist to enter a trade
            order_pos_dynamic = Order_Pos_Functions(account_to_use)




            #MANUAL OVERRIDE ENTRY
            if auto_flag == 0:


                #try:
                    
                get_account_settings = Settings(account_to_use)
                account_settings = get_account_settings.load_Account_Variables()
                user_symbol = account_settings[4]
                check_pos_exist = order_pos_dynamic.check_Position_With_Symbol_Active(user_symbol)
                if check_pos_exist == 0:
                    if side == 'LONG':
                        manual_unlock = txt_ops.quick_write_txt_file('txt/settings/manual_lock.txt',0)
                        enter_Position(account_to_use,user_symbol,'LONG','manual_long')
                    elif side == 'SHORT':
                        manual_unlock = txt_ops.quick_write_txt_file('txt/settings/manual_lock.txt',0)
                        enter_Position(account_to_use,user_symbol,'SHORT','manual_short')
                else:
                    playsound('audio/unable_open_clash.wav')
                #except:
                    #print("\nError reading settings [470]...")






            #CHECK AUTO
            if auto_flag == 1:

                try:
                    get_account_settings = Settings(account_to_use)
                    account_settings = get_account_settings.load_Account_Variables()
                    account_permitted = int(account_settings[0])
                    print("\nAuto settings read active:",account_permitted)
                    maintain_balance = int(account_settings[13])
                    print("\nAuto settings read maintain balance:",maintain_balance)
                except:
                    print("\nError reading settings [490]...")
                    

                

      

                if account_permitted == 1:

                    try:

                        get_next_symbol_data = order_pos_dynamic.determine_Position_Next() #next_symbol,can_afford,file_path
                        next_symbol = get_next_symbol_data[0]
                        can_afford = get_next_symbol_data[1]
                        settings_path = get_next_symbol_data[2]
                   
                        #also check there are no open orders for symbol
                        check_open_exist = order_pos_dynamic.check_Order_Clash(next_symbol)

                        #also check there are no open positions already for symbol
                        check_pos_exist = order_pos_dynamic.check_Position_With_Symbol_Active(next_symbol)
                    
                    except:
                        pass

                    if check_open_exist == 1:
                        playsound('audio/unable_open_clash.wav')



                    if check_pos_exist == 1:
                        playsound('audio/unable_pos_clash.wav')

                        
                    if next_symbol != 'NONE' and check_pos_exist == 0 and check_open_exist == 0 and can_afford == 1:




                        #get settings for account/symbol
                        try:
                            settings_functions = Settings(account_to_use)
                            settings_array = settings_functions.load_Trade_Variables(next_symbol)
                            longs_allowed = int(settings_array[13])
                            shorts_allowed = int(settings_array[14])
                            print("\nENTRY MANAGER | Successfully loaded Long/Short permissions settings:",longs_allowed,shorts_allowed)
                        except:
                            print("\nError reading settings [520]...")

                        if longs_allowed == 1:
                            
                            final_status = Signals(account_to_use).final_Status(next_symbol,'LONG')

                            if final_status == 'SAFE':
                                print("\nENTRY MANAGER | Long opportunity detected, entering position...")


                                check_long_clash = order_pos_dynamic.check_Sides_Balance('LONG')

                                if (maintain_balance == 1 and check_long_clash == 0) or maintain_balance == 0:
                                    manual_unlock = txt_ops.quick_write_txt_file('txt/settings/manual_lock.txt',0)
                                    enter_Position(account_to_use,next_symbol,'LONG','auto_long')
                                else:
                                    
                                    playsound('audio/unable_too_many_longs.wav')

                                    #pass




                            else:
                                print("\nENTRY MANAGER | Waiting for long signals to align...")

                        if shorts_allowed == 1:

                            try:
                                final_status = Signals(account_to_use).final_Status(next_symbol,'SHORT')
                            except:
                                print("\nENTRY MANAGER | Problem fetching short signals report, waiting...")

                            #final_status = 'SAFE'

                            if final_status == 'SAFE':
                                print("\nENTRY MANAGER | Short opportunity detected, entering position...")


                                check_short_clash = order_pos_dynamic.check_Sides_Balance('SHORT')



                                if (maintain_balance == 1 and check_short_clash == 0) or maintain_balance == 0:
                                    manual_unlock = txt_ops.quick_write_txt_file('txt/settings/manual_lock.txt',0)
                                    enter_Position(account_to_use,next_symbol,'SHORT','auto_short')
                                else:
                                    playsound('audio/unable_too_many_shorts.wav')


                            else:
                                print("\nENTRY MANAGER | Waiting for short signals to align...")




                    if next_symbol != 'NONE' and can_afford == 0 and check_open_exist == 0:
                        print("\nENTRY MANAGER | Symbol(s) available but account margin is too low to trade, waiting...")
                        
                    if next_symbol == 'NONE':
                        print("\nENTRY MANAGER | No symbols are available, waiting...")


                  


    #basic account free check (not in pos), proceeds to signal check via attempt_Entry
    if auto_account != 0:
        attempt_Entry(auto_account,1,'')



#######################################################################################################################################
    
    #SCAN FOR MANUAL ENTRY REQUESTS
    get_last_account_tab_str = txt_ops.quick_read_txt_file('txt/last_tab_account.txt')
    get_last_account_tab = int(get_last_account_tab_str)

    print("\n**************************************************************")
    print("\nENTRY MANAGER | Checking for manual instructions for account",get_last_account_tab)
    
    if get_last_account_tab > 0:

        manual_trigger_long = 0
        manual_trigger_short = 0
  
        try:
            #get last pair symbol from settings combo dropdown
            get_account_settings = Settings(get_last_account_tab)
            account_settings = get_account_settings.load_Account_Variables()
            pair_symbol = account_settings[4]
            print("\nPair symbol for settings is:",pair_symbol)
            
            #now load the trade settings for this pair symbol
            get_pair_settings = get_account_settings.load_Trade_Variables(pair_symbol)
            manual_trigger_long = int(get_pair_settings[11])
            manual_trigger_short = int(get_pair_settings[12])
            print("\nSuccessful settings read for manual triggers...")
            print("\nManual Trigger Long:",manual_trigger_long)
            print("Manual Trigger Short:",manual_trigger_short)

        except:
            manual_trigger_long = 0
            manual_trigger_short = 0
        
        if manual_trigger_long == 1:
            print("\nManual entry requested for Account",str(get_last_account_tab) + ", entering",pair_symbol,"LONG")
            attempt_Entry(get_last_account_tab,0,'LONG')
        if manual_trigger_short == 1:
            print("\nManual entry requested for Account",str(get_last_account_tab) + ", entering",pair_symbol,"SHORT")
            attempt_Entry(get_last_account_tab,0,'SHORT')

    print("\nENTRY MANAGER | END Checking for manual instructions for account",get_last_account_tab)
    print("\n**************************************************************")


    #Reset all manual entry triggers
    if loop_cycle == 1 or loop_cycle % 8 == 0:

        manual_lock = int(txt_ops.quick_read_txt_file('txt/settings/manual_lock.txt'))

        if manual_lock == 0:
        
            if get_last_account_tab != 0:
                reset_Manual_Triggers(get_last_account_tab)
            if auto_account != 0:
                reset_Manual_Triggers(auto_account)




        #call spot balance again, process too slow
        balance_functions = Balance_Functions(get_last_account_tab)
        spot_balance = balance_functions.request_Spot_Balance_USDT()


        
    #-----------------------------------------------------------------------

    s.enter(4, 1, Looper, (sc,)) #refresh function wrapper
s.enter(4, 1, Looper, (s,)) #execute the refresh function

if __name__==('__main__'):
    s.run()
