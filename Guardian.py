print("\nLoading OMICRON | GUARDIAN...\n")
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
from _Maths_Functions import *
from _Withdraw_Functions import *
from _Fetch_Settings import *
from _Time_Functions import *
from _Account_Functions import *
from _Order_Pos_Functions import *
from _Record_Stats import *
from _Balance_Functions import *
from _Crash_Manager import *
from _txt_Ops import *
txt_ops = txt_Ops()
from _csv_Ops import *
csv_ops = csv_Ops()

#assign a Windows PID
pid_protect = os.getpid()
txt_ops.quick_write_txt_file('txt/pids/pid_protect.txt',pid_protect)
s = sched.scheduler(time.time, time.sleep)

#reset at first run
pad_unlock = txt_ops.quick_write_txt_file('txt/settings/guard/padlock.txt',0)
manual_unlock = txt_ops.quick_write_txt_file('txt/settings/manual_lock.txt',0)


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
            print("\nError: Unknown network connection timeout issue!")
            raise NetworkError
    return inner

def makeBeep(frequency,duration,play_times):
    for i in range(play_times):
        winsound.Beep(frequency, duration)

def login_Counter():
    maths_functions = Maths_Functions(1)
    login_count = maths_functions.count_Files('txt/login/')[0]
    return login_count

def get_Current_Price_Man(pair_symbol):
    price_functions = Price_Functions(1)
    get_price_data = price_functions.request_Price_Data(pair_symbol)
    current_price = get_price_data[2] # 0 avg | 1 mark | 2 hybrid
    return current_price
 


def leverage_Change(tab_account,symbol):
    path_str = 'txt/setup/' + str(tab_account) + '/setup_' + str(tab_account) +\
               '_' + str(symbol) + '.txt'
    #get current lev value
    settings = Settings(tab_account)
    get_current_lev = int(settings.load_Trade_Variables(symbol)[37])
    get_req_lev = int(settings.load_Trade_Variables(symbol)[38])
    if get_req_lev != get_current_lev:
        account_functions = Account_Functions(tab_account)
        #change global leverage
        change_global_leverage = account_functions.change_Global_Leverage(symbol,get_req_lev)
        print(change_global_leverage)
        #replace leverage value
        lev_str = "leverage=" + str(get_req_lev)
        txt_ops.replace_Specific_Line(path_str,38,lev_str)
        #alert user
        playsound('audio/leverage.wav')
        print("\nGUARDIAN | Leverage Manager | Mismatch, leverage changed.\n")
    else:
        print("\nGUARDIAN | Leverage Manager | No need to change leverage.\n")




def auto_Move_Spot_Fut_USDT():

    auto_move_allowed = int(txt_ops.quick_read_txt_file('txt/settings/liqs/auto_move.txt'))
    padlock_check = int(txt_ops.quick_read_txt_file('txt/settings/guard/padlock.txt'))
    skim_allowed = int(txt_ops.quick_read_txt_file('txt/settings/skim_mode.txt'))
    skim_amount = float(txt_ops.quick_read_txt_file('txt/settings/skim/skim_amount.txt'))
    
    if auto_move_allowed == 1:

        if padlock_check == 0:
        
            for i in range(login_Counter()):

                account_no = i+1
                balance_functions = Balance_Functions(account_no)
                usdt_balance = balance_functions.request_Spot_Balance_A_Crypto('USDT')
                
                if usdt_balance > 0:
                   
                    withdraw_functions = Withdraw_Functions(account_no)
                    
                    if skim_allowed == 1:

                        try:
                            withdraw_functions.transfer_Spot_Cross_Margin('USDT',skim_amount)
                            withdraw_functions.transfer_Spot_Futures('USDT',usdt_balance-skim_amount)
                            if account_no == 1:
                                playsound('audio/auto_move_1.wav')
                            else:
                                playsound('audio/auto_move_2.wav')
                        except:
                            pass

                    elif skim_allowed == 0:

                        try:
                            withdraw_functions.transfer_Spot_Futures('USDT',usdt_balance)
                            if account_no == 1:
                                playsound('audio/auto_move_1.wav')
                            else:
                                playsound('audio/auto_move_2.wav')
                        except:
                            pass

                    

                
        
