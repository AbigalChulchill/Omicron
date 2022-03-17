import os, shutil
from _txt_Ops import *
from _csv_Ops import *



class Admin:

    def __init__(self):

        self.txt_ops = txt_Ops()
        self.csv_ops = csv_Ops()


    def clear_Configs(self):


        print("\nClearing All Cache...")

        self.txt_ops.quick_write_txt_file("txt/account_created.txt",0)
        self.txt_ops.quick_write_txt_file("txt/active_account.txt",1)
        self.txt_ops.quick_write_txt_file("txt/tab_account.txt",0)
        self.txt_ops.quick_write_txt_file("txt/last_tab_account.txt",0)
        self.txt_ops.quick_write_txt_file("txt/batch_launch.txt",1)
        self.txt_ops.quick_write_txt_file("txt/console.txt","Welcome to Astaroth")
        self.txt_ops.quick_write_txt_file("txt/full_auto.txt",0)
        self.txt_ops.quick_write_txt_file("txt/full_auto_account.txt",0)
        self.txt_ops.quick_write_txt_file("txt/login/login_1.txt","")
        self.txt_ops.quick_write_txt_file("txt/settings/liqs/pad_protector.txt",0)
        self.txt_ops.quick_write_txt_file("txt/settings/travel_mode.txt",0)
        self.txt_ops.quick_write_txt_file("txt/settings/skim_mode.txt",0)

        self.txt_ops.quick_write_txt_file_plus("txt/stats/init_balance_1",0)
        self.txt_ops.quick_write_txt_file_plus("txt/stats/init_balance_2",0)
        #
        self.txt_ops.quick_write_txt_file_plus("txt/settings/email/3m_stale_mins.txt",17)
        self.txt_ops.quick_write_txt_file_plus("txt/settings/email/4h_stale_mins.txt",10000)
        self.txt_ops.quick_write_txt_file_plus("txt/settings/email/use_rsi_3m.txt",1)
        self.txt_ops.quick_write_txt_file_plus("txt/settings/email/use_macd_3m.txt",1)
        self.txt_ops.quick_write_txt_file_plus("txt/settings/email/use_rsi_4h.txt",1)
        self.txt_ops.quick_write_txt_file_plus("txt/settings/email/use_macd_4h.txt",1)

    

##
##        folder = 'txt/login'
##
##        for filename in os.listdir(folder):
##            file_path = os.path.join(folder, filename)
##            try:
##                if os.path.isfile(file_path) or os.path.islink(file_path):
##                    os.unlink(file_path)
##                elif os.path.isdir(file_path):
##                    shutil.rmtree(file_path)
##            except Exception as e:
##                print('Failed to delete %s. Reason: %s' % (file_path, e))
##
##
##


        folder = 'txt/setup'

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))








        folder = 'txt/withdraw'

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))




    def clear_Recent(self):

        print("\nClearing Recent Data...")
       
        self.txt_ops.quick_write_txt_file("txt/active_account.txt",1)
        self.txt_ops.quick_write_txt_file("txt/tab_account.txt",0)
        self.txt_ops.quick_write_txt_file("txt/full_auto.txt",0)
        self.txt_ops.quick_write_txt_file("txt/full_auto_account.txt",0)
    




def check_Module():

    a = Admin()

    prep_pack = a.clear_Configs()





if __name__ == '__main__':

    check_Module()

