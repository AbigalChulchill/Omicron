import sys
sys.path.insert(1,'lib')

#UI libs
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QMainWindow, QWidget, QApplication, QTabWidget, QTabBar, QLabel, QPushButton, QCheckBox, QSlider)
from PyQt5.QtWidgets import (QStatusBar, QVBoxLayout, QMenuBar, QAction, QMessageBox, QDialog)
from PyQt5.QtCore import pyqtSlot
import time
from _txt_Ops import *
from _Fetch_Settings import *
from _Order_Pos_Functions import *
from _Record_Stats import *


class Popup_Manager(QWidget):

    def __init__(self):

        super().__init__()
        self.txt_ops = txt_Ops()
        self.current_tab_id = 0


    def popup_Simple(self,exec_string):

        
        def apply(Dialog):

            print("\nApply clicked.")


            if exec_string == "Force Close":

                self.current_tab_id = self.txt_ops.quick_read_txt_file('txt/last_tab_account.txt')

                account_no = int(self.current_tab_id)

                get_account_settings = Settings(account_no).load_Account_Variables()

                pair_symbol = get_account_settings[3]

                order_pos_functions = Order_Pos_Functions(account_no)

                a = order_pos_functions.force_Close_Position(pair_symbol)

                record_stats = Record_Stats(account_no)
                record_stats.request_Write_USDT_Balance()

               
            
            Dialog.close()
           

        def cancel(Dialog):

            print("\nClosing popup...")
            Dialog.close()
            
            


        basic_dialog = QDialog(self)

        #Window settings
        title_str = " Are you sure you want to " + exec_string + "?"
        basic_dialog.setWindowTitle(title_str)
        basic_dialog.resize(300,60)

        #BUTTON - APPLY
        button_apply = QtWidgets.QPushButton(basic_dialog)
        button_apply.setGeometry(QtCore.QRect(60,20,60,20))
        button_apply.setObjectName("button_apply")
        button_apply.setText("Yes")
        button_apply.clicked.connect(lambda:apply(basic_dialog))

        #BUTTON - CANCEL
        button_cancel = QtWidgets.QPushButton(basic_dialog)
        button_cancel.setGeometry(QtCore.QRect(180,20,60,20))
        button_cancel.setObjectName("button_cancel")
        button_cancel.setText("No")
        button_cancel.clicked.connect(lambda:cancel(basic_dialog))
        
        basic_dialog.exec_()



