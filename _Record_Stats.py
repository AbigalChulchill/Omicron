import sys
sys.path.insert(1,'lib')
import os
from os.path import exists
import winsound
from _Withdraw_Functions import *
from _Time_Functions import *
from _Balance_Functions import *
from _txt_Ops import *
from _csv_Ops import *
from playsound import playsound
from _Maths_Functions import *
from _Array_Functions import *
import random



#check intbal exists, not zero


class Record_Stats():


    def __init__(self,account_no):

        self.account_no = account_no
        self.time_functions = Time_Functions()
        self.txt_ops = txt_Ops()
        self.csv_ops = csv_Ops()
        self.maths_functions = Maths_Functions(self.account_no)
        self.balance_functions = Balance_Functions(self.account_no)
        self.array_functions = Array_Functions()
                

    def request_Write_USDT_Balance(self):

        #request current balance data live
        curr_time = str(int(time.time()))
        get_balances = self.balance_functions.request_Futures_Balances_With_Client()
        balance = float("%.2f"%(get_balances[0]))

        #balance log file path
        file_path_str = 'txt/stats/init_balance_' + str(self.account_no) + '.txt'

        #get last balance in log, want to avoid duplicates
        last_balance = float(self.array_functions.symbol_Sep_To_Array(file_path_str,",","float")[-1])

        #if data is different, append new balance to log file
        if last_balance != balance:
            if os.path.exists(file_path_str):
                #if file exists, write with comma
                append_balance_value = txt_ops.quick_append_txt_file(file_path_str,","+str(balance))
            else:
                #if file does not exist, write first entry without comma
                write_balance_value = txt_ops.quick_write_txt_file_plus(file_path_str,str(balance))

            
                

    def analyze_Log_File(self,account_no):

        file_path = 'txt/stats/init_balance_' + str(account_no) + '.txt'
        win_events = 0
        loss_events = 0
        win_amounts = []
        loss_amounts = []
        diff = 0
        win_amounts_total = 0
        loss_amounts_total = 0
        
        values_array = self.txt_ops.read_commas_into_array(file_path,0)

        array_length = len(values_array)

        if array_length > 1:

            for i in range(1,array_length):

                current_value = float(values_array[i])
                prev_value = float(values_array[i-1])

                print(prev_value)
                print(current_value)
                
                if prev_value < current_value:
                    win_events += 1
                    win_amounts.append(current_value-prev_value)
                elif prev_value > current_value:
                    loss_events += 1
                    loss_amounts.append(current_value-prev_value)

            print(win_amounts, loss_amounts)

            diff = float(values_array[-1]) - float(values_array[0])

            win_amounts_total = sum(win_amounts)
            loss_amounts_total = sum(loss_amounts)
            
            return diff,win_amounts_total,loss_amounts_total,win_events,loss_events


            

   




    def analyze_Log_Folder(self):

        folder_path = 'txt/stats/'

        sum_array = []
        wins_array = []
        losses_array = []
        win_events_array = []
        loss_events_array = []
        final_pnl = 0
        final_wins = 0
        final_losses = 0
        final_win_events = 0
        final_loss_events = 0

        list_array = self.maths_functions.list_All_Files_In_Folder(folder_path)

        no_of_files = len(list_array)

        if no_of_files > 0:
            for i in range(no_of_files):
                print("\nAnalyzing account",i+1)
                curr_file = list_array[i]
                full_path = folder_path + curr_file
                get_data = self.analyze_Log_File(i+1)
                pnl = get_data[0]
                wins = get_data[1]
                losses = get_data[2]
                win_events = get_data[3]
                loss_events = get_data[4]
                sum_array.append(pnl)
                wins_array.append(wins)
                losses_array.append(losses)
                win_events_array.append(win_events)
                loss_events_array.append(loss_events)

        final_pnl = sum(sum_array)

        final_wins = sum(wins_array)

        final_losses = sum(losses_array)

        final_win_events = sum(win_events_array)

        final_loss_events = sum(loss_events_array)

        self.txt_ops.quick_write_txt_file_plus('txt/data/for_perf/final_pnl.txt',final_pnl)
        self.txt_ops.quick_write_txt_file_plus('txt/data/for_perf/final_wins.txt',final_wins)
        self.txt_ops.quick_write_txt_file_plus('txt/data/for_perf/final_losses.txt',final_losses)
        self.txt_ops.quick_write_txt_file_plus('txt/data/for_perf/final_win_events.txt',final_win_events)
        self.txt_ops.quick_write_txt_file_plus('txt/data/for_perf/final_loss_events.txt',final_loss_events)

        return final_pnl,final_wins,final_losses,final_win_events,final_loss_events
                

        

        





if __name__ == '__main__':

    a = Record_Stats(1)

    #'txt/stats/init_balance_' + str(account_to_use) + '.txt'

    c = a.analyze_Log_File(1)
    print(c)
    d = a.analyze_Log_Folder()
    print(d)

    




 
