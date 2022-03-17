from _txt_Ops import *
import os

class Logins:

    def __init__(self):
        self.txt_ops = txt_Ops()

    def return_Keys(self,account_no):
        parts = ''
        api_key = ''
        sec_key = ''
        dict_values_1 = ''
        dict_values_2 = ''
        travel_mode = int(self.txt_ops.quick_read_txt_file('txt/settings/travel_mode.txt'))
        if account_no == 0:
            account_no = 1
        keys_dict={}
        acc_str = 'txt/login/login_' + str(account_no) + '.txt'
        with open (acc_str, "r") as hfile:
            sp = hfile.read()
        lines = sp.split("\n")
        try:
            for line in lines:
                if line != '':
                    parts = line.split("=")
                keys_dict[ parts[0] ] = parts[1]
            if travel_mode == 0:
                dict_values_1 = list( keys_dict.values() )[0]
                dict_values_2 = list( keys_dict.values() )[1]
            elif travel_mode == 1:
                dict_values_1 = list( keys_dict.values() )[2]
                dict_values_2 = list( keys_dict.values() )[3]
        except:
            print("\nAPI Login error...")
        api_key = dict_values_1
        sec_key = dict_values_2
        return api_key,sec_key


def check_Module():
    logins = Logins()
    return_keys = logins.return_Keys(1)
    print("Running test module for Logins class:",return_keys)
    

if __name__=='__main__':
    check_Module()
    