################ POPUPS ######################################################################################################


    def popup_Allow_Auto(self):

        self.current_tab_id = self.txt_ops.quick_read_txt_file('txt/last_tab_account.txt')


        f = []
        init_dict = {}
        folder_path = 'txt/setup/' + str(self.current_tab_id) + '/'
        make_str_account = folder_path + 'setup_' + str(self.current_tab_id) + '.txt'
        init_dict = self.txt_ops.create_dict_from_txt(make_str_account,'=')
        
        def apply_Method(Dialog):

            print("\nApply clicked.")
            Dialog.close()

        def cancel_Method(Dialog):

            print("\nCancel clicked.")
            Dialog.close()

        def checkbox_Changed(Dialog,input_checkbox,pair_symbol):
                 
            for (dirpath, dirnames, filenames) in walk(folder_path):
                f.extend(filenames)
                break
     
            if input_checkbox.isChecked():
                print("\nTurning",pair_symbol,"on...")
                for i in range(len(f)):
                    file_name = f[i]
                    print('file_name',file_name)
                    if str(pair_symbol) in str(file_name):
                        self.txt_ops.replace_Specific_Line(folder_path+file_name,1,'active=1')
            else:
                print("\nTurning",pair_symbol,"off...")
                for i in range(len(f)):
                    file_name = f[i]
                    print('file_name',file_name)
                    if str(pair_symbol) in str(file_name):
                        self.txt_ops.replace_Specific_Line(folder_path+file_name,1,'active=0')

        def load_Checked_States(pair_symbol,checkbox_ID):

            active_value = 0

            for (dirpath, dirnames, filenames) in walk(folder_path):
                f.extend(filenames)
                break
          
            for i in range(len(f)):
                file_name = f[i]
                  
                if str(pair_symbol) in str(file_name):
                    create_dict = self.txt_ops.create_dict_from_txt(folder_path+file_name,'=')
                    active_value = int(create_dict['active'])
            
            if active_value == 1:
                checkbox_ID.setChecked(True)
            elif active_value == 0:
                checkbox_ID.setChecked(False)

        allow_auto_dialog = QDialog(self)

        #Window settings
        allow_auto_dialog.setWindowTitle(" Pair symbols allowed to auto-trade")
        allow_auto_dialog.resize(350, 200)

        #checkbox BTC
        checkbox_btc = QCheckBox("BTCUSDT",allow_auto_dialog)
        checkbox_btc.move(70,30)
        checkbox_btc.stateChanged.connect(lambda:checkbox_Changed(allow_auto_dialog,checkbox_btc,'BTCUSDT'))
        load_Checked_States('BTCUSDT',checkbox_btc)

        #checkbox ETH
        checkbox_eth = QCheckBox("ETHUSDT",allow_auto_dialog)
        checkbox_eth.move(70,55)
        checkbox_eth.stateChanged.connect(lambda:checkbox_Changed(allow_auto_dialog,checkbox_eth,'ETHUSDT'))
        load_Checked_States('ETHUSDT',checkbox_eth)

        #checkbox LTC
        checkbox_ltc = QCheckBox("LTCUSDT",allow_auto_dialog)
        checkbox_ltc.move(70,80)
        checkbox_ltc.stateChanged.connect(lambda:checkbox_Changed(allow_auto_dialog,checkbox_ltc,'LTCUSDT'))
        load_Checked_States('LTCUSDT',checkbox_ltc)

        #checkbox ADA
        checkbox_ada = QCheckBox("ADAUSDT",allow_auto_dialog)
        checkbox_ada.move(70,105)
        checkbox_ada.stateChanged.connect(lambda:checkbox_Changed(allow_auto_dialog,checkbox_ada,'ADAUSDT'))
        load_Checked_States('ADAUSDT',checkbox_ada)
        
        #checkbox BNB
        checkbox_bnb = QCheckBox("BNBUSDT",allow_auto_dialog)
        checkbox_bnb.move(200,30)
        checkbox_bnb.stateChanged.connect(lambda:checkbox_Changed(allow_auto_dialog,checkbox_bnb,'BNBUSDT'))
        load_Checked_States('BNBUSDT',checkbox_bnb)

        #BUTTON - APPLY
        button_apply = QtWidgets.QPushButton(allow_auto_dialog)
        button_apply.setGeometry(QtCore.QRect(70,160,70,20))
        button_apply.setObjectName("button_apply")
        button_apply.setText("Apply")
        button_apply.clicked.connect(lambda:apply_Method(allow_auto_dialog))

        #BUTTON - CANCEL
        button_cancel = QtWidgets.QPushButton(allow_auto_dialog)
        button_cancel.setGeometry(QtCore.QRect(210,160,70,20))
        button_cancel.setObjectName("button_cancel")
        button_cancel.setText("Cancel")
        button_cancel.clicked.connect(lambda:cancel_Method(allow_auto_dialog))
        
        allow_auto_dialog.exec_()



    def popup_Sup_Res_Settings(self):

        init_dict = {}
        self.current_tab_id = self.txt_ops.quick_read_txt_file('txt/last_tab_account.txt')

        #search mins file
        search_mins_path = 'txt/settings/mode/mode_back.txt'

        #get last pair symbol from settings
        settings = Settings(self.current_tab_id)
        pair_symbol = settings.load_Account_Variables()[4]

        path_str = 'txt/setup/' + str(self.current_tab_id) + '/setup_' + str(self.current_tab_id) + '_' + str(pair_symbol) + '.txt'
        init_dict = self.txt_ops.create_dict_from_txt(path_str,'=')
        
        def apply_Sup_Res(Dialog,mode_algo,mode_buffer,mins_back):

            print("\nApply clicked.")

            str_mode_algo = 'mode_algo=' + str(mode_algo)
            str_mode_buffer = 'mode_buffer=' + str(mode_buffer)
            mins_back = 'mode_search_mins=' + str(mins_back)

            self.txt_ops.replace_Specific_Line(path_str,29,str_mode_algo)
            self.txt_ops.replace_Specific_Line(path_str,30,str_mode_buffer)
            self.txt_ops.replace_Specific_Line(path_str,40,mins_back)
            #self.txt_ops.quick_write_txt_file(search_mins_path,mins_back)

            Dialog.close()

        def cancel_Sup_Res(Dialog):

            print("\nCancel clicked.")
            Dialog.close()

        sup_res_dialog = QDialog(self)

        #Window settings
        sup_res_dialog.setWindowTitle(" Gold/Silver Settings")
        sup_res_dialog.resize(350, 200)

        read_value_algo = str(init_dict['mode_algo'])
        read_value_buffer = str(init_dict['mode_buffer'])
        read_value_mins_back = str(init_dict['mode_search_mins'])

        #PLAIN LABEL - TYPE
        label_supres_type = QtWidgets.QLabel(sup_res_dialog)
        label_supres_type.setGeometry(QtCore.QRect(70,25,110,20))
        label_supres_type.setObjectName("label_supres_type")
        label_supres_type.setText("Algorithm type")

        #COMBO BOX
        combo_supres_type = QtWidgets.QComboBox(sup_res_dialog)
        combo_supres_type.setGeometry(QtCore.QRect(210,25,70,20))
        combo_supres_type.setObjectName("combo_supres_type")
        add_items = ['GOLD','SILVER','EITHER','BOTH']
        combo_supres_type.clear()
        combo_supres_type.addItems(add_items)

        #set index based on current text file settings
        index = combo_supres_type.findText(read_value_algo,QtCore.Qt.MatchFixedString)
        if index >= 0:
             combo_supres_type.setCurrentIndex(index)
             
        #PLAIN LABEL - BUFFER
        label_supres_buffer = QtWidgets.QLabel(sup_res_dialog)
        label_supres_buffer.setGeometry(QtCore.QRect(70,65,110,20))
        label_supres_buffer.setObjectName("label_supres_buffer")
        label_supres_buffer.setText("Buffer from lines (%)")

        #DATA LABEL - BUFFER
        data_label_supres_buffer = QtWidgets.QLineEdit(sup_res_dialog)
        data_label_supres_buffer.setGeometry(QtCore.QRect(210,65,70,20))
        data_label_supres_buffer.setObjectName("data_label_supres_buffer")
        data_label_supres_buffer.setText(read_value_buffer)

        #PLAIN LABEL - MINS BACK
        label_mins_back = QtWidgets.QLabel(sup_res_dialog)
        label_mins_back.setGeometry(QtCore.QRect(70,105,110,20))
        label_mins_back.setObjectName("label_mins_back")
        label_mins_back.setText("Search minutes")

        #DATA LABEL - MINS BACK
        data_label_mins_back = QtWidgets.QLineEdit(sup_res_dialog)
        data_label_mins_back.setGeometry(QtCore.QRect(210,105,70,20))
        data_label_mins_back.setObjectName("data_label_mins_back")
        data_label_mins_back.setText(read_value_mins_back)

        #BUTTON - APPLY
        button_test = QtWidgets.QPushButton(sup_res_dialog)
        button_test.setGeometry(QtCore.QRect(70,150,70,20))
        button_test.setObjectName("button_test")
        button_test.setText("Apply")
        button_test.clicked.connect(lambda:apply_Sup_Res(sup_res_dialog,str(combo_supres_type.currentText()),str(data_label_supres_buffer.text()),\
                                                         str(data_label_mins_back.text())))

        #BUTTON - CANCEL
        button_cancel = QtWidgets.QPushButton(sup_res_dialog)
        button_cancel.setGeometry(QtCore.QRect(210,150,70,20))
        button_cancel.setObjectName("button_test")
        button_cancel.setText("Cancel")
        button_cancel.clicked.connect(lambda:cancel_Sup_Res(sup_res_dialog))
        
        sup_res_dialog.exec_()



    def popup_Avoid_Settings(self):

        #get settings is avoid enabled
        init_dict = {}
        self.current_tab_id = self.txt_ops.quick_read_txt_file('txt/last_tab_account.txt')

        #get last pair symbol from settings
        settings = Settings(self.current_tab_id)
        pair_symbol = settings.load_Account_Variables()[4]
        
        path_str = 'txt/setup/' + str(self.current_tab_id) + '/setup_' + str(self.current_tab_id) + '_' + str(pair_symbol) + '.txt'
        init_dict = self.txt_ops.create_dict_from_txt(path_str,'=')

        def apply_Method(Dialog,long_value,short_value):

            print("\nApply clicked.")

            #make strings
            long_value = 'avoid_region_long=' + str(long_value)
            short_value = 'avoid_region_short=' + str(short_value)

            #write vars
            write_long = self.txt_ops.replace_Specific_Line(path_str,34,long_value)
            write_short = self.txt_ops.replace_Specific_Line(path_str,35,short_value)

            Dialog.close()

        def cancel_Method(Dialog):

            print("\nCancel clicked.")
            Dialog.close()

        avoid_settings_dialog = QDialog(self)

        #Window settings
        avoid_settings_dialog.setWindowTitle(" Avoid Regions Settings")
        avoid_settings_dialog.resize(350, 200)

        #read vars
        read_long = settings.load_Trade_Variables(pair_symbol)[33]
        read_short = settings.load_Trade_Variables(pair_symbol)[34]
          
        #PLAIN LABEL - DONT ALLOW LONGS ABOVE
        label_avoid_longs_above = QtWidgets.QLabel(avoid_settings_dialog)
        label_avoid_longs_above.setGeometry(QtCore.QRect(70,35,118,20))
        label_avoid_longs_above.setObjectName("label_avoid_longs_above")
        label_avoid_longs_above.setText("Avoid Long entry above:")
        #
        data_label_avoid_longs_above = QtWidgets.QLineEdit(avoid_settings_dialog)
        data_label_avoid_longs_above.setGeometry(QtCore.QRect(210,35,70,20))
        data_label_avoid_longs_above.setObjectName("data_label_avoid_longs_above")
        data_label_avoid_longs_above.setText(str(read_long))

        #PLAIN LABEL - DONT ALLOW SHORTS BELOW
        label_avoid_shorts_below = QtWidgets.QLabel(avoid_settings_dialog)
        label_avoid_shorts_below.setGeometry(QtCore.QRect(70,75,118,20))
        label_avoid_shorts_below.setObjectName("label_avoid_shorts_below")
        label_avoid_shorts_below.setText("Avoid Short entry below:")
        #
        data_label_avoid_shorts_below = QtWidgets.QLineEdit(avoid_settings_dialog)
        data_label_avoid_shorts_below.setGeometry(QtCore.QRect(210,75,70,20))
        data_label_avoid_shorts_below.setObjectName("data_label_avoid_shorts_below")
        data_label_avoid_shorts_below.setText(str(read_short))

        #BUTTON - APPLY
        button_apply = QtWidgets.QPushButton(avoid_settings_dialog)
        button_apply.setGeometry(QtCore.QRect(70,150,70,20))
        button_apply.setObjectName("button_apply")
        button_apply.setText("Apply")
        button_apply.clicked.connect(lambda:apply_Method(avoid_settings_dialog,str(data_label_avoid_longs_above.text()),str(data_label_avoid_shorts_below.text())))

        #BUTTON - CANCEL
        button_cancel = QtWidgets.QPushButton(avoid_settings_dialog)
        button_cancel.setGeometry(QtCore.QRect(210,150,70,20))
        button_cancel.setObjectName("button_cancel")
        button_cancel.setText("Cancel")
        button_cancel.clicked.connect(lambda:cancel_Method(avoid_settings_dialog))
        
        avoid_settings_dialog.exec_()



    def popup_Email_Settings(self):

        def apply_Method(Dialog,email_name,app_pass):

            print("\nApply clicked.")

            write_email_name = self.txt_ops.quick_write_txt_file('txt/settings/email/account/email.txt',str(email_name))
            write_app_pass = self.txt_ops.quick_write_txt_file('txt/settings/email/account/app_pass.txt',str(app_pass))

            Dialog.close()

        def cancel_Method(Dialog):

            print("\nCancel clicked.")
            Dialog.close()

        email_settings_dialog = QDialog(self)

        #Window settings
        email_settings_dialog.setWindowTitle(" Gmail Account Settings")
        email_settings_dialog.resize(350, 200)

        #read current vars
        read_email_name = self.txt_ops.quick_read_txt_file('txt/settings/email/account/email.txt')
        read_app_pass = self.txt_ops.quick_read_txt_file('txt/settings/email/account/app_pass.txt')
          
        #PLAIN LABEL - EMAIL
        label_email_name = QtWidgets.QLabel(email_settings_dialog)
        label_email_name.setGeometry(QtCore.QRect(40,35,110,20))
        label_email_name.setObjectName("label_email_name")
        label_email_name.setText("Email")
        #DATA LABEL - EMAIL
        data_label_email_name = QtWidgets.QLineEdit(email_settings_dialog)
        data_label_email_name.setGeometry(QtCore.QRect(90,35,220,20))
        data_label_email_name.setObjectName("data_label_email_name")
        data_label_email_name.setText(read_email_name)

        #PLAIN LABEL - PASS
        label_app_pass = QtWidgets.QLabel(email_settings_dialog)
        label_app_pass.setGeometry(QtCore.QRect(40,75,110,20))
        label_app_pass.setObjectName("label_app_pass")
        label_app_pass.setText("Password")
        #DATA LABEL - PASS
        data_label_app_pass = QtWidgets.QLineEdit(email_settings_dialog)
        data_label_app_pass.setGeometry(QtCore.QRect(90,75,220,20))
        data_label_app_pass.setObjectName("data_label_app_pass")
        data_label_app_pass.setText(read_app_pass)
        data_label_app_pass.setEchoMode(QtWidgets.QLineEdit.Password)

        #BUTTON - APPLY
        button_apply = QtWidgets.QPushButton(email_settings_dialog)
        button_apply.setGeometry(QtCore.QRect(70,150,70,20))
        button_apply.setObjectName("button_apply")
        button_apply.setText("Apply")
        button_apply.clicked.connect(lambda:apply_Method(email_settings_dialog,data_label_email_name.text(),data_label_app_pass.text()))

        #BUTTON - CANCEL
        button_cancel = QtWidgets.QPushButton(email_settings_dialog)
        button_cancel.setGeometry(QtCore.QRect(210,150,70,20))
        button_cancel.setObjectName("button_cancel")
        button_cancel.setText("Cancel")
        button_cancel.clicked.connect(lambda:cancel_Method(email_settings_dialog))
        
        email_settings_dialog.exec_()





    def popup_Rebuild_Settings(self):

        init_dict = {}

        self.current_tab_id = self.txt_ops.quick_read_txt_file('txt/last_tab_account.txt')

        #get last pair symbol from dropdown 3/4
        settings = Settings(self.current_tab_id)
        pair_symbol = settings.load_Account_Variables()[4]
        
        path_str = 'txt/setup/' + str(self.current_tab_id) + '/setup_' + str(self.current_tab_id) + '_' + pair_symbol + '.txt'

        init_dict = self.txt_ops.create_dict_from_txt(path_str,'=')
        
        def apply_Settings(Dialog,tp_type,sl_type):

            print("\nApply clicked.")

            tp_type_str = 'tp_type=' + str(tp_type)
            sl_type_str = 'sl_type=' + str(sl_type)

            write_long = self.txt_ops.replace_Specific_Line(path_str,32,tp_type_str)
            write_short = self.txt_ops.replace_Specific_Line(path_str,33,sl_type_str)

            Dialog.close()

        def cancel_Dialog(Dialog):

            print("\nClosing Popup...")
            Dialog.close()

        def checkbox_Changed(Dialog,input_checkbox):

            if input_checkbox.isChecked():
                self.txt_ops.quick_write_txt_file('txt/settings/rebuild/rebuild_all.txt',1)
            else:
                self.txt_ops.quick_write_txt_file('txt/settings/rebuild/rebuild_all.txt',0)


        def load_Checked_States(checkbox_ID):

            active_value = int(self.txt_ops.quick_read_txt_file('txt/settings/rebuild/rebuild_all.txt'))

            if active_value == 1:
                checkbox_ID.setChecked(True)
            elif active_value == 0:
                checkbox_ID.setChecked(False)


        rebuild_dialog = QDialog(self)

        #Window settings
        rebuild_dialog.setWindowTitle(" Build Take Profit/Stop Loss Settings")
        rebuild_dialog.resize(350, 200)

        read_tp_type = str(list(init_dict.values())[31])
        read_sl_type = str(list(init_dict.values())[32])

        #PLAIN LABEL - TP
        label_tp_type = QtWidgets.QLabel(rebuild_dialog)
        label_tp_type.setGeometry(QtCore.QRect(50,35,180,20))
        label_tp_type.setObjectName("label_tp_type")
        label_tp_type.setText("Take Profit Amount")

        #COMBO
        combo_tp_type = QtWidgets.QComboBox(rebuild_dialog)
        combo_tp_type.setGeometry(QtCore.QRect(210,35,70,20))
        combo_tp_type.setObjectName("combo_tp_type")
        #
        add_items_tp = ['FULL','HALF','NONE']
        combo_tp_type.clear()
        combo_tp_type.addItems(add_items_tp)

        #set index based on current text file settings
        index = combo_tp_type.findText(read_tp_type,QtCore.Qt.MatchFixedString)
        if index >= 0:
             combo_tp_type.setCurrentIndex(index)

        #PLAIN LABEL - SL
        label_sl_type = QtWidgets.QLabel(rebuild_dialog)
        label_sl_type.setGeometry(QtCore.QRect(50,75,180,20))
        label_sl_type.setObjectName("label_sl_type")
        label_sl_type.setText("Stop Loss Amount")

        #COMBO BOX
        combo_sl_type = QtWidgets.QComboBox(rebuild_dialog)
        combo_sl_type.setGeometry(QtCore.QRect(210,75,70,20))
        combo_sl_type.setObjectName("combo_sl_type")
        #
        add_items_sl = ['FULL','HALF','NONE']
        combo_sl_type.clear()
        combo_sl_type.addItems(add_items_sl)

        #set index based on current text file settings
        index = combo_sl_type.findText(read_sl_type,QtCore.Qt.MatchFixedString)
        if index >= 0:
             combo_sl_type.setCurrentIndex(index)


        #checkbox BTC
        checkbox_all = QCheckBox("Rebuild All (Slow)",rebuild_dialog)
        checkbox_all.move(50,110)
        checkbox_all.stateChanged.connect(lambda:checkbox_Changed(rebuild_dialog,checkbox_all))
        load_Checked_States(checkbox_all)
             

        #BUTTON - APPLY
        button_apply = QtWidgets.QPushButton(rebuild_dialog)
        button_apply.setGeometry(QtCore.QRect(70,150,70,20))
        button_apply.setObjectName("button_apply")
        button_apply.setText("Apply")
        button_apply.clicked.connect( lambda:apply_Settings(rebuild_dialog,str(combo_tp_type.currentText()),str(combo_sl_type.currentText())))

        #BUTTON - CANCEL
        button_cancel = QtWidgets.QPushButton(rebuild_dialog)
        button_cancel.setGeometry(QtCore.QRect(210,150,70,20))
        button_cancel.setObjectName("button_cancel")
        button_cancel.setText("Cancel")
        button_cancel.clicked.connect(lambda:cancel_Dialog(rebuild_dialog))
        
        rebuild_dialog.exec_()








    def popup_Liq_SL_Settings(self):

        init_dict = {}
        self.current_tab_id = self.txt_ops.quick_read_txt_file('txt/last_tab_account.txt')

        #get last pair symbol from dropdown 3/4
        settings = Settings(self.current_tab_id)
        pair_symbol = settings.load_Account_Variables()[4]
        
        path_str = 'txt/setup/' + str(self.current_tab_id) + '/setup_' + str(self.current_tab_id) + '_' + str(pair_symbol) + '.txt'
        init_dict = self.txt_ops.create_dict_from_txt(path_str,'=')
        
        def apply_Settings(Dialog,squeeze):

            print("\nApply clicked.")
            str_squeeze = 'stop_to_limit_spread=' + str(squeeze)
            #self.replace_Pair_Settings_Line(8,str_squeeze)
            write = self.txt_ops.replace_Specific_Line(path_str,8,str_squeeze)
            Dialog.close()

        def cancel_Dialog(Dialog):

            print("\nClosing Stop Loss Settings Popup...")
            Dialog.close()

        sl_dialog = QDialog(self)

        #Window settings
        sl_dialog.setWindowTitle(" Near Liquidation Price Stop Loss Settings")
        sl_dialog.resize(350, 200)

        read_current_squeeze = str(list(init_dict.values())[7])

        y_first_data_row = 55
        
        label_squeeze = QtWidgets.QLabel(sl_dialog)
        label_squeeze.setGeometry(QtCore.QRect(55,y_first_data_row,180,20))
        label_squeeze.setObjectName("label_squeeze")
        label_squeeze.setText("Dist. from Liquidation Price (%)")

        #DATA LABEL - BUFFER
        data_label_squeeze = QtWidgets.QLineEdit(sl_dialog)
        data_label_squeeze.setGeometry(QtCore.QRect(220,y_first_data_row,70,20))
        data_label_squeeze.setObjectName("data_label_squeeze")
        data_label_squeeze.setText(read_current_squeeze)

        #BUTTON - APPLY
        button_apply = QtWidgets.QPushButton(sl_dialog)
        button_apply.setGeometry(QtCore.QRect(70,150,70,20))
        button_apply.setObjectName("button_apply")
        button_apply.setText("Apply")
        button_apply.clicked.connect(lambda:apply_Settings(sl_dialog,str(data_label_squeeze.text())))

        #BUTTON - CANCEL
        button_cancel = QtWidgets.QPushButton(sl_dialog)
        button_cancel.setGeometry(QtCore.QRect(210,150,70,20))
        button_cancel.setObjectName("button_cancel")
        button_cancel.setText("Cancel")
        button_cancel.clicked.connect(lambda:cancel_Dialog(sl_dialog))
        
        sl_dialog.exec_()






    def popup_Guard_Settings(self):
        pass


        
    def popup_Pad_Settings(self):

        read_value_allow = str(self.txt_ops.quick_read_txt_file('txt/settings/guard/allow_multiple.txt'))
        read_value_risk = str(self.txt_ops.quick_read_txt_file('txt/settings/guard/risk_multiple.txt'))
        read_value_amount = str(self.txt_ops.quick_read_txt_file('txt/settings/guard/pad_move_amount.txt'))

        def apply_Method(Dialog,allow,risk,amount):

            print("\nApply clicked.")
            
            write_allow = self.txt_ops.quick_write_txt_file('txt/settings/guard/allow_multiple.txt',allow)
            write_risk = self.txt_ops.quick_write_txt_file('txt/settings/guard/risk_multiple.txt',risk)
            write_amount = self.txt_ops.quick_write_txt_file('txt/settings/guard/pad_move_amount.txt',amount)

            Dialog.close()

        def cancel_Method(Dialog):

            print("\nCancel clicked.")
            Dialog.close()

        guard_dialog = QDialog(self)

        #Window settings
        guard_dialog.setWindowTitle(" Padding Protection Settings")
        guard_dialog.resize(350, 200)

        #PLAIN LABEL - ALLOW
        label_allow = QtWidgets.QLabel(guard_dialog)
        label_allow.setGeometry(QtCore.QRect(70,35,210,20))
        label_allow.setObjectName("label_allow")
        label_allow.setText("Allow Multiple")
        #DATA LABEL - ALLOW
        data_label_allow = QtWidgets.QLineEdit(guard_dialog)
        data_label_allow.setGeometry(QtCore.QRect(250,35,30,20))
        data_label_allow.setObjectName("data_label_allow")
        data_label_allow.setText(read_value_allow)

        #PLAIN LABEL - RISK
        label_risk = QtWidgets.QLabel(guard_dialog)
        label_risk.setGeometry(QtCore.QRect(70,70,210,20))
        label_risk.setObjectName("label_risk")
        label_risk.setText("Risk Multiple")
        #DATA LABEL - RISK
        data_label_risk = QtWidgets.QLineEdit(guard_dialog)
        data_label_risk.setGeometry(QtCore.QRect(250,70,30,20))
        data_label_risk.setObjectName("data_label_risk")
        data_label_risk.setText(read_value_risk)

        #PLAIN LABEL - SELL
        label_amount = QtWidgets.QLabel(guard_dialog)
        label_amount.setGeometry(QtCore.QRect(70,105,210,20))
        label_amount.setObjectName("label_amount")
        label_amount.setText("Move amount (USDT)")
        #DATA LABEL - SELL
        data_label_amount = QtWidgets.QLineEdit(guard_dialog)
        data_label_amount.setGeometry(QtCore.QRect(250,105,30,20))
        data_label_amount.setObjectName("data_label_amount")
        data_label_amount.setText(read_value_amount)

        #BUTTON - APPLY
        button_apply = QtWidgets.QPushButton(guard_dialog)
        button_apply.setGeometry(QtCore.QRect(70,150,70,20))
        button_apply.setObjectName("button_apply")
        button_apply.setText("Apply")
        button_apply.clicked.connect(lambda:apply_Method(guard_dialog,str(data_label_allow.text()),str(data_label_risk.text()),str(data_label_amount.text())))

        #BUTTON - CANCEL
        button_cancel = QtWidgets.QPushButton(guard_dialog)
        button_cancel.setGeometry(QtCore.QRect(210,150,70,20))
        button_cancel.setObjectName("button_cancel")
        button_cancel.setText("Cancel")
        button_cancel.clicked.connect(lambda:cancel_Method(guard_dialog))
        
        guard_dialog.exec_()


        

        
    def popup_Skim_Settings(self):

        settings_file_path = 'txt/settings/skim/skim_amount.txt'

        read_value_amount = str(self.txt_ops.quick_read_txt_file(settings_file_path))

        def apply_Method(Dialog,amount):

            print("\nApply clicked.")
            
            write_amount = self.txt_ops.quick_write_txt_file(settings_file_path,amount)

            Dialog.close()

        def cancel_Method(Dialog):

            print("\nCancel clicked.")
            Dialog.close()

        skim_dialog = QDialog(self)

        #Window settings
        skim_dialog.setWindowTitle(" Skim Settings")
        skim_dialog.resize(350, 200)

        #PLAIN LABEL - ALLOW
        label_amount = QtWidgets.QLabel(skim_dialog)
        label_amount.setGeometry(QtCore.QRect(70,35,210,20))
        label_amount.setObjectName("label_allow")
        label_amount.setText("Skim Amount (USDT)")
        #DATA LABEL - ALLOW
        data_label_amount = QtWidgets.QLineEdit(skim_dialog)
        data_label_amount.setGeometry(QtCore.QRect(250,35,30,20))
        data_label_amount.setObjectName("data_label_amount")
        data_label_amount.setText(read_value_amount)

        #BUTTON - APPLY
        button_apply = QtWidgets.QPushButton(skim_dialog)
        button_apply.setGeometry(QtCore.QRect(70,150,70,20))
        button_apply.setObjectName("button_apply")
        button_apply.setText("Apply")
        button_apply.clicked.connect(lambda:apply_Method(skim_dialog,  str(data_label_amount.text())   ))

        #BUTTON - CANCEL
        button_cancel = QtWidgets.QPushButton(skim_dialog)
        button_cancel.setGeometry(QtCore.QRect(210,150,70,20))
        button_cancel.setObjectName("button_cancel")
        button_cancel.setText("Cancel")
        button_cancel.clicked.connect(lambda:cancel_Method(skim_dialog))
        
        skim_dialog.exec_()




    def popup_Spread_Settings(self):
        pass




if __name__ == '__main__':

    app = QApplication(['Omicron 2.0'])
    w = Window()
    #
    #
   
    #
    w.show()
    #
    sys.exit(app.exec_())