def pad_Accounts_Man():

    network = 'BNB'
    status_code = 0

    padding_allowed = int(txt_ops.quick_read_txt_file('txt/settings/liqs/pad_protector.txt'))

    if padding_allowed == 1:

        transfer_threshold = float(txt_ops.quick_read_txt_file('txt/settings/guard/allow_multiple.txt'))
        risk_threshold = float(txt_ops.quick_read_txt_file('txt/settings/guard/risk_multiple.txt'))
        move_amount = float(txt_ops.quick_read_txt_file('txt/settings/guard/pad_move_amount.txt'))

        for i in range(login_Counter()):
            
            account_no = i + 1
            get_balances = Balance_Functions(account_no)
            balance_data = get_balances.request_Futures_Balances()
            balance_amount = balance_data[0]
            margin_amount = balance_data[1]
            risk_ratio = balance_amount / margin_amount

            print("\nRisk ratio is",risk_ratio)

            if account_no == 1 and risk_ratio > risk_threshold:

                get_balances = Balance_Functions(2)
                balance_data = get_balances.request_Futures_Balances()
                balance_amount = balance_data[0]
                margin_amount = balance_data[1]
                other_risk_ratio = balance_amount / margin_amount

                if other_risk_ratio < transfer_threshold:

                    pad_lock = txt_ops.quick_write_txt_file('txt/settings/guard/padlock.txt',1)

                    playsound('audio/padding1.wav')
             
                    withdraw_functions = Withdraw_Functions(2)
                    status_code = withdraw_functions.transfer_Futures_Spot('USDT',move_amount)

                    if status_code == 200:

                        #get to address data
                        withdraw_functions = Withdraw_Functions(1)
                        address_data = withdraw_functions.request_Deposit_Address('USDT',network)
                        address = address_data[0]
                        address_tag = address_data[1]

                        #withdraw from
                        withdraw_functions = Withdraw_Functions(2)
                        status_code = withdraw_functions.withdraw('USDT',move_amount,address,address_tag,network)

                        time.sleep(1)

                        if status_code == 200:
                            print("\nPadding Protection | Withdrawal of ",move_amount,"USDT from account 2 to account 1 completed.")
                            playsound("audio/transfer_success.wav")
                        else:
                            print("\nPadding Protection | Withdrawal of ",move_amount,"USDT from account 2 to account 1 failed!")
                            playsound("audio/transfer_fail.wav")
                        pad_lock = txt_ops.quick_write_txt_file('txt/settings/guard/padlock.txt',0)

            if account_no == 2 and risk_ratio > risk_threshold:

                get_balances = Balance_Functions(1)
                balance_data = get_balances.request_Futures_Balances()
                balance_amount = balance_data[0]
                margin_amount = balance_data[1]
                other_risk_ratio = balance_amount / margin_amount

                if other_risk_ratio < transfer_threshold:

                    pad_lock = txt_ops.quick_write_txt_file('txt/settings/guard/padlock.txt',1)
                    
                    playsound('audio/padding2.wav')

                    withdraw_functions = Withdraw_Functions(1)
                    status_code = withdraw_functions.transfer_Futures_Spot('USDT',move_amount)

                    if status_code == 200:

                        print("\nPadding Protection | Transfer of ",move_amount," USDT complete.")

                        #get to address data
                        withdraw_functions = Withdraw_Functions(2)
                        address_data = withdraw_functions.request_Deposit_Address('USDT',network)
                        address = address_data[0]
                        address_tag = address_data[1]

                        #withdraw from
                        withdraw_functions = Withdraw_Functions(1)
                        status_code = withdraw_functions.withdraw('USDT',move_amount,address,address_tag,network)

                        time.sleep(1)

                        if status_code == 200:

                            print("\nPadding Protection | Withdrawal of ",move_amount,"USDT from account 1 to account 2 completed.")
                            playsound("audio/transfer_success.wav")

                        else:
                            print("\nPadding Protection | Withdrawal of ",move_amount,"USDT from account 1 to account 2 failed!")

                            playsound("audio/transfer_fail.wav")
                                
                            
                        pad_lock = txt_ops.quick_write_txt_file('txt/settings/guard/padlock.txt',0)



                    
                   

def remove_Orphan_Orders_Man():
    print("\nGUARDIAN | Searching for orphan TP/SL orders for removal...")
    sweep_list = login_Counter()
    for i in range(sweep_list):
        order_pos_dynamic = Order_Pos_Functions(i+1)
        remove_orphans = order_pos_dynamic.remove_Orphan_Orders()
        if remove_orphans > 0:
            playsound('audio/remaining.wav')


loop_cycle = 0
session_start_time = Time_Functions().get_Timestamp(13)

@retryer
def Looper(sc):

    global loop_cycle
    global session_start_time

    loop_cycle += 1

    #get time and crash detection
    current_unix_time = Time_Functions().get_Timestamp(13)
    #txt_ops.quick_write_txt_file('txt/clock_check/protector_time.txt',current_unix_time)

    converted_time = Time_Functions().convert_Time(current_unix_time)
    elapsed_time_mins = round((current_unix_time - session_start_time) / 60)
    print("----------------------------------------------------------------")
    print("\nGUARDIAN | Scan Cycle:",loop_cycle,"| Elapsed Time:",elapsed_time_mins,"mins")
    print("\n----------------------------------------------------------------")

    if loop_cycle == 1 or loop_cycle % 4 == 0:
        try:
            remove_Orphan_Orders_Man()
        except:
            print("\nError: Unknown remove orphans issue!")
    if loop_cycle == 1 or loop_cycle % 2 == 0:
        try:
            auto_Move_Spot_Fut_USDT()
        except:
            print("\nError: Unknown auto move USDT issue!")

        try:
            pad_Accounts_Man()
        except:
            print("\nError: Unknown pad account issue!")

    #SCAN FOR LEVERAGE CHANGE REQUESTS
    get_last_account_tab = int(txt_ops.quick_read_txt_file("txt/last_tab_account.txt"))
    if get_last_account_tab > 0:
        try:
            make_str = 'txt/setup/' + str(get_last_account_tab) + '/setup_' + str(get_last_account_tab) + '.txt' 
            get_settings = Settings(get_last_account_tab)
            account_settings = get_settings.load_Account_Variables()
            pair_last = account_settings[4]
            leverage_Change(get_last_account_tab,pair_last)
        except:
            print("\nError: Leverage change operation cannot be completed, skipping...")
        
    #-----------------------------------------------------------------------

    time.sleep(1)
    s.enter(5, 1, Looper, (sc,)) #refresh function wrapper
s.enter(5, 1, Looper, (s,)) #execute the refresh function

if __name__==('__main__'):
    s.run()
