import sys
sys.path.insert(1, 'lib')

import os
import re
import requests
from collections import Counter
import time
import hmac
import hashlib
from urllib.parse import urljoin, urlencode

#my libs
from _Logins import *
from _txt_Ops import *
from _Binance_Exceptions import *


class Maths_Functions():

    def __init__(self,account_no):
        super().__init__()
        self.account_no = account_no
        self.txt_ops = txt_Ops()


    def find_Most_Common_Values(self,input_array):
        common_1 = 0
        common_2 = 0
        common_1_occur = 0
        common_2_occur = 0
        c = Counter(input_array)
        try:
            common_1 = c.most_common(1)[0][0]
            common_1_occur = c.most_common(1)[0][1]
        except:
            print("\nWarning: No common value applicable, skipping...")
        try:
            common_2 = c.most_common(2)[1][0]
            common_2_occur = c.most_common(2)[1][1]
        except:
            print("\nWarning: No second most common value applicable, skipping...")
        return common_1,common_2,common_1_occur,common_2_occur

    def find_Most_Common_Values_Rem_Zero(self,input_array):
        common_1 = 0
        common_1_occur = 0
        c = Counter(input_array)
        common_1 = c.most_common(1)[0][0]
        common_1_occur = c.most_common(1)[0][1]
        if common_1 == 0:
            common_1 = c.most_common(2)[1][0]
            common_1_occur = c.most_common(2)[1][1]
        return common_1,common_1_occur

    def count_Files(self,file_path):
        file_no_array=[]
        path, dirs, files = next(os.walk(file_path))
        file_count = len(files)
        for i in range(file_count):
            a=re.findall(r'\d+', files[i])
            b=", ".join(map(str, a))
            str(b).replace('[','').replace(']','')
            file_no_array.append(b)
        return file_count,file_no_array


    def count_Folders(self,file_path):
        path, dirs, files = next(os.walk(file_path))
        folder_count = len(dirs)
        return folder_count

    def list_All_Files_In_Folder(self,folder_path):

        from os import listdir
        from os.path import isfile, join
        file_list = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
        return file_list

    def filter_All_Symbols_In_Folder(self,folder_path):

        list_array = self.list_All_Files_In_Folder(folder_path)
        length = len(list_array)
        filtered_array = []

        for i in range(length):
            make_str = list_array[i]
            if make_str.find('USD') > 0:
                r_string = str(re.findall('([A-Z]+)', make_str))
                valids = re.sub(r"[^A-Za-z]+", '', r_string)
                
                filtered_array.append(valids)

        return filtered_array
                
            



    

    def calculate_Fibs(self,input_array):
        if input_array != []:
            fibs_array = []
            price_min = min(input_array)
            price_max = max(input_array)
            range_max = price_max - price_min
            line_236 = float("%.4f"%(price_min + ((23.6 * range_max) / 100)))
            line_382 = float("%.4f"%(price_min + ((38.2 * range_max) / 100)))
            line_500 = float("%.4f"%(price_min + ((50 * range_max) / 100)))
            line_618 = float("%.4f"%(price_min + ((61.8 * range_max) / 100)))
            line_786 = float("%.4f"%(price_min + ((78.6 * range_max) / 100)))
            fibs_array = [line_236,line_382,line_500,line_618,line_786]
            #print('\nfibs_array',fibs_array)
            self.txt_ops.quick_write_txt_file('txt/mode/fib_236.txt',fibs_array[0])
            self.txt_ops.quick_write_txt_file('txt/mode/fib_382.txt',fibs_array[1])
            self.txt_ops.quick_write_txt_file('txt/mode/fib_500.txt',fibs_array[2])
            self.txt_ops.quick_write_txt_file('txt/mode/fib_618.txt',fibs_array[3])
            self.txt_ops.quick_write_txt_file('txt/mode/fib_786.txt',fibs_array[4])
            return fibs_array


    def convert_Array_To_Quantized(self,input_array,multiplier,quantize_value):
        quant_array = []
        for j in range(len(input_array)):
            quant_array.append(    (int(round(float(input_array[j]*multiplier)/quantize_value))*quantize_value)/multiplier        )
        return quant_array



    def convert_Array_To_Quantized_Special(self,input_array):
        arr = []
        quant_array = []
        if input_array != None and input_array != [] and len(input_array) > 0:
            get_max_price = sum(input_array) / len(input_array)
            #BTC Region
            if get_max_price >= 10000: #$100 INCREMENTS
                arr = [1,100]
            #ETH region
            if get_max_price >= 1000 and get_max_price < 10000: 
                arr = [1,10]
            #region?
            if get_max_price >= 500 and get_max_price < 1000: 
                arr = [1,5]
            #BNB/LTC regions
            if get_max_price >= 100 and get_max_price < 500: 
                arr = [1,1]
            #BNB, LINK, UNI
            if get_max_price >= 20 and get_max_price < 100:
                arr = [1,1]
            #LINK region
            if get_max_price >= 5 and get_max_price < 20:
                arr = [4,1]
            #XRP, EOS, 
            if get_max_price >= 0.5 and get_max_price < 5:
                arr = [10000,100]
            #ADA, XRP
            if get_max_price < 0.5:
                arr = [10000,1]
            for j in range(len(input_array)):
                quant_array.append((int(round(float(input_array[j]*arr[0])/arr[1]))*arr[1])/arr[0])
        return quant_array

    def calc_Price_Mode_Values(self,pair_symbol,input_array):
        mode_1 = 0
        mode_2 = 0
        quant_array = self.convert_Array_To_Quantized_Special(input_array)
        mode_1 = self.find_Most_Common_Values(quant_array)[0]
        mode_2 = self.find_Most_Common_Values(quant_array)[1]
        #print("\nMode Function | Mode values calculated:",mode_1,mode_2)
        return mode_1,mode_2

    def calc_Gold_Silver(self,pair_symbol,input_array):
        gold_array = []
        quantized_array = self.convert_Array_To_Quantized_Special(input_array)
        get_most_common = self.find_Most_Common_Values(quantized_array)
        mode_1 = get_most_common[0]
        mode_2 = get_most_common[1]
        if mode_1 != 0:
            gold_array.append(mode_1)
        if mode_2 != 0:
            gold_array.append(mode_2)
        #write to text file
        self.txt_ops.quick_write_txt_file_plus("txt/mode/mode_1_" + pair_symbol + ".txt",str(mode_1))
        self.txt_ops.quick_write_txt_file_plus("txt/mode/mode_2_" + pair_symbol + ".txt",str(mode_2))
        fibs_array = self.calculate_Fibs(input_array)
        quant_fibs_array = self.convert_Array_To_Quantized_Special(fibs_array)
        for j in range(len(quant_fibs_array)):
            gold_array.append(quant_fibs_array[j])
        gold = self.find_Most_Common_Values(gold_array)[0]
        silver = self.find_Most_Common_Values(gold_array)[1]
        #print("\nMaths Functions | Gold/Silver values calculated:",self.find_Most_Common_Values(gold_array))
        #write to text file
        self.txt_ops.quick_write_txt_file_plus("txt/mode/gold_" + pair_symbol + ".txt",str(gold))
        self.txt_ops.quick_write_txt_file_plus("txt/mode/silver_" + pair_symbol + ".txt",str(silver))
        return gold,silver




def check_Module():

    maths_functions = Maths_Functions(1)

    list_all = maths_functions.filter_All_Symbols_In_Folder('txt/setup/1/')
    print(list_all)




if __name__=='__main__':


    check_Module()
