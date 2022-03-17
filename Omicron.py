import sys
sys.path.insert(1,'lib')

import requests
import lxml
import time
import os
os.getpid()
from os import path
from os.path import exists
import subprocess as s
from playsound import playsound
import webbrowser
import math
from _Crash_Manager import *

#UI libs
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QMainWindow, QWidget, QApplication, QTabWidget, QTabBar, QLabel, QPushButton, QCheckBox, QSlider)
from PyQt5.QtWidgets import (QStatusBar, QVBoxLayout, QMenuBar, QAction, QMessageBox, QDialog)
from PyQt5.QtCore import pyqtSlot

#my libs
from _Balance_Functions import *
from _Maths_Functions import *
from _Account_Functions import *
from _Price_Functions import *
from _Withdraw_Functions import *
from _txt_Ops import *
from _Order_Pos_Functions import *
from _csv_Ops import *
from urllib.parse import urljoin, urlencode
from _Precision_Manager import *
from version_scraper import *
from _Admin import *
from _Signals import *
from _Record_Stats import *
from _Fetch_Settings import *
from _Popup_Manager import *

#high DPI scaling
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class MainWidget(QWidget):

    def __init__(self, textLabel, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)

class Window(QWidget):

    def __init__(self):

        super().__init__()
        self.setWindowIcon(QtGui.QIcon('img/omicron_icon.png'))
        self.maths_functions = Maths_Functions(1)

        def appExec():
            app = QApplication(sys.argv)
            app.exec_()

        def my_exception_hook(exctype, value, traceback):
            print(exctype, value, traceback)
            sys._excepthook(exctype, value, traceback)
            sys.exit(1)

        sys._excepthook = sys.excepthook
        sys.excepthook = my_exception_hook

        self.this_version = 313

        self.setObjectName("Main_Window")
        self.setWindowTitle(" Omicron " + str(self.this_version / 100) + "  |  Automate. Win more. Play more.")
        self.width = 945
        self.height = 640
        self.resize(self.width, self.height)
        self.translate = QtCore.QCoreApplication.translate
        
        #Count Login Files - Sort numerically
        self.accounts_list = self.maths_functions.count_Files('txt/login')[1]
        self.accounts_list = [int(x) for x in self.accounts_list]
        self.accounts_list.sort()
        self.accounts_count = len(self.accounts_list)

        self.refresh_ms = 1000
        self.pos_array = []
        self.global_activate = 0
        self.load_chart = 0
        self.balance = 0
        self.count = 0
        self.current_tab_id = 0
        self.number_of_tabs = 0
        self.txt_ops = txt_Ops()
        self.csv_ops = csv_Ops()
        self.global_wins_amount = 0
        self.global_losses_amount = 0
        self.total_balance = 0
        self.total_margin = 0
        self.tab_position_side = ''
        self.current_offline_address = ''
        self.tag_list = []
        self.popup_manager = Popup_Manager()
        self.current_pair_selected = ''
        self.create_style_left_align_text = "text-align:left;padding-left:8px;"
        icon_settings = QtGui.QPixmap("img/settings.png")
        self.max_leverage_amount = 30

        if os.path.isfile('txt/login/login_1.txt') == True:
            self.first_run = False
        else:
            self.first_run = True

        #set a bold font
        bold_font = QtGui.QFont()
        bold_font.setBold(True)
        bold_font.setWeight(75)
        
        #first run
        self.first_run_complete = 0
        self.tabs_looked_at = []

        self.master_Tabs_Container = QTabWidget()
        self.tab_type = 'Dashboard'
        self.tabColors = {}


        def create_Plus_Group():

            self.tab_Plus = MainWidget('')
            self.master_Tabs_Container.addTab(self.tab_Plus,'+')

            #HEADER - Add a Binance Account
            self.header_add_binance = QtWidgets.QLabel(self.master_Tabs_Container)
            self.header_add_binance.setFont(bold_font)
            self.header_add_binance.setObjectName("header_add_binance")
            self.header_add_binance.setText("Add a Binance Account")
            self.header_add_binance.setGeometry(QtCore.QRect(-999, -999, 0, 0))

            #PLAIN LABEL - ADD API KEY
            self.label_add_account_api = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_add_account_api.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_add_account_api.setObjectName("label_add_account_api")
            self.label_add_account_api.setText("API Key")
            #DATA LABEL - ADD API KEY
            self.data_label_add_account_api = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_add_account_api.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_add_account_api.setObjectName("data_label_add_account_api")

            #PLAIN LABEL - ADD SEC KEY
            self.label_add_account_sec = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_add_account_sec.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_add_account_sec.setObjectName("label_add_account_sec")
            self.label_add_account_sec.setText("Secret Key")
            #DATA LABEL - ADD SEC KEY
            self.data_label_add_account_sec = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_add_account_sec.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_add_account_sec.setObjectName("data_label_add_account_sec")
            self.data_label_add_account_sec.setEchoMode(QtWidgets.QLineEdit.Password)

            #ADD ACCOUNT BUTTON
            self.label_what_this = QtWidgets.QPushButton(self.master_Tabs_Container)
            create_api_tut_style = "background-color:#fafafa;color:blue;text-decoration:underline;border:none;"
            self.label_what_this.setStyleSheet(create_api_tut_style)

            self.label_what_this.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_what_this.setObjectName("label_what_this")
            self.label_what_this.setText("What is an API/Secret Key?")
            self.label_what_this.clicked.connect(self.get_API_Tutorial)
            self.label_what_this.setToolTip("An API Key is essentially a login password consisting of two parts, which will allow Omicron to trade on your behalf. "\
                                            "Go to your Binance profile icon and choose 'API Management' at the bottom of the list to create one.<br>")
            
            #HEADER - Add a Travel Account
            self.header_add_travel_api = QtWidgets.QLabel(self.master_Tabs_Container)
            self.header_add_travel_api.setFont(bold_font)
            self.header_add_travel_api.setObjectName("header_add_travel_api")
            self.header_add_travel_api.setText("(Optional) Add a Travel Mode API - Withdrawals disabled")
            self.header_add_travel_api.setGeometry(QtCore.QRect(-999, -999, 0, 0))

            #PLAIN LABEL - ADD TRAVEL API KEY
            self.label_add_account_travel_api = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_add_account_travel_api.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_add_account_travel_api.setObjectName("label_add_account_travel_api")
            self.label_add_account_travel_api.setText("Travel API Key")
            #DATA LABEL - ADD TRAVEL API KEY
            self.data_label_add_account_travel_api = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_add_account_travel_api.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_add_account_travel_api.setObjectName("data_label_add_account_travel_api")

            #PLAIN LABEL - ADD TRAVEL SEC KEY
            self.label_add_account_travel_sec = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_add_account_travel_sec.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_add_account_travel_sec.setObjectName("label_add_account_travel_sec")
            self.label_add_account_travel_sec.setText("Travel Secret Key")
            #DATA LABEL - ADD TRAVEL SEC KEY
            self.data_label_add_account_travel_sec = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_add_account_travel_sec.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_add_account_travel_sec.setObjectName("data_label_add_account_travel_sec")
            self.data_label_add_account_travel_sec.setEchoMode(QtWidgets.QLineEdit.Password)

            #ADD ACCOUNT BUTTON
            self.button_add_account = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_add_account.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_add_account.setObjectName("button_add_account")
            self.button_add_account.setText("Add Account")
            self.button_add_account.clicked.connect(self.create_Login_File_Man)


        def create_Dashboard_Group():
            self.tab_Dashboard = MainWidget('')
            self.master_Tabs_Container.addTab(self.tab_Dashboard ,'Dashboard')

            #HEADER - DASH TOTALS
            self.header_dash_totals = QtWidgets.QLabel(self.master_Tabs_Container)
            self.header_dash_totals.setFont(bold_font)
            self.header_dash_totals.setObjectName("header_dash_totals")
            self.header_dash_totals.setText("Accounts Summary")
            self.header_dash_totals.setGeometry(QtCore.QRect(-999, -999, 0, 0))

            #PLAIN LABEL - TOTAL BALANCES
            self.label_dash_balances_total = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_dash_balances_total.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_dash_balances_total.setObjectName("label_dash_balances_total")
            self.label_dash_balances_total.setText("All Balances Total ($)")

            #DATA LABEL - TOTAL BALANCES
            self.data_label_dash_balances_total = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_dash_balances_total.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_dash_balances_total.setObjectName("data_label_dash_balances_total")
            self.data_label_dash_balances_total.setEnabled(False)

            #PLAIN LABEL - TOTAL MARGINS
            self.label_dash_margins_total = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_dash_margins_total.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_dash_margins_total.setObjectName("label_dash_margins_total")
            self.label_dash_margins_total.setText("All Margins Total ($)")

            #DATA LABEL - TOTAL MARGINS
            self.data_label_dash_margins_total = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_dash_margins_total.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_dash_margins_total.setObjectName("data_label_dash_margins_total")
            self.data_label_dash_margins_total.setEnabled(False)

            #PLAIN LABEL - GLOBAL PNL
            self.label_dash_pnl_total = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_dash_pnl_total.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_dash_pnl_total.setObjectName("label_dash_pnl_total")
            self.label_dash_pnl_total.setText("All PNL Total ($)")
            
            #DATA LABEL - GLOBAL PNL
            self.data_label_dash_pnl_total = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_dash_pnl_total.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_dash_pnl_total.setObjectName("data_label_dash_pnl_total")
            self.data_label_dash_pnl_total.setEnabled(False)

            #HEADER - WIN LOSE
            self.header_dash_win_lose = QtWidgets.QLabel(self.master_Tabs_Container)
            self.header_dash_win_lose.setFont(bold_font)
            self.header_dash_win_lose.setObjectName("header_dash_win_lose")
            self.header_dash_win_lose.setText("Win/Lose Stats")
            self.header_dash_win_lose.setGeometry(QtCore.QRect(-999, -999, 0, 0))

            #BUTTON - CLEAR STATS
            self.button_clear_stats = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_clear_stats.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_clear_stats.setObjectName("button_clear_stats")
            self.button_clear_stats.setText("Clear")
            self.button_clear_stats.clicked.connect(self.clear_Stats)
            self.button_clear_stats.setToolTip("Resets all Win/Lose statistics.<br>")
            
            #PLAIN LABEL - DASHBOARD GLOBAL WINS AMOUNT
            self.label_dash_global_wins_amount = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_dash_global_wins_amount.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_dash_global_wins_amount.setObjectName("label_dash_global_wins_amount")
            self.label_dash_global_wins_amount.setText("Total Wins ($)")

            #DATA LABEL - DASHBOARD GLOBAL WINS AMOUNT
            self.data_label_dash_global_wins_amount = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_dash_global_wins_amount.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_dash_global_wins_amount.setObjectName("data_label_dash_global_wins_amount")
            self.data_label_dash_global_wins_amount.setEnabled(False)

            #PLAIN LABEL - DASHBOARD GLOBAL LOSSES AMOUNT
            self.label_dash_global_losses_amount = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_dash_global_losses_amount.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_dash_global_losses_amount.setObjectName("label_dash_global_losses_amount")
            self.label_dash_global_losses_amount.setText("Total Losses ($)")

            #DATA LABEL - DASHBOARD GLOBAL LOSSES AMOUNT
            self.data_label_dash_global_losses_amount = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_dash_global_losses_amount.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_dash_global_losses_amount.setObjectName("data_label_dash_global_losses_amount")
            self.data_label_dash_global_losses_amount.setEnabled(False)

            #PLAIN LABEL - DIFFERENCE
            self.label_dash_global_difference = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_dash_global_difference.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_dash_global_difference.setObjectName("label_dash_global_difference")
            self.label_dash_global_difference.setText("Difference ($)")

            #DATA LABEL - DIFFERENCE
            self.data_label_dash_global_difference = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_dash_global_difference.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_dash_global_difference.setObjectName("data_label_dash_global_difference")
            self.data_label_dash_global_difference.setEnabled(False)

            #PLAIN LABEL - RATIO
            self.label_dash_global_ratio = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_dash_global_ratio.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_dash_global_ratio.setObjectName("label_dash_global_ratio")
            self.label_dash_global_ratio.setText("Win/Lose Ratio ($)")
            #DATA LABEL - RATIO
            self.data_label_dash_global_ratio = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_dash_global_ratio.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_dash_global_ratio.setObjectName("data_label_dash_global_ratio")
            self.data_label_dash_global_ratio.setEnabled(False)

            #PLAIN LABEL - RATIO EVENT
            self.label_dash_global_ratio_event = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_dash_global_ratio_event.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_dash_global_ratio_event.setObjectName("label_dash_global_ratio_event")
            self.label_dash_global_ratio_event.setText("Win/Lose Event Ratio")
            #DATA LABEL - RATIO EVENT
            self.data_label_dash_global_ratio_event = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_dash_global_ratio_event.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_dash_global_ratio_event.setObjectName("data_label_dash_global_ratio_event")
            self.data_label_dash_global_ratio_event.setEnabled(False)

            self.header_global_auto = QtWidgets.QLabel(self.master_Tabs_Container)
            self.header_global_auto.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.header_global_auto.setFont(bold_font)
            self.header_global_auto.setObjectName("header_global_auto")
            self.header_global_auto.setText("Omicron")

            #BUTTON - START SERVER
            self.button_global_activate = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_global_activate.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_global_activate.setObjectName("button_global_activate")
            self.button_global_activate.setText("    Start Server")
            self.button_global_activate.setIcon(QtGui.QIcon('img/icon_start.png'))
            self.button_global_activate.setStyleSheet(self.create_style_left_align_text)

            self.button_global_activate.setFont(bold_font)
            self.button_global_activate.setCheckable(True)
            self.button_global_activate.clicked.connect(self.global_Activate)
            #
            self.button_global_activate.setToolTip("Start Omicron Server and therefore auto-trading across all accounts. Until you hit this button nothing will run.<br>")

            #BUTTON - POWERGRAPH
            self.button_global_chart = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_global_chart.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_global_chart.setObjectName("button_global_chart")
            self.button_global_chart.setText("    PowerGraph")
            self.button_global_chart.setIcon(QtGui.QIcon('img/icon_chart.png'))
            self.button_global_chart.setStyleSheet(self.create_style_left_align_text)
            self.button_global_chart.setCheckable(True)
            self.button_global_chart.clicked.connect(self.load_Power_Graph)
            self.button_global_chart.setToolTip("Load <b>PowerGraph</b> to see important visual data such as price candles, liquidation events, "\
                                                "large crypto transfers to exchanges and more.<br>")
            self.button_global_chart.setEnabled(False)

            #HEADER - GLOBAL SETTINGS
            self.header_global_settings = QtWidgets.QLabel(self.master_Tabs_Container)
            self.header_global_settings.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.header_global_settings.setFont(bold_font)
            self.header_global_settings.setObjectName("header_global_settings")
            self.header_global_settings.setText("Global Settings")

            #BUTTON - GLOBAL SPREAD
            self.button_global_spread = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_global_spread.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_global_spread.setObjectName("button_global_spread")
            self.button_global_spread.setText("  Price Spreading")
            self.button_global_spread.setCheckable(True)
            self.button_global_spread.setIcon(QtGui.QIcon('img/icon_spread.png'))
            self.button_global_spread.setStyleSheet(self.create_style_left_align_text)
            self.button_global_spread.clicked.connect(self.change_Global_Spread)
            self.button_global_spread.setToolTip("Price spreading ensures you don't enter into another Long or Short position with a very "\
                                                 "similar entry price.<br><br>It ensures your various positions are "\
                                                 "well spread out, increasing the chances of profiting more regularly, and reducing risk.<br>")
            #BUTTON - GLOBAL SPREAD SETTINGS
            self.button_global_spread_settings = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_global_spread_settings.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_global_spread_settings.setObjectName("button_global_spread_settings")
            self.button_global_spread_settings.setIcon(QtGui.QIcon(icon_settings))
            self.button_global_spread_settings.clicked.connect(self.popup_manager.popup_Spread_Settings)
            self.button_global_spread.setEnabled(False)
            self.button_global_spread_settings.setEnabled(False)

            #BUTTON - SLASHER
            self.button_slasher = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_slasher.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_slasher.setObjectName("button_protector")
            self.button_slasher.setText("  Slash Protection")
            self.button_slasher.setCheckable(True)
            self.button_slasher.setIcon(QtGui.QIcon('img/icon_slash.png'))
            self.button_slasher.setStyleSheet(self.create_style_left_align_text)
            self.button_slasher.clicked.connect(lambda:self.toggle_Button_File_Switch('txt/settings/liqs/liqs_protector.txt',self.button_slasher))
            self.button_slasher.setToolTip("Slash Protection is a second layer of security that will ensure your account does not get liquidated. When "\
                                             "your account margin dips below a certain ratio, x% of your positions will be automatically sold to nudge the "\
                                             "Liquidation threshold further away.<br>")
            self.button_slasher.setEnabled(False)

            #BUTTON - SLASHER / SETTINGS
            self.button_slasher_settings = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_slasher_settings.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_slasher_settings.setObjectName("button_protector_settings")
            self.button_slasher_settings.setIcon(QtGui.QIcon(icon_settings))
            self.button_slasher_settings.clicked.connect(self.popup_manager.popup_Guard_Settings)
            self.button_slasher_settings.setEnabled(False)

            #BUTTON - PADDING
            self.button_padding = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_padding.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_padding.setObjectName("button_padding")
            self.button_padding.setText("  Padding Protection")
            self.button_padding.setCheckable(True)
            self.button_padding.setIcon(QtGui.QIcon('img/icon_padding.png'))
            self.button_padding.setStyleSheet(self.create_style_left_align_text)
            self.button_padding.clicked.connect(lambda:self.toggle_Button_File_Switch('txt/settings/liqs/pad_protector.txt',self.button_padding))
            self.button_padding.setToolTip("Padding Protection is a second layer of security that will ensure your account does not get liquidated. When "\
                                             "your account margin dips below a certain ratio, funds will be transferred from other healthier accounts to top-up margin.<br>")

            #BUTTON - PADDING / SETTINGS
            self.button_padding_settings = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_padding_settings.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_padding_settings.setObjectName("button_padding_settings")
            self.button_padding_settings.setIcon(QtGui.QIcon(icon_settings))
            self.button_padding_settings.clicked.connect(self.popup_manager.popup_Pad_Settings)
            if self.accounts_count < 2:
                turn_off = self.txt_ops.quick_write_txt_file('txt/settings/liqs/pad_protector.txt',0)
                self.button_padding.setEnabled(False)
                self.button_padding_settings.setEnabled(False)


            #BUTTON - AUTO_MOVE
            self.button_auto_move = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_auto_move.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_auto_move.setObjectName("button_auto_move")
            self.button_auto_move.setText("  Auto Move Funds")
            self.button_auto_move.setCheckable(True)
            self.button_auto_move.setIcon(QtGui.QIcon('img/icon_transfer.png'))
            #set stylesheet
            self.button_auto_move.setStyleSheet(self.create_style_left_align_text)
            self.button_auto_move.setToolTip("Enable this if using Padding Protection. Automatically moves any USDT in the Spot Wallets to the Futures Wallets.<br>")
            self.button_auto_move.clicked.connect(lambda:self.toggle_Button_File_Switch('txt/settings/liqs/auto_move.txt',self.button_auto_move))




            #BUTTON - TRAVEL_MODE
            self.button_travel_mode = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_travel_mode.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_travel_mode.setObjectName("button_travel_mode")
            self.button_travel_mode.setText("  Travel Mode")
            self.button_travel_mode.setCheckable(True)
            self.button_travel_mode.setIcon(QtGui.QIcon('img/icon_boat.png'))
            #set stylesheet
            self.button_travel_mode.setStyleSheet(self.create_style_left_align_text)
            self.button_travel_mode.setToolTip("Binance requires an IP address to allow withdrawals. It is advised that you create a second API key pair, with withdrawals disabled, "\
                                               "which will allow you to trade from any IP address while travelling. This button switches between the two APIs.<br>")
            self.button_travel_mode.clicked.connect(lambda:self.toggle_Button_File_Switch('txt/settings/travel_mode.txt',self.button_travel_mode))

            #BUTTON - SKIM
            self.button_skim = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_skim.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_skim.setObjectName("button_skim")
            self.button_skim.setText("  Skim Mode")
            self.button_skim.setCheckable(True)
            self.button_skim.setIcon(QtGui.QIcon('img/icon_skim.png'))
            #set stylesheet
            self.button_skim.setStyleSheet(self.create_style_left_align_text)
            self.button_skim.setToolTip("Experimental - Binance will skim a small amount of USDT off 'Auto Move Funds' transfers, and send it to the Margin account for storage.<br>")
            self.button_skim.clicked.connect(lambda:self.toggle_Button_File_Switch('txt/settings/skim_mode.txt',self.button_skim))
            #BUTTON - SKIM / SETTINGS
            self.button_skim_settings = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_skim_settings.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_skim_settings.setObjectName("button_skim_settings")
            self.button_skim_settings.setIcon(QtGui.QIcon(icon_settings))
            self.button_skim_settings.clicked.connect(self.popup_manager.popup_Skim_Settings)
            
            #--------------------------------------------------------------
            # -------------- END DASHBOARD TABS -------------- #




        def create_Account_Group():


            self.create_Account_Tabs()

            #All text styles here:
            padding_left = '8'
            create_button_title_style_black = "color:black;text-align:left;padding-left:" + padding_left + "px;"
            create_button_title_style_green = "color:green;text-align:left;padding-left:" + padding_left + "px;"
            create_button_title_style_red = "color:red;text-align:left;padding-left:" + padding_left + "px;"

            #HEADER - FUTURES ACCOUNT
            self.header_futures_account = QtWidgets.QLabel(self.master_Tabs_Container)
            self.header_futures_account.setFont(bold_font)
            self.header_futures_account.setObjectName("header_futures_account")
            self.header_futures_account.setText("Futures Account")
            self.header_futures_account.setGeometry(QtCore.QRect(-999, -999, 0, 0))

            #Leverage
            self.lev_Slider = QtWidgets.QSlider(self.master_Tabs_Container)
            self.lev_Slider.setOrientation(QtCore.Qt.Horizontal)
            self.lev_Slider.setGeometry(30,40,600,30)
            self.lev_Slider.setRange(1,self.max_leverage_amount)
            self.lev_Slider.setPageStep(1)
            self.lev_Slider.setToolTip("Changes leverage amount between 1x and 15x.<br>")
            self.lev_Slider.valueChanged[int].connect(self.request_Change_Leverage_Value)
            self.data_label_lev = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_lev.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_lev.setObjectName("data_label_lev")
            self.data_label_lev.setEnabled(False)

            #BALANCE
            self.label_balance = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_balance.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_balance.setObjectName("label_balance")
            self.label_balance.setText("Account Balance")
            self.data_label_balance = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_balance.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_balance.setObjectName("data_label_balance")
            self.data_label_balance.setEnabled(False)
            self.data_label_balance.setFont(bold_font)

            #MARGIN
            self.label_margin = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_margin.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_margin.setObjectName("label_margin")
            self.label_margin.setText("Account Margin")
            self.label_margin.setToolTip("This is your available balance. It will increase or decrease "\
                                         "depending on your Profit and Loss when in a position.<br>")
            self.data_label_margin = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_margin.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_margin.setObjectName("data_label_margin")
            self.data_label_margin.setEnabled(False)
            self.data_label_margin.setToolTip("This is your available balance. It will increase or decrease "\
                                         "depending on your Profit and Loss when in a position.<br>")


            #PLAIN LABEL - PNL
            self.label_PNL = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_PNL.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_PNL.setObjectName("label_PNL")
            self.label_PNL.setText("Profit and Loss")
            self.label_PNL.setToolTip("Profit and Loss amounts for the entire account, and individual positions respectively.<br>")

            #DATA LABEL - PNL
            self.data_label_PNL = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_PNL.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_PNL.setObjectName("data_label_PNL")
            self.data_label_PNL.setEnabled(False)
            self.data_label_PNL.setToolTip("Profit and Loss amount for the entire account.<br>")


            #DATA LABEL - PNL
            self.data_label_PNL_pos = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_PNL_pos.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_PNL_pos.setObjectName("data_label_PNL_pos")
            self.data_label_PNL_pos.setEnabled(False)
            self.data_label_PNL_pos.setToolTip("Profit and Loss amount for the position selected from the dropdown below.<br>")

            #DATA LABEL - RISK RATIO
            self.data_label_risk_ratio = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_risk_ratio.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_risk_ratio.setObjectName("data_label_risk_ratio")
            self.data_label_risk_ratio.setEnabled(False)
            self.data_label_risk_ratio.setToolTip("Balance divided by margin. Used to assess the overall risk factor of an account.<br>")

            


            #HEADER - POSITIONS ( 1 of 1 )
            self.header_positions = QtWidgets.QLabel(self.master_Tabs_Container)
            self.header_positions.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.header_positions.setFont(bold_font)
            self.header_positions.setObjectName("header_positions")
            self.header_positions.setText("Positions")
            #
            self.header_positions.setToolTip("A list of Long and Short positions relating to this Account.<br>")



            #PLAIN LABEL - ENTRY ORDER
            self.label_entry_order = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_entry_order.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_entry_order.setObjectName("label_entry_order")
            self.label_entry_order.setText("Entry Order")
            self.label_entry_order.setToolTip("Orders that build a Position are displayed here.<br>")

            #DATA LABEL
            self.data_label_entry = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_entry.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_entry.setObjectName("data_label_entry")
            self.data_label_entry.setEnabled(False)
            self.data_label_entry.setToolTip("Orders that build a Position are displayed here.<br>")


            #PLAIN LABEL - POSITIONS
            self.label_positions = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_positions.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_positions.setObjectName("label_positions")
            self.label_positions.setText("Open Positions")
            self.label_positions.setToolTip("A list of Long and Short positions relating to this Account.<br>")
            #COMBO DATA - POSITIONS
            #positions_list = ['First Position','Second Position','Third Position']

            self.combo_positions = QtWidgets.QComboBox(self.master_Tabs_Container)
            self.combo_positions.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.combo_positions.setObjectName("combo_positions")
            self.combo_positions.currentTextChanged.connect(self.on_Combo_Positions_Changed)


            #SPINBOX
            self.spinbox_slash = QtWidgets.QSpinBox(self.master_Tabs_Container)
            self.spinbox_slash.setFixedSize(36, 18)
            self.spinbox_slash.setRange(1,99)
            self.spinbox_slash.setSingleStep(1)
            self.spinbox_slash.valueChanged[int].connect(self.request_Change_Slash_Value)

            

            #BUTTON - INCREASE
            self.button_increase_position = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_increase_position.setObjectName("button_increase_position")
            self.button_increase_position.setText("+")
            self.button_increase_position.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_increase_position.clicked.connect(lambda:self.adjust_Position('increase'))
            #
            self.button_increase_position.setToolTip("Increases the amount of your current position by x%, defined left.<br>")


            #BUTTON - DECREASE
            self.button_decrease_position = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_decrease_position.setObjectName("button_decrease_position")
            self.button_decrease_position.setText("-")
            self.button_decrease_position.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_decrease_position.clicked.connect(lambda:self.adjust_Position('decrease'))
            #
            self.button_decrease_position.setToolTip("Reduces the amount of your current position by x%, defined left.<br>")
            # END COMBO DATA ### - POSITIONS



            
            #PLAIN LABEL - TP ORDER
            self.label_order_tp = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_order_tp.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_order_tp.setObjectName("label_order_tp")
            self.label_order_tp.setText("Take Profit Order")

            #PLAIN LABEL - SL ORDER
            self.label_order_sl = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_order_sl.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_order_sl.setObjectName("label_order_sl")
            self.label_order_sl.setText("Stop Loss Order")




            #PLAIN LABEL - LIQUIDATION PRICE
            self.label_liq_price = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_liq_price.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_liq_price.setObjectName("label_liq_price")
            self.label_liq_price.setText("Liq/Current Price")
            #
            self.label_liq_price.setToolTip("This is the price at which you will lose your entire <b>Account Balance</b>."\
                                            " Manage your leverage accordingly.<br>")
            #DATA LABEL - LIQUIDATION PRICE
            self.data_label_liq_price = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_liq_price.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_liq_price.setObjectName("data_label_liq_price")
            self.data_label_liq_price.setEnabled(False)
            #color styles
            create_style_string_red = "color:" + ("red") + ";"
            self.data_label_liq_price.setStyleSheet(create_style_string_red)
            #
            self.data_label_liq_price.setToolTip("This is the price at which you will lose your entire <b>Account Balance</b>."\
                                            " Manage your leverage accordingly.<br>")


            #DATA LABEL - CURRENT PRICE
            self.data_label_current_price = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_current_price.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_current_price.setObjectName("data_label_current_price")
            self.data_label_current_price.setEnabled(False)
            #color styles
            create_style_string_green = "color:" + ("green") + ";"
            self.data_label_current_price.setStyleSheet(create_style_string_green)
            
            #
            self.data_label_current_price.setToolTip("The current average Futures price of the symbol.<br>")

            #DATA LABEL - TO GO
            self.data_label_liq_progress = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_liq_progress.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_liq_progress.setObjectName("data_label_liq_progress")
            self.data_label_liq_progress.setEnabled(False)

            #color styles
            create_style_string_green = "color:" + ("green") + ";"
            self.data_label_liq_progress.setStyleSheet(create_style_string_green)
            self.data_label_liq_progress.setToolTip("To liquidation price (100% will result in your account being liquidated!)<br>")
            #




            #HEADER - ATTACHED ORDERS
            self.header_linked_orders = QtWidgets.QLabel(self.master_Tabs_Container)
            self.header_linked_orders.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.header_linked_orders.setFont(bold_font)
            self.header_linked_orders.setObjectName("header_attached_orders")
            self.header_linked_orders.setText("Linked Orders")



            #DATA LABELS - TP AND SL ORDERS
            self.data_label_order_tp = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_order_tp.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_order_tp.setObjectName("data_label_order_tp")
            self.data_label_order_tp.setEnabled(False)

            self.data_label_order_sl = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_order_sl.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_order_sl.setObjectName("data_label_order_sl")        
            self.data_label_order_sl.setEnabled(False)



            #BUTTON - CANCEL ALL LINKED
            self.button_cancel_open_orders = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_cancel_open_orders.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_cancel_open_orders.setObjectName("button_cancel_open_orders")
            self.button_cancel_open_orders.setText("Cancel Linked")
            self.button_cancel_open_orders.clicked.connect(lambda:self.cancel_All_Method(1))
            #
            self.button_cancel_open_orders.setToolTip("Cancels all open orders for the selected symbol in the dropdown above.<br>")


            #BUTTON - CANCEL ALL
            self.button_cancel_all_open_orders = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_cancel_all_open_orders.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_cancel_all_open_orders.setObjectName("button_cancel_all_open_orders")
            self.button_cancel_all_open_orders.setText("Cancel All")
            self.button_cancel_all_open_orders.clicked.connect(lambda:self.cancel_All_Method(2))
            #
            self.button_cancel_all_open_orders.setToolTip("Cancels all open orders for the account, regardless of pair symbol.<br>")



            #BUTTON - REBUILD
            self.button_rebuild = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_rebuild.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_rebuild.setObjectName("button_rebuild")
            self.button_rebuild.setText("Build TP/SL")
            self.button_rebuild.clicked.connect(self.rebuild_Method)
            #
            self.button_rebuild.setToolTip("Builds Take Profit and Stop Loss orders for the open Position,"
                                           " using the <b>Trade Settings</b> values defined to the right. Currently open orders will be cancelled.<br>")


            #BUTTON - REFRESH POS
            self.button_refresh_pos = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_refresh_pos.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_refresh_pos.setObjectName("button_refresh_pos")
            #self.button_refresh_pos.setText("Refresh")
            self.button_refresh_pos.setIcon(QtGui.QIcon('img/icon_refresh.png'))
            self.button_refresh_pos.clicked.connect(self.update_Pos_Combo)
            #
            self.button_refresh_pos.setToolTip("Refresh the positions list.<br>")


            #BUTTON - USE SUPPORT/RES SETTINGS
            self.button_rebuild_cog = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_rebuild_cog.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_rebuild_cog.setObjectName("button_rebuild_cog")
            self.button_rebuild_cog.setIcon(QtGui.QIcon(icon_settings))
            self.button_rebuild_cog.clicked.connect(self.popup_manager.popup_Rebuild_Settings)
            #
            self.button_rebuild_cog.setToolTip("Define your Take Profit and Stop Loss amounts; FULL (100%), HALF (50%) or NONE (Will not create an order). "\
                                               "This setting is local to each pair symbol, defined under Trade Settings to the right.<br>")





            #BUTTON - FORCE CLOSE
            self.button_force_close = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_force_close.setObjectName("button_force_close")
            self.button_force_close.setText("Force Close")
            self.button_force_close.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_force_close.clicked.connect(self.force_Close_Method)
            #
            self.button_force_close.setToolTip("Closes the open Position immediately at Market price. You will profit or lose depending "\
                                               "on your <b>Profit and Loss</b> value above at that moment.<br>")




            #HEADER - TRADE SETTINGS
            self.header_trade_settings = QtWidgets.QLabel(self.master_Tabs_Container)
            self.header_trade_settings.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.header_trade_settings.setFont(bold_font)
            self.header_trade_settings.setObjectName("header_trade_settings")
            self.header_trade_settings.setText("Trade Settings")

           

            #PLAIN LABEL - MAX POS
            self.label_leverage = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_leverage.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_leverage.setObjectName("label_leverage")
            self.label_leverage.setText("Leverage")
            #
            self.label_leverage.setToolTip("The leverage setting for the symbol below, use with care. "\
                                          "A leverage of 5x means a 20% swing in the wrong direction could liquidate your account.<br>")



            #line ------------------------------------------
            self.line = QtWidgets.QFrame(self.master_Tabs_Container)
            self.line.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.line.setFrameShape(QtWidgets.QFrame.HLine)
            self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line.setObjectName("line")
            
            #PLAIN LABEL - POST BIDS
            self.label_order_type = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_order_type.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_order_type.setObjectName("label_order_type")
            self.label_order_type.setText("Order Type")
            self.label_order_type.setToolTip("Market orders execute instantly. Limit orders require that you define a <b>Bid</b>.<br><br>"\
                                          "If using Fragments, the Entry Bid is how much above/below the market price you wish to purchase the first segment. "\
                                          "Post Bids define the segments that come after.<br>")


            #PLAIN LABEL - FRAGMENTS
            self.label_fragments = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_fragments.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_fragments.setObjectName("label_fragments")
            self.label_fragments.setText("Fragments")
            self.label_fragments.setToolTip("A powerful function that allows you to enter into a position in smaller segments, over a defined period of time.<br><br>"\
                                            "In example, if Time Range is set to 240 seconds, and the Fragments to 4, Omicron will buy 1 unit, every 60 seconds, "\
                                            "until it reaches 4 units.<br>")
                                       



            #PLAIN LABEL - TIME RANGE
            self.label_time_range = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_time_range.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_time_range.setObjectName("label_time_range")
            self.label_time_range.setText("Time Range (s)")
            self.label_time_range.setToolTip("Defines over how many seconds all Fragments should be purchased.<br>")





            #PLAIN LABEL - ENTRY BIDS
            self.label_entry_bid = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_entry_bid.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_entry_bid.setObjectName("label_entry_bid")
            self.label_entry_bid.setText("Entry Bid ($)")
            self.label_entry_bid.setToolTip("How much above/below the market price to purchase the first fragment of a position.<br><br>"\
                                            "In example, a user who wishes to go Long while the market price of an asset is $200, may set the bid to $1 to enter at $199 instead.<br>")


            self.data_label_entry_bid = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_entry_bid.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_entry_bid.setObjectName("data_label_entry_bid")
            self.data_label_entry_bid.setToolTip("How much above/below the market price to purchase the first fragment of a position.<br><br>"\
                                            "In example, a user who wishes to go Long while the market price of an asset is $200, may set the bid to $1 to enter at $199 instead.<br>")



            #PLAIN LABEL - POST BIDS
            self.label_post_bids = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_post_bids.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_post_bids.setObjectName("label_post_bids")
            self.label_post_bids.setText("Post Bids ($)")
            #
            self.label_post_bids.setToolTip("Same as above but to define a bid for the fragments after the initial first one.<br>")

            self.data_label_post_bids = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_post_bids.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_post_bids.setObjectName("data_label_post_bids")
            #
            self.data_label_post_bids.setToolTip("Same as above but to define a bid for the fragments after the initial first one.<br>")





            #PLAIN LABEL - SL 
            self.label_sl_setting = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_sl_setting.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_sl_setting.setObjectName("label_sl_setting")
            self.label_sl_setting.setText("Stop Loss ($)")


            #PAIR SYMBOL COMBO
            pairs_array = ['BTCUSDT','ETHUSDT','ADAUSDT','LTCUSDT','BNBUSDT']
            self.label_pair_symbol = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_pair_symbol.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_pair_symbol.setObjectName("label_pair_symbol")
            self.label_pair_symbol.setText("Pair Symbol")
            self.combo_symbols = QtWidgets.QComboBox(self.master_Tabs_Container)
            self.combo_symbols.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.combo_symbols.setObjectName("combo_symbols")
            self.combo_symbols.addItems(pairs_array)
            self.combo_symbols.currentTextChanged.connect(self.on_Combo_Symbols_Changed)


            #TP
            self.label_tp_setting = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_tp_setting.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_tp_setting.setObjectName("label_tp_setting")
            self.label_tp_setting.setText("Take Profit ($)")

            
            #AMOUNT
            self.label_amount_to_trade = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_amount_to_trade.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_amount_to_trade.setObjectName("label_amount_to_trade")
            self.label_amount_to_trade.setText("Amount")
            self.label_amount_to_trade.setToolTip("The maximum amount of the crypto asset you would like to trade.<br>")
            self.button_1x = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_1x.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_1x.setObjectName("button_1x")
            self.button_1x.setText("Max")
            self.button_1x.clicked.connect(self.calc_1x)
            self.button_1x.setToolTip("Omicron will attempt to calculate the max amount you can afford.<br>")



            #PLAIN LABEL - LIMIT ORDER
            self.button_limit = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_limit.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_limit.setObjectName("button_limit")
            self.button_limit.setText("Limit")
            self.button_limit.setCheckable(True)
            self.button_limit.toggle()
            

            
            self.button_limit.clicked.connect(self.use_Limit_Order)

            #PLAIN LABEL - MARKET ORDER
            self.button_market = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_market.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_market.setObjectName("button_market")
            self.button_market.setText("Market")
            self.button_market.setCheckable(True)
            self.button_market.clicked.connect(self.use_Market_Order)



            #PLAIN LABEL - APPLY
            self.button_apply = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_apply.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_apply.setObjectName("button_apply")
            self.button_apply.setText("Apply Settings")
            #self.button_apply.setCheckable(True) 
            self.button_apply.clicked.connect(self.apply_Trade_Settings)

            self.data_label_amount = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_amount.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_amount.setObjectName("data_label_amount")

            self.data_label_fragments = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_fragments.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_fragments.setObjectName("data_label_entry_order")

            self.data_label_time_range = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_time_range.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_time_range.setObjectName("data_label_time_range")


            #TP SETTINGS
            self.data_label_tp_setting = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_tp_setting.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_tp_setting.setObjectName("data_label_tp_setting")

            #BUTTON - TP SETTINGS
            self.dynamic_tp = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.dynamic_tp.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.dynamic_tp.setObjectName("dynamic_tp")
            self.dynamic_tp.setText("Dynamic TP")
            self.dynamic_tp.setCheckable(True)
            self.dynamic_tp.clicked.connect(self.use_Dynamic_TP)
            #
            self.dynamic_tp.setToolTip("Instead of defining a fixed <b>Take Profit (TP)</b> amount, you can let Omicron recommend one. This "\
                                              "setting will set your TP at the Gold line, IF it is higher than your fixed TP setting.<br>")
            #self.dynamic_tp.setEnabled(False)



            

            self.data_label_sl_setting = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_sl_setting.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_sl_setting.setObjectName("data_label_sl_setting")

            #BUTTON - SL SETTINGS
            self.dynamic_sl = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.dynamic_sl.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.dynamic_sl.setObjectName("dynamic_sl")
            self.dynamic_sl.setText("Dynamic SL")
            self.dynamic_sl.setCheckable(True)
            self.dynamic_sl.clicked.connect(self.use_Dynamic_SL)
            #
            self.dynamic_sl.setToolTip("An experimental feature that is currently not recommended. Stop Loss is dynamically set "\
                                              "a little below the Gold line, as it signifies a small 'trend broken' signal.<br>")
            self.dynamic_sl.setEnabled(False)

            self.button_sl_liq_setting = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_sl_liq_setting.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_sl_liq_setting.setObjectName("button_sl_liq_setting")
            self.button_sl_liq_setting.setText("Liq. Price")
            self.button_sl_liq_setting.setCheckable(True)
            self.button_sl_liq_setting.clicked.connect(self.use_Liq_SL)
            #
            self.button_sl_liq_setting.setToolTip("With this option selected, Omicron will set your Stop Loss just before the liquidation price.<br>")


            #BUTTON - USE SUPPORT/RES SETTINGS
            self.button_sl_liq_setting_cog = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_sl_liq_setting_cog.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_sl_liq_setting_cog.setObjectName("button_sl_liq_setting_cog")
            #self.button_use_sup_res_settings.setText("")
            self.button_sl_liq_setting_cog.setIcon(QtGui.QIcon(icon_settings))
            self.button_sl_liq_setting_cog.clicked.connect(self.popup_manager.popup_Liq_SL_Settings)








            #######################################################################################################################

            #HEADER - ALLOW AUTO
            self.header_automation = QtWidgets.QLabel(self.master_Tabs_Container)
            self.header_automation.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.header_automation.setFont(bold_font)
            self.header_automation.setObjectName("header_automation")
            self.header_automation.setText("Automation")
            #ALLOW AUTO
            self.button_allow_auto = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_allow_auto.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_allow_auto.setFont(bold_font)
            self.button_allow_auto.setObjectName("button_allow_auto")
            self.button_allow_auto.setText("    Allow Auto")
            self.button_allow_auto.setStyleSheet(create_button_title_style_black)
            self.button_allow_auto.setIcon(QtGui.QIcon('img/icon_robot.png'))
            self.button_allow_auto.setCheckable(True)
            self.button_allow_auto.clicked.connect(self.allow_Auto_Method)
            #
            self.button_allow_auto.setToolTip("With this selected, Omicron will automatically search for good entry signals, using the Algorithm Builder settings below.<br><br>"\
                                              "If unselected, Omicron will not use this particular account for auto-trading, however, you can "\
                                              "still use the Manual Override options situated in the bottom right corner.<br>")
            #ALLOW AUTO SETTINGS
            self.button_auto_settings = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_auto_settings.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_auto_settings.setObjectName("button_auto_settings")
            self.button_auto_settings.setIcon(QtGui.QIcon(icon_settings))
            self.button_auto_settings.clicked.connect(self.popup_manager.popup_Allow_Auto)
            self.button_auto_settings.setToolTip("Here you can choose precisely which coins are allowed to auto-trade.<br>")

            #MAINTAIN BALANCE
            self.button_maintain_balance = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_maintain_balance.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_maintain_balance.setObjectName("button_maintain_balance")
            self.button_maintain_balance.setText("  Maintain Balance")
            self.button_maintain_balance.setStyleSheet(create_button_title_style_black)
            self.button_maintain_balance.setCheckable(True)
            self.button_maintain_balance.clicked.connect(self.use_Round_Method)
            self.button_maintain_balance.setToolTip("Account global setting. Omicron will attempt to create an equal number of Long and Short positions within the Account, "\
                                                "i.e. if max positions is 4, it will try and maintain a balance of 2 Long and 2 Short positions.<br>")
            self.button_maintain_balance.setIcon(QtGui.QIcon('img/icon_balance.png'))
            #######################################################################################################################


            #HEADER - ALGORITHM BUILDER
            self.header_algorithm_builder = QtWidgets.QLabel(self.master_Tabs_Container)
            self.header_algorithm_builder.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.header_algorithm_builder.setFont(bold_font)
            self.header_algorithm_builder.setObjectName("header_algorithm_builder")
            self.header_algorithm_builder.setText("Algorithm Builder")
            #
            self.header_algorithm_builder.setToolTip("Build your own awesome multi-condition algorithms for entry! Settings apply individually per coin.<br>")


            #ALLOW LONGS
            self.button_allow_longs = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_allow_longs.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_allow_longs.setObjectName("button_allow_longs")
            self.button_allow_longs.setText("  Allow Longs")
            self.button_allow_longs.setCheckable(True)
            self.button_allow_longs.clicked.connect(self.allow_Auto_Longs_Method)
            self.button_allow_longs.setIcon(QtGui.QIcon('img/icon_up.png'))
            self.button_allow_longs.setStyleSheet(create_button_title_style_green)
            self.button_allow_longs.setFont(bold_font)
            self.button_allow_longs.setToolTip("With this selected, Omicron will be allowed to enter Long positions for this particular pair symbol, "\
                                               "defined left in Trade Settings.<br>")

            #BUTTON - ALLOW SHORTS
            self.button_allow_shorts = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_allow_shorts.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_allow_shorts.setObjectName("button_allow_shorts")
            self.button_allow_shorts.setIcon(QtGui.QIcon('img/icon_down.png'))
            self.button_allow_shorts.setText("  Allow Shorts")
            self.button_allow_shorts.setCheckable(True)
            self.button_allow_shorts.clicked.connect(self.allow_Auto_Shorts_Method)
            self.button_allow_shorts.setToolTip("With this selected, Omicron will be allowed to enter Short positions for this particular pair symbol, "\
                                               "defined left in Trade Settings.<br>")
            self.button_allow_shorts.setStyleSheet(create_button_title_style_red)
            self.button_allow_shorts.setFont(bold_font)



            #BUTTON - USE SUPPORT/RES
            self.button_use_sup_res = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_use_sup_res.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_use_sup_res.setObjectName("button_use_sup_res")
            self.button_use_sup_res.setText("  Use Gold/Silver")
            self.button_use_sup_res.setIcon(QtGui.QIcon('img/icon_gold.png'))
            #stylesheet
            self.button_use_sup_res.setStyleSheet(self.create_style_left_align_text)

            self.button_use_sup_res.setCheckable(True)
            self.button_use_sup_res.clicked.connect(self.use_Sup_Res_Method)
            #
            self.button_use_sup_res.setToolTip("Enter based on a combination of the Price Mode Average and the Fibonacci Retracement Levels.<br><br>"\
                                               "Omicron calculates the PMA, and then picks the closest Fib next to it, "\
                                               "to create <b>Gold</b> and <b>Silver</b> regions that have even more relevance than standard Fibs. "\
                                               "If the current price dips below these regions, Longs are recommended, and vice versa for Shorts.<br>")
            #self.button_use_sup_res.setToolTipDuration(5000)
            #self.button_use_sup_res.CloseOnPressOutsideParent(True)


            #BUTTON - USE SUPPORT/RES SETTINGS
            self.button_use_sup_res_settings = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_use_sup_res_settings.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_use_sup_res_settings.setObjectName("button_use_sup_res_settings")
            #self.button_use_sup_res_settings.setText("")
            self.button_use_sup_res_settings.setIcon(QtGui.QIcon(icon_settings))
            self.button_use_sup_res_settings.clicked.connect(self.popup_manager.popup_Sup_Res_Settings)
            








            #BUTTON - USE LIQ EVENTS
            self.button_use_avoid = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_use_avoid.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_use_avoid.setObjectName("button_use_liq_events")
            self.button_use_avoid.setText("  Avoid Regions")
            self.button_use_avoid.setCheckable(True)
            self.button_use_avoid.setIcon(QtGui.QIcon('img/icon_avoid.png'))
            #stylesheet
            self.button_use_avoid.setStyleSheet(self.create_style_left_align_text)

            self.button_use_avoid.clicked.connect(self.use_Liq_Events_Method)
            #
            self.button_use_avoid.setToolTip("You can manually define a 'box zone' where Long and Short entries"\
                                                  " are not allowed if the current price is outside of it.<br>")
            #BUTTON - USE LIQ EVENTS SETTINGS
            self.button_use_avoid_settings = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_use_avoid_settings.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_use_avoid_settings.setObjectName("button_liq_events_settings")

            #Settings ICON
            self.button_use_avoid_settings.setIcon(QtGui.QIcon(icon_settings))
            self.button_use_avoid_settings.clicked.connect(self.popup_manager.popup_Avoid_Settings)

            #self.button_use_avoid.setEnabled(False)






            #BUTTON - USE EMAIL 5M
            self.button_use_email_5m = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_use_email_5m.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_use_email_5m.setObjectName("button_use_email_5m")
            self.button_use_email_5m.setText("  Use Email 3m")
            self.button_use_email_5m.setCheckable(True)
            self.button_use_email_5m.setIcon(QtGui.QIcon('img/icon_email.png'))

            self.button_use_email_5m.setStyleSheet(self.create_style_left_align_text)

            self.button_use_email_5m.clicked.connect(self.use_Email_5m_Method)
            #self.button_use_email_5m.setEnabled(False)
            #
            self.button_use_email_5m.setToolTip("Omicron can read the title of an email which allows you to use custom 3 minute signals,  i.e. "\
                                                "'MACD BTCUSDT 3m LONG' or 'RSI BNBUSDT 3m SHORT'. Omicron provides these signals by default, if no custom server is defined.<br>")
            #BUTTON - USE EMAIL 5M SETTINGS
            self.button_use_email_5m_settings = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_use_email_5m_settings.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_use_email_5m_settings.setObjectName("button_use_email_5m_settings")
            #Settings ICON
            self.button_use_email_5m_settings.setIcon(QtGui.QIcon(icon_settings))
            self.button_use_email_5m_settings.clicked.connect(self.popup_manager.popup_Email_Settings)




            #BUTTON - USE EMAIL 4h
            self.button_use_email_4h = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_use_email_4h.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_use_email_4h.setObjectName("button_use_email_4h")
            self.button_use_email_4h.setText("  Use Email 4h")
            self.button_use_email_4h.setCheckable(True)
            self.button_use_email_4h.setIcon(QtGui.QIcon('img/icon_email.png'))
            self.button_use_email_4h.setStyleSheet(self.create_style_left_align_text)
            self.button_use_email_4h.clicked.connect(self.use_Email_4h_Method)
            #self.button_use_email_4h.setEnabled(False)
            #
            self.button_use_email_4h.setToolTip("Omicron can read the title of an email which allows you to use custom 4 hour signals,  i.e. "\
                                                "'RSI BTCUSDT 4h LONG' or 'MACD LTCUSDT 4h SHORT'. Omicron provides these signals by default, if no custom server is defined.<br>")
            #BUTTON - USE EMAIL 4h SETTINGS
            self.button_use_email_4h_settings = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_use_email_4h_settings.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_use_email_4h_settings.setObjectName("button_use_email_4h_settings")
            #Settings ICON
            self.button_use_email_4h_settings.setIcon(QtGui.QIcon(icon_settings))
            self.button_use_email_4h_settings.clicked.connect(self.popup_manager.popup_Email_Settings)











            #BUTTON - USE BARTS
            self.button_use_barts = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_use_barts.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_use_barts.setObjectName("button_use_barts")
            self.button_use_barts.setText("  Use Bart Patterns")
            self.button_use_barts.setCheckable(True)
            self.button_use_barts.setEnabled(False)
            self.button_use_barts.clicked.connect(self.use_Barts_Method)
            self.button_use_barts.setStyleSheet(self.create_style_left_align_text)
            self.button_use_barts.setIcon(QtGui.QIcon('img/icon_bart.png'))

            #BUTTON - USE TURAN
            self.button_use_turan = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_use_turan.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_use_turan.setObjectName("button_use_turan")
            self.button_use_turan.setText("  Use T.U.R.A.N.")
            self.button_use_turan.setCheckable(False)
            self.button_use_turan.setEnabled(False)
            self.button_use_turan.clicked.connect(self.use_Turan_Method)
            self.button_use_turan.setStyleSheet(self.create_style_left_align_text)
            self.button_use_turan.setIcon(QtGui.QIcon('img/icon_brain.png'))


            #HEADER - MANUAL
            self.header_manual = QtWidgets.QLabel(self.master_Tabs_Container)
            self.header_manual.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.header_manual.setFont(bold_font)
            self.header_manual.setObjectName("header_manual")
            self.header_manual.setText("Manual Override")
            #
            self.button_manual_long = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_manual_long.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_manual_long.setObjectName("button_manual_long")
            self.button_manual_long.setText(" Go Manual Long")
            self.button_manual_long.clicked.connect(self.go_Manual_Long)
            #self.button_manual_long.setFont(bold_font)


            self.button_manual_long.setIcon(QtGui.QIcon('img/icon_up.png'))
            self.button_manual_long.setStyleSheet(create_button_title_style_green)
            #
            self.button_manual_short = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_manual_short.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_manual_short.setObjectName("button_manual_short")
            self.button_manual_short.setText(" Go Manual Short")
            self.button_manual_short.clicked.connect(self.go_Manual_Short)

            self.button_manual_short.setIcon(QtGui.QIcon('img/icon_down.png'))
            self.button_manual_short.setStyleSheet(create_button_title_style_red)
            #self.button_manual_short.setFont(bold_font)

            ###########################################################################################################



            #WITHDRAW
            self.header_spot_account = QtWidgets.QLabel(self.master_Tabs_Container)
            self.header_spot_account.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.header_spot_account.setFont(bold_font)
            self.header_spot_account.setObjectName("header_spot_account")
            self.header_spot_account.setText("Main Gateway Account")

            

            self.label_spot_usdt_balance = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_spot_usdt_balance.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_spot_usdt_balance.setObjectName("label_spot_usdt_balance")
            self.label_spot_usdt_balance.setText("USDT Balance")

            self.data_label_spot_usdt_balance = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_spot_usdt_balance.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_spot_usdt_balance.setObjectName("data_label_spot_usdt_balance")
            self.data_label_spot_usdt_balance.setEnabled(False)
            

            #TRANSFER AMOUNT
            self.label_transfer_amount = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_transfer_amount.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_transfer_amount.setObjectName("label_transfer_amount")
            self.label_transfer_amount.setText("Transfer Amount")

            self.data_label_transfer_amount = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_transfer_amount.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_transfer_amount.setObjectName("data_label_transfer_amount")
            self.data_label_transfer_amount.setText("0.00")




            #TO ADDRESS
            self.label_to_address = QtWidgets.QLabel(self.master_Tabs_Container)
            self.label_to_address.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.label_to_address.setObjectName("label_to_address")
            self.label_to_address.setText("To Address")

            self.data_label_to_address = QtWidgets.QLineEdit(self.master_Tabs_Container)
            self.data_label_to_address.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.data_label_to_address.setObjectName("data_label_to_address")
            self.data_label_to_address.setText(self.current_offline_address)
            self.data_label_to_address.setEnabled(False)
            



            self.button_spot_fut = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_spot_fut.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_spot_fut.setObjectName("button_spot_fut")
            self.button_spot_fut.setText("Spot » Fut")
            self.button_spot_fut.clicked.connect(lambda:self.spot_Fut_Transfer(0))
            #
            self.button_spot_fut.setToolTip("Transfer funds from your Main Wallet to your Futures Wallet.<br>")  

            self.button_fut_spot = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_fut_spot.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_fut_spot.setObjectName("button_fut_spot")
            self.button_fut_spot.setText("Fut » Spot")
            self.button_fut_spot.clicked.connect(self.fut_Spot_Transfer)
            #
            self.button_fut_spot.setToolTip("Transfer funds from your Futures Wallet to your Main Wallet.<br>")  

            self.button_inject_account = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_inject_account.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_inject_account.setObjectName("button_inject_account")
            self.button_inject_account.setText("Inject")
            self.button_inject_account.clicked.connect(self.inject_Account)
            #
            self.button_inject_account.setToolTip("Quickly transfer funds to this account from another account that has enough margin. Good for emergency top-ups.<br>")
            if self.accounts_count < 2:
                self.button_inject_account.setEnabled(False)

            self.button_withdraw = QtWidgets.QPushButton(self.master_Tabs_Container)
            self.button_withdraw.setGeometry(QtCore.QRect(-999, -999, 0, 0))
            self.button_withdraw.setObjectName("button_withdraw")
            self.button_withdraw.setText("Withdraw")
            self.button_withdraw.clicked.connect(self.popup_Withdraw)
            #
            self.button_withdraw.setToolTip("Withdraw funds to an address of your choice (tag optional).<br><br>Will automatically convert USDT to a crypto of your choosing.<br>")



        #Build UI (normal/first run)
        if self.first_run == False:
            print("\nLoading UI...")
            #build_Menu()
            create_Dashboard_Group()
            create_Account_Group()
            create_Plus_Group()
        else:
            print("\nPreparing for first run...")
            a = Admin()
            delete_previous = a.clear_Configs()
            #build_Menu()
            create_Plus_Group()


        #TAB CHANGE EVENT ATTACH - create a Tab Button click event connector
        self.master_Tabs_Container.currentChanged.connect(self.on_Tab_Change)
        self.master_Tabs_Container.tabBar().currentChanged.connect(self.style_Tabs)


        #---STATUS BAR---
        self.statusBar = QStatusBar()
        #create download button
        self.download_new = QtWidgets.QPushButton("Download new version")
        self.download_new.setVisible(False)
        self.download_new.clicked.connect(self.download_New_Version)
        create_style_string = "color:black;"
        self.download_new.setStyleSheet(create_style_string)
        self.statusBar.addPermanentWidget(self.download_new)
        #---END STATUS BAR---

        #construct all
        box_layout = QVBoxLayout()        
        #box_layout.addWidget(self.bar)#used for menu bar top
        box_layout.addWidget(self.master_Tabs_Container)
        box_layout.addWidget(self.statusBar)
        self.setLayout(box_layout)




########################



    def create_Account_Tabs(self):
        for i in range(len(self.accounts_list)):
            self.tab_Widget = MainWidget('')
            account_number = int(self.accounts_list[i])
            self.master_Tabs_Container.addTab(self.tab_Widget,"Account {}".format(account_number))



    def style_Tabs(self,index):
        
        light_grey = '#dadada'
        light_green = '#2de75f'
        light_yellow = '#ffffff'
        light_red = '#ff8d63'
        selected_color = light_yellow

        self.tabColors = {
            0: selected_color, 
            1: selected_color, 
            2: selected_color, 
            3: selected_color, 
            4: selected_color,
            5: selected_color,
            6: selected_color,
            7: selected_color,
            8: selected_color,
            9: selected_color,
            10: selected_color,
            11: selected_color,
            12: selected_color,
            13: selected_color,
            14: selected_color,
            15: selected_color,
            16: selected_color,
            17: selected_color
            }

        self.untabColors = {
            0: light_grey, 
            1: light_grey, 
            2: light_grey, 
            3: light_grey, 
            4: light_grey,
            5: light_grey,
            6: light_grey,
            7: light_grey,
            8: light_grey,
            9: light_grey,
            10: light_grey,
            11: light_grey,
            12: light_grey,
            13: light_grey,
            14: light_grey,
            15: light_grey,
            16: light_grey,
            17: light_grey
            }

        self.master_Tabs_Container.setStyleSheet('''
            QTabBar::tab {{}}
            QTabBar::tab:selected {{background-color: {color};}}
            '''.format(color=self.tabColors[index]))




        




#### END UI CREATION ########################################################################################################################

######## UI CONFIG ################################################################################################################

    def hide_Accounts_UI(self):

        hide_list = [self.header_futures_account,\
                     self.lev_Slider,\
                     self.header_trade_settings,\
                     self.header_algorithm_builder,\
                     self.header_manual,\
                     self.header_positions,\
                     self.header_linked_orders,\
                     self.header_automation,\
                     self.combo_positions,\
                     self.button_increase_position,\
                     self.button_decrease_position,\
                     self.data_label_lev,\
                     self.label_PNL,\
                     self.label_margin,\
                     self.label_balance,\
                     self.label_post_bids,\
                     self.label_time_range,\
                     self.label_fragments,\
                     self.label_entry_bid,\
                     self.label_sl_setting,\
                     self.label_pair_symbol,\
                     self.label_tp_setting,\
                     self.label_amount_to_trade,\
                     self.label_order_type,\
                     self.label_positions,\
                     self.label_entry_order,\
                     self.label_order_tp,\
                     self.label_order_sl,\
                     self.label_liq_price,\
                     self.label_leverage,\
                     self.line,\
                     self.data_label_spot_usdt_balance,\
                     self.label_spot_usdt_balance,\
                     self.data_label_amount,\
                     self.button_1x,\
                  
                     self.spinbox_slash,\
                     self.data_label_fragments,\
                     self.data_label_time_range,\
                     self.data_label_tp_setting,\
                     self.dynamic_tp,\
                     self.data_label_sl_setting,\
                     self.dynamic_sl,\
                     self.button_sl_liq_setting,\
                     self.button_sl_liq_setting_cog,\
                     self.data_label_entry_bid,\
                     self.combo_symbols,\
                     self.data_label_post_bids,\
                     self.data_label_balance,\
                     self.data_label_margin,\
                     self.data_label_PNL,\
                     self.data_label_PNL_pos,\
                     self.data_label_risk_ratio,\
                     self.data_label_entry,\
                     self.data_label_liq_price,\
                     self.data_label_current_price,\
                     self.data_label_liq_progress,\
                     self.data_label_order_tp,\
                     self.data_label_order_sl,\
                     self.button_limit,\
                     self.button_market,\
                     self.button_apply,\

                     self.button_force_close,\
                     self.button_auto_settings,\
                     self.button_use_sup_res,\
                     self.button_use_sup_res_settings,\
                     self.button_use_avoid,\
                     self.button_use_avoid_settings,\
                     self.button_use_email_5m,\
                     self.button_use_email_5m_settings,\
                     self.button_use_email_4h,\
                     self.button_use_email_4h_settings,\
                     self.button_maintain_balance,\
                     self.button_use_barts,\
                     self.button_use_turan,\
                     self.button_manual_long,\
                     self.button_manual_short,\
                     self.button_cancel_open_orders,\
                     self.button_cancel_all_open_orders,\
                     self.button_rebuild,\
                     self.button_refresh_pos,\
                     self.button_rebuild_cog,\
                     self.button_allow_auto,\
                     self.button_allow_longs,\
                     self.button_allow_shorts,\
                     self.header_spot_account,\
               
                     self.label_transfer_amount,\
                     self.data_label_transfer_amount,\
                     self.button_spot_fut,\
                     self.button_fut_spot,\
                     self.button_inject_account,\
                     self.label_to_address,\
                     self.data_label_to_address,\
                     self.button_withdraw]
                     
        for widget in hide_list:
            widget.setGeometry(QtCore.QRect(-999, -999, 0, 0))


    def hide_Dashboard_UI(self):

        hide_dash_list = [self.header_dash_totals,\
                     self.label_dash_balances_total,\
                     self.data_label_dash_balances_total,\
                     self.label_dash_margins_total,\
                     self.data_label_dash_margins_total,\
                     self.label_dash_pnl_total,\
                     self.data_label_dash_pnl_total,\
                     self.header_dash_win_lose,\
                     self.button_clear_stats,\
                     self.label_dash_global_wins_amount,\
                     self.data_label_dash_global_wins_amount,\
                     self.label_dash_global_losses_amount,\
                     self.data_label_dash_global_losses_amount,\
                     self.label_dash_global_difference,\
                     self.data_label_dash_global_difference,\
                     self.label_dash_global_ratio,\
                     self.data_label_dash_global_ratio,\
                     self.label_dash_global_ratio_event,\
                     self.data_label_dash_global_ratio_event,\
                     self.header_global_auto,\
                     self.button_global_activate,\
                     self.button_global_chart,\
                     self.button_global_spread,\
                     self.button_global_spread_settings,\
                     self.header_global_settings,\
                     self.button_slasher,\
                     self.button_slasher_settings,\
                     self.button_padding,\
                     self.button_padding_settings,\
                     self.button_travel_mode,\
                     self.button_skim,\
                     self.button_skim_settings,\
                     self.button_auto_move]


        for widget in hide_dash_list:
            widget.setGeometry(QtCore.QRect(-999, -999, 0, 0))



    def hide_Plus_UI(self):

        hide_plus_list = [self.header_add_binance,\
                          self.label_add_account_api,\
                          self.data_label_add_account_api,\
                          self.label_add_account_sec,\
                          self.data_label_add_account_sec,\
                          self.header_add_travel_api,\
                          self.label_add_account_travel_api,\
                          self.data_label_add_account_travel_api,\
                          self.label_add_account_travel_sec,\
                          self.data_label_add_account_travel_sec,\
                          self.label_what_this,\
                          self.button_add_account]


        for widget in hide_plus_list:
            widget.setGeometry(QtCore.QRect(-999,-999,0,0))


            


    #CONFIGURE UI METHODS
    def configure_Dashboard_UI(self):

        if self.first_run == False:

            self.hide_Accounts_UI()
            self.hide_Plus_UI()

            #HEADER
            self.header_dash_totals.setGeometry(QtCore.QRect(16, 32, 130, 16))

            #DASHBOARD - TOTALS
            self.label_dash_balances_total.setGeometry(QtCore.QRect(16, 64, 110, 16))
            self.data_label_dash_balances_total.setGeometry(QtCore.QRect(128, 64+1, 145, 17))
            #
            self.label_dash_margins_total.setGeometry(QtCore.QRect(16, 96, 110, 16))
            self.data_label_dash_margins_total.setGeometry(QtCore.QRect(128, 96+1, 145, 16))
            #
            self.label_dash_pnl_total.setGeometry(QtCore.QRect(16, 128, 110, 16))
            self.data_label_dash_pnl_total.setGeometry(QtCore.QRect(128, 128+1, 145, 16))
            #HEADER
            self.header_dash_win_lose.setGeometry(QtCore.QRect(16, 160, 130, 16))
            self.button_clear_stats.setGeometry(QtCore.QRect(127, 160, 50, 17))
            #DASHBOARD - STATS -WIN/LOSE
            self.label_dash_global_wins_amount.setGeometry(QtCore.QRect(16, 192, 81, 16))
            self.data_label_dash_global_wins_amount.setGeometry(QtCore.QRect(128, 192+1, 145, 17))
            #
            self.label_dash_global_losses_amount.setGeometry(QtCore.QRect(16, 224, 83, 16))
            self.data_label_dash_global_losses_amount.setGeometry(QtCore.QRect(128, 224+1, 145, 16))
            #
            self.label_dash_global_difference.setGeometry(QtCore.QRect(16, 256, 83, 16))
            self.data_label_dash_global_difference.setGeometry(QtCore.QRect(128, 256+1, 145, 16))
            #
            self.label_dash_global_ratio_event.setGeometry(QtCore.QRect(16, 288, 110, 16))
            self.data_label_dash_global_ratio_event.setGeometry(QtCore.QRect(128, 288+1, 145, 16))
            #
            self.label_dash_global_ratio.setGeometry(QtCore.QRect(16, 320, 110, 16))
            self.data_label_dash_global_ratio.setGeometry(QtCore.QRect(128, 320+1, 145, 16))
            #START SERVER / CHART
            self.header_global_auto.setGeometry(QtCore.QRect(752, 32, 99, 16))
            #
            self.button_global_activate.setGeometry(QtCore.QRect(752, 64, 132, 28))
            self.button_global_chart.setGeometry(QtCore.QRect(752, 96, 132, 28))
            #GLOBAL SETTINGS
            self.header_global_settings.setGeometry(QtCore.QRect(752, 144, 99, 16))
            #
            self.button_global_spread.setGeometry(QtCore.QRect(752, 176, 132, 28))
            self.button_global_spread_settings.setGeometry(QtCore.QRect(887, 176, 22, 28))
            #
            self.button_slasher.setGeometry(QtCore.QRect(752, 208, 132, 28))
            self.button_slasher_settings.setGeometry(QtCore.QRect(887, 208, 22, 28))
            #
            self.button_padding.setGeometry(QtCore.QRect(752, 240, 132, 28))
            self.button_padding_settings.setGeometry(QtCore.QRect(887, 240, 22, 28))
            #
            self.button_auto_move.setGeometry(QtCore.QRect(752, 272, 132, 28))
            #
            self.button_travel_mode.setGeometry(QtCore.QRect(752, 304, 132, 28))

            #hide for now
            self.button_skim.setGeometry(QtCore.QRect(-999,-999,132,28))#752, 336, 132, 28))
            self.button_skim_settings.setGeometry(QtCore.QRect(-999,-999,22,28))#887, 336, 22, 28))
            
            
    def configure_Accounts_UI(self):

        if self.first_run == False:
            self.hide_Dashboard_UI()
            self.hide_Plus_UI()
            self.header_futures_account.setGeometry(QtCore.QRect(16, 32, 112, 16))
            self.label_balance.setGeometry(QtCore.QRect(16, 64, 81, 16))
            self.data_label_balance.setGeometry(QtCore.QRect(128, 64, 145, 17))
            self.label_margin.setGeometry(QtCore.QRect(16, 96, 81, 16))
            self.data_label_margin.setGeometry(QtCore.QRect(128, 96, 110, 16))
            self.data_label_risk_ratio.setGeometry(QtCore.QRect(241, 96, 31, 16))
            self.label_PNL.setGeometry(QtCore.QRect(16, 128, 81, 16))
            self.data_label_PNL.setGeometry(QtCore.QRect(128, 128, 71, 16))
            self.data_label_PNL_pos.setGeometry(QtCore.QRect(202, 128, 71, 16))
            self.header_positions.setGeometry(QtCore.QRect(16, 160, 110, 16))
            self.label_positions.setGeometry(QtCore.QRect(24, 192, 99, 16))
            self.combo_positions.setGeometry(QtCore.QRect(136, 192, 145, 17))
            self.button_force_close.setGeometry(QtCore.QRect(136, 218, 70, 20))
            self.button_refresh_pos.setGeometry(QtCore.QRect(283, 191, 18, 19))
            self.spinbox_slash.setGeometry(QtCore.QRect(208, 219, 72, 22))
            self.button_increase_position.setGeometry(QtCore.QRect(246, 219, 17, 18))
            self.button_decrease_position.setGeometry(QtCore.QRect(264, 219, 17, 18))
            self.label_liq_price.setGeometry(QtCore.QRect(24, 256, 99, 16))
            self.data_label_liq_price.setGeometry(QtCore.QRect(136, 256, 56, 16))
            self.data_label_current_price.setGeometry(QtCore.QRect(194, 256, 56, 16))
            self.data_label_liq_progress.setGeometry(QtCore.QRect(252, 256, 29, 16))
            self.header_linked_orders.setGeometry(QtCore.QRect(16, 288, 110, 16))
            self.label_entry_order.setGeometry(QtCore.QRect(24, 320, 99, 16))
            self.data_label_entry.setGeometry(QtCore.QRect(136, 320, 145, 16))
            self.label_order_tp.setGeometry(QtCore.QRect(24, 352, 99, 16))
            self.data_label_order_tp.setGeometry(QtCore.QRect(136, 352, 145, 16))
            self.label_order_sl.setGeometry(QtCore.QRect(24, 384, 99, 16))
            self.data_label_order_sl.setGeometry(QtCore.QRect(136, 384, 145, 16))
            self.button_cancel_open_orders.setGeometry(QtCore.QRect(135, 410, 74, 20))
            self.button_cancel_all_open_orders.setGeometry(QtCore.QRect(135, 431, 74, 20))
            self.button_rebuild.setGeometry(QtCore.QRect(210, 410, 71, 20))
            self.button_rebuild_cog.setGeometry(QtCore.QRect(282, 410, 18, 20))
            self.header_trade_settings.setGeometry(QtCore.QRect(400, 32, 99, 16))
            self.label_leverage.setGeometry(QtCore.QRect(400, 64, 81, 16))
            self.lev_Slider.setGeometry(QtCore.QRect(496, 64, 102, 16))
            self.data_label_lev.setGeometry(QtCore.QRect(603, 64, 22, 17))
            self.line.setGeometry(QtCore.QRect(400, 80, 225, 16))
            self.label_order_type.setGeometry(QtCore.QRect(400, 96, 81, 16))
            self.label_amount_to_trade.setGeometry(QtCore.QRect(400, 160, 81, 16))
            self.label_fragments.setGeometry(QtCore.QRect(400, 192, 81, 16))
            self.label_time_range.setGeometry(QtCore.QRect(400, 224, 81, 16))
            self.button_market.setGeometry(QtCore.QRect(496, 96, 63, 17))
            self.button_limit.setGeometry(QtCore.QRect(562, 96, 63, 17))
            self.label_pair_symbol.setGeometry(QtCore.QRect(400, 128, 81, 16))
            self.combo_symbols.setGeometry(QtCore.QRect(496, 128, 129, 16))
            self.data_label_amount.setGeometry(QtCore.QRect(496, 160, 86, 16))
            self.button_1x.setGeometry(QtCore.QRect(586, 160, 39, 17))
            self.data_label_fragments.setGeometry(QtCore.QRect(496, 192, 129, 16))
            self.data_label_time_range.setGeometry(QtCore.QRect(496, 224, 129, 16))
            self.label_tp_setting.setGeometry(QtCore.QRect(400, 256, 81, 16))
            self.data_label_tp_setting.setGeometry(QtCore.QRect(496, 256, 129, 16))
            self.dynamic_tp.setGeometry(QtCore.QRect(496, 282, 68, 20))#tp dynamic button
            self.label_sl_setting.setGeometry(QtCore.QRect(400, 320, 81, 16))
            self.data_label_sl_setting.setGeometry(QtCore.QRect(496, 320, 129, 16))
            self.dynamic_sl.setGeometry(QtCore.QRect(496, 346, 68, 20))#sl dynamic button
            self.button_sl_liq_setting.setGeometry(QtCore.QRect(565, 346, 60, 20))#sl liq dynamic button
            self.button_sl_liq_setting_cog.setGeometry(QtCore.QRect(626, 346, 18, 20))#sl liq dynamic button
            self.label_entry_bid.setGeometry(QtCore.QRect(400, 384, 81, 16))
            self.data_label_entry_bid.setGeometry(QtCore.QRect(496, 384, 129, 16))
            self.label_post_bids.setGeometry(QtCore.QRect(400, 416, 81, 16))
            self.data_label_post_bids.setGeometry(QtCore.QRect(496, 416, 129, 16))
            self.button_apply.setGeometry(QtCore.QRect(512, 448, 113, 28)) #was 384
            #
            

            #AUTOMATION
            self.header_automation.setGeometry(QtCore.QRect(752, 32, 73, 16))
            
            self.button_allow_auto.setGeometry(QtCore.QRect(752, 64, 132, 28))
            self.button_auto_settings.setGeometry(QtCore.QRect(887, 64, 22, 28))
            self.button_maintain_balance.setGeometry(QtCore.QRect(752, 96, 132, 28)) #336

            self.header_algorithm_builder.setGeometry(QtCore.QRect(752, 144, 99, 16)) #176

            self.button_allow_longs.setGeometry(QtCore.QRect(752, 176, 132, 28))
            self.button_allow_shorts.setGeometry(QtCore.QRect(752, 208, 132, 28))
            
            self.button_use_sup_res.setGeometry(QtCore.QRect(752, 240, 132, 28))
            self.button_use_sup_res_settings.setGeometry(QtCore.QRect(887, 240, 22, 28))

            self.button_use_avoid.setGeometry(QtCore.QRect(752, 272, 132, 28))
            self.button_use_avoid_settings.setGeometry(QtCore.QRect(887, 272, 22, 28))
            self.button_use_email_5m.setGeometry(QtCore.QRect(752, 304, 132, 28))
            self.button_use_email_5m_settings.setGeometry(QtCore.QRect(887, 304, 22, 28))
            self.button_use_email_4h.setGeometry(QtCore.QRect(752, 336, 132, 28))
            self.button_use_email_4h_settings.setGeometry(QtCore.QRect(887, 336, 22, 28))
            self.button_use_barts.setGeometry(QtCore.QRect(752, 368, 132, 28))
            self.button_use_turan.setGeometry(QtCore.QRect(752, 400, 132, 28))

            self.header_manual.setGeometry(QtCore.QRect(752, 448, 102, 16))
            self.button_manual_long.setGeometry(QtCore.QRect(752, 480, 132, 28))
            self.button_manual_short.setGeometry(QtCore.QRect(752, 512, 132, 28))

            spot_data_width = 145 #128

            spot_shift_y = 16
            
            #SPOT ACCOUNT - HEADER/DEP ADDRESS
            self.header_spot_account.setGeometry(QtCore.QRect(16, 480-spot_shift_y, 140, 16))



            #USDT BALANCE
            self.label_spot_usdt_balance.setGeometry(QtCore.QRect(16, 512-spot_shift_y, 145, 16))
            self.data_label_spot_usdt_balance.setGeometry(QtCore.QRect(128, 512-spot_shift_y, spot_data_width, 16))

            #TRANSFER
            self.label_transfer_amount.setGeometry(QtCore.QRect(16, 544-spot_shift_y, 81, 16))
            self.data_label_transfer_amount.setGeometry(QtCore.QRect(128, 544-spot_shift_y, spot_data_width, 16))

            #BUTTONS
            self.button_spot_fut.setGeometry(QtCore.QRect(16, 576-spot_shift_y, 62, 22))
            self.button_fut_spot.setGeometry(QtCore.QRect(80, 576-spot_shift_y, 62, 22))


            self.button_inject_account.setGeometry(QtCore.QRect(144, 576-spot_shift_y, 55, 22))


            self.button_withdraw.setGeometry(QtCore.QRect(211, 576-spot_shift_y, 62, 22))



    def configure_Plus_UI(self):

        if self.first_run == False:
            self.hide_Accounts_UI()
            self.hide_Dashboard_UI()

        input_label_width = 404
        
        #config
        self.header_add_binance.setGeometry(QtCore.QRect(16, 32, 360, 16))
        
        self.label_add_account_api.setGeometry(QtCore.QRect(16, 64, 81, 16))
        self.data_label_add_account_api.setGeometry(QtCore.QRect(88, 64, input_label_width, 17))
        #
        self.label_add_account_sec.setGeometry(QtCore.QRect(16, 96, 81, 16))
        self.data_label_add_account_sec.setGeometry(QtCore.QRect(88, 96, input_label_width, 16))
        #


        #config
        self.header_add_travel_api.setGeometry(QtCore.QRect(16, 128, 360, 16))
        
        self.label_add_account_travel_api.setGeometry(QtCore.QRect(16, 160, 90, 16))
        self.data_label_add_account_travel_api.setGeometry(QtCore.QRect(88+30, 160, input_label_width-30, 17))
        #
        self.label_add_account_travel_sec.setGeometry(QtCore.QRect(16, 192, 90, 16))
        self.data_label_add_account_travel_sec.setGeometry(QtCore.QRect(88+30, 192, input_label_width-30, 16))

        self.label_what_this.setGeometry(QtCore.QRect(4+340, 214, 162, 16))

        #submit button
        self.button_add_account.setGeometry(QtCore.QRect(16+394, 248, 81, 24))


        if self.first_run == False:
            self.header_add_binance.setText("Add another Binance API account")
        elif self.first_run == True:
            self.header_add_binance.setText("Please link your Binance API account")

        #if 2 accounts already exist, block user from adding more...for now...
        if len(self.accounts_list) > 1:
            self.header_add_binance.setText("Only a maximum of two accounts is currently supported!")
            self.data_label_add_account_api.setEnabled(False)
            self.data_label_add_account_sec.setEnabled(False)
            self.button_add_account.setEnabled(False)
            self.data_label_add_account_travel_api.setEnabled(False)
            self.data_label_add_account_travel_sec.setEnabled(False)







##### LOAD/SHUT DOWN WINDOWS ##########################################################################################




    def kill_Process(self,pid):
        s.Popen('taskkill /F /PID {0}'.format(pid),shell=True)




    def kill_Processes_Backend(self): #2 or 3

        #get pids
        pid_backend = int(txt_ops.quick_read_txt_file('txt/pids/pid_backend.txt'))
        pid_requests = int(txt_ops.quick_read_txt_file('txt/pids/pid_requests.txt'))
        pid_protect = int(txt_ops.quick_read_txt_file('txt/pids/pid_protect.txt'))

        
        try:
            self.kill_Process(pid_requests)
        except:
            print("\nWarning: Couldn't kill process Requests_Manager.py")
        
        try:
            self.kill_Process(pid_backend)
        except:
            print("\nWarning: Couldn't kill process Entry_Manager.py")

        try:
            self.kill_Process(pid_protect)
        except:
            print("\nWarning: Couldn't kill process Guardian.py")


    def kill_Processes_All(self): #2 or 3
        try:
            pid_requests = int(txt_ops.quick_read_txt_file('txt/pids/pid_requests.txt'))
            self.kill_Process(pid_requests)
            sys.exit()
        except:
            print("\nWarning: Couldn't kill process Requests_Manager.py")
        try:
            pid_backend = int(txt_ops.quick_read_txt_file('txt/pids/pid_backend.txt'))
            self.kill_Process(pid_backend)
            sys.exit()
        except:
            print("\nWarning: Couldn't kill process Entry_Manager.py")
##        try:
##            pid_candle_chart = int(txt_ops.quick_read_txt_file('txt/pids/pid_candle_chart.txt'))
##            self.kill_Process(pid_candle_chart)
##        except:
##            print("\nWarning: Couldn't kill process Power_Chart.py")
        try:
            pid_protect = int(txt_ops.quick_read_txt_file('txt/pids/pid_protect.txt'))
            self.kill_Process(pid_protect)
            sys.exit()
        except:
            print("\nWarning: Couldn't kill process Guardian.py")



    def global_Activate(self):

        method = 1

        print("\nLoad backend clicked...")

        if self.global_activate == 0:

            if method == 1:
                requests_proc = s.Popen(['python','Requests_Manager.py'],shell=False)
                entry_proc = s.Popen(['python','Entry_Manager.py'],shell=False)
                guardian_proc = s.Popen(['python','Guardian.py'],shell=False)
            elif method == 2:
                os.system("start cmd /k Requests_Manager.py")
                os.system("start cmd /k Entry_Manager.py")
                os.system("start cmd /k Guardian.py")          

            self.global_activate = 1

        elif self.global_activate == 1:

            self.kill_Processes_Backend()

            self.global_activate = 0

            

    def load_Power_Graph(self):
        pass
##        if self.load_chart == 0:
##            try:
##                print("\nLaunching PowerGraph...")
##                candle_proc = s.Popen(['python','Power_Chart.py'],shell=True)
##                self.load_chart = 1
##            except:
##                print("\nError: Unable to launch PowerGraph.")
##        elif self.load_chart == 1:
##            try:
##                print("\nClosing PowerGraph...")
##                pid_candle_chart = int(txt_ops.quick_read_txt_file('txt/pids/pid_candle_chart.txt'))
##                self.kill_Process(pid_candle_chart)
##                self.load_chart = 0
##            except:
##                print("\nError: Unable to close PowerGraph.")
##            
##

    def restart_Omicron(self):
        os.startfile(sys.argv[0])
        self.kill_Processes_All()
        sys.exit()        




    def kill_All_Exit(self):

        self.kill_Processes_All()
        sys.exit()
        time.sleep(0.2)
        sys.exit()
        time.sleep(0.2)
        sys.exit()


    def travel_Mode_Toggle(self):
        read_current_setting = int(self.txt_ops.quick_read_txt_file('txt/settings/travel_mode.txt'))
        if read_current_setting == 0:
            write_em = self.txt_ops.quick_write_txt_file('txt/settings/travel_mode.txt',1)
        elif read_current_setting == 1:
            write_em = self.txt_ops.quick_write_txt_file('txt/settings/travel_mode.txt',0)
        #self.build_Menu()

    def closeEvent(self,event):

            reply = QMessageBox.question(
                self, "Exit Omicron",
                " Are you sure you want to quit? ",
                QMessageBox.Close | QMessageBox.Cancel)

            if reply == QMessageBox.Close:
                self.kill_Processes_All()
                event.accept()
            else:
                event.ignore()


##### END LOAD/SHUT DOWN WINDOWS ##########################################################################################













###### UPDATES #######################################################################################################


    def download_New_Version(self):
        url = "https://astaroth.pythonanywhere.com/download"
        webbrowser.open(url,new=2)

    def check_Updates(self):

        try:

            #change this version no before each compile
            

            #get latest version from website
            latest_version = explore_Version()

            print("Latest version is",str(latest_version))


     

            if latest_version == self.this_version and self.first_run == True:
                self.statusBar.showMessage("Omicron " + str(self.this_version / 100) + " is ready. Please input your Binance API details to create an account and begin trading.")
                #
                create_style_string = "color:green;"
                self.statusBar.setStyleSheet(create_style_string)

                #hide button
                self.download_new.setVisible(False)


            if latest_version == self.this_version and self.first_run == False:
                self.statusBar.showMessage("Omicron " + str(self.this_version / 100) + " is ready. Click Start Server in the top right to begin.")
                #
                create_style_string = "color:green;"
                self.statusBar.setStyleSheet(create_style_string)

                #hide button
                self.download_new.setVisible(False)


            #compare the two version numbers
            if latest_version > self.this_version:

                #new version message
                self.statusBar.showMessage("A new version of Omicron " + str(latest_version / 100) + " is available!")
                create_style_string = "color:green;"
                self.statusBar.setStyleSheet(create_style_string)

                #show button
                self.download_new.setVisible(True)

            #compare the two version numbers
            if latest_version < self.this_version:

                #new version message
                self.statusBar.showMessage("Omicron Developer Environment")
                create_style_string = "color:green;"
                self.statusBar.setStyleSheet(create_style_string)

        except:

            print("\nVersion check error: Internet connection.")

            
###### END UPDATES #######################################################################################################










#### SETUP FUNCTIONS ###########################################################################################################        





    def ping_Server(self,api_key,sec_key):

        response = ''

        futures_balance = 0

        url = 'http://fapi.binance.com/fapi/v2/balance'

        headers = {
            'X-MBX-APIKEY': api_key
        }

        timestamp = int(str(int(time.time())) + '000')

        params = {
            'recvWindow':5000,
            'timestamp':timestamp
        }

        query_string = urlencode(params)
        params['signature'] = hmac.new(sec_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        
        r = requests.get(url, headers=headers, params=params)
        
        if r.status_code == 200:
            data = r.json()
            response = 'connected'
        else:
            response = 'error'

        return response



    def get_Current_Price(self,pair_symbol):

        #get current price of the asset
        price_functions_static = Price_Functions(1)
        current_price = price_functions_static.request_Price_Data(pair_symbol)[0]

        return current_price





    #Example use: max_Afford_Amount(11,'ETHUSDT',3)
    #^How much ETH can be bought with the available USDT balance in Account 11, assuming min 3x leverage is allowed...^
    def max_Afford_Amount(self,account_num,pair_symbol):

        coin_settings_path = "txt/setup/" + str(account_num) + "/setup_1_" + pair_symbol + '.txt'

        settings = Settings(account_num)
        b = settings.load_Trade_Variables(pair_symbol)
        leverage = int(b[37])

        #get futures balance
        balance_functions = Balance_Functions(account_num)
        get_balance_data = balance_functions.request_Futures_Balances()
        get_balance = get_balance_data[0]
        get_margin = get_balance_data[1]

        order_pos_functions = Order_Pos_Functions(account_num)
        pos_array = order_pos_functions.read_Position_Data()
        pos_length = len(pos_array)

        #margin required
        margin_required = get_balance / leverage
        margin_free = ((get_margin * leverage) / pos_length) - (margin_required)

        rec_amount = (margin_free) / self.get_Current_Price(pair_symbol)
        rec_amount = float("%.4f"%(rec_amount)) * 100
        rec_amount = math.ceil(rec_amount / 2.) * 2
        rec_amount = rec_amount / 100

        return rec_amount



    def calc_1x(self):

        pair_symbol = self.combo_symbols.currentText()#self.data_label_pair_symbol.text()

        amount = str(self.max_Afford_Amount(self.current_tab_id,pair_symbol))

        self.data_label_amount.setText(amount)

        




    def create_Default_Files(self,origin_folder,compare_folder,create_file_name,line_array):

        make_setup_str = ''

        length = len(line_array)

        origin_array = []
        
        origin_array = self.maths_functions.count_Files(origin_folder)[1]

        compare_array = self.maths_functions.count_Files(compare_folder)[1]

        intersect = [i for i in origin_array if i not in compare_array]

        if intersect != []:

            if length > 0 and line_array == [1]:

                 for j in intersect:
                     
                     order_pos_dynamic = Order_Pos_Functions(j)
                     x = order_pos_dynamic.request_Position_Information()
                     print(x)
                  

            elif length > 0 and line_array == [2]:

                for j in intersect:
                    
                    balance_functions = Balance_Functions(j)
                    y = balance_functions.request_Futures_Balances_With_Client()
                    print(y)
                    
            
            elif length > 0 and line_array == [3]:

                for j in intersect:
                
                    order_pos_dynamic = Order_Pos_Functions(j)
                    z = order_pos_dynamic.request_Open_Orders_Data()
                    print(z)

                    
            elif length > 0 and (line_array != [1] or line_array != [2] or line_array != [3]):

                for j in intersect:

                    #create a new folder, for each position
                    new_folder = str(j)
                    if not os.path.exists(new_folder):
                        os.makedirs(new_folder)                       

                    make_setup_str = str('txt/setup/' + new_folder + '/setup' + '_') + str(j) + str(".txt")
                    #make_setup_str = str(compare_folder + create_file_name + '_') + str(j) + str(".txt")

                    print("make_setup_str:",make_setup_str)

                    with open(make_setup_str,'w') as out:

                        for r in range(length):
                        
                            out.write('{}\n'.format(str(line_array[r])))





    def create_Default_Pair_Settings_Array(self,pair_symbol):


        quantity_to_trade_str = ''
        take_profit_str = ''
        stop_loss_str = ''
        initial_bid_str = ''
        bids_str = ''
        avoid_region_long_str = ''
        avoid_region_short_str = ''


        if pair_symbol == 'ETHUSDT':

            quantity_to_trade_str = 'quantity_to_trade=0.6'
            take_profit_str = 'take_profit=16'
            stop_loss_str = 'stop_loss=500'
            initial_bid_str = 'initial_bid=0.11'
            bids_str = 'bids=0.09'
            avoid_region_long_str = "avoid_region_long=2700"
            avoid_region_short_str = "avoid_region_short=2200"
            mode_buffer_str = "mode_buffer=1"

        elif pair_symbol == 'LTCUSDT':

            quantity_to_trade_str = 'quantity_to_trade=12'
            take_profit_str = 'take_profit=2'
            stop_loss_str = 'stop_loss=50'
            initial_bid_str = 'initial_bid=0.01'
            bids_str = 'bids=0.01'
            avoid_region_long_str = "avoid_region_long=177"
            avoid_region_short_str = "avoid_region_short=100"
            mode_buffer_str = "mode_buffer=0.2"

        elif pair_symbol == 'ADAUSDT':

            quantity_to_trade_str = 'quantity_to_trade=1000'
            take_profit_str = 'take_profit=0.022'
            stop_loss_str = 'stop_loss=1'
            initial_bid_str = 'initial_bid=0.0001'
            bids_str = 'bids=0.0001'
            avoid_region_long_str = "avoid_region_long=1.4"
            avoid_region_short_str = "avoid_region_short=0.8"
            mode_buffer_str = "mode_buffer=0.002"

        elif pair_symbol == 'BTCUSDT':

            quantity_to_trade_str = 'quantity_to_trade=0.04'
            take_profit_str = 'take_profit=388'
            stop_loss_str = 'stop_loss=10001'
            initial_bid_str = 'initial_bid=22'
            bids_str = 'bids=11'
            avoid_region_long_str = "avoid_region_long=48000"
            avoid_region_short_str = "avoid_region_short=35000"
            mode_buffer_str = "mode_buffer=2"


        elif pair_symbol == 'BNBUSDT':

            quantity_to_trade_str = 'quantity_to_trade=4'
            take_profit_str = 'take_profit=5'
            stop_loss_str = 'stop_loss=300'
            initial_bid_str = 'initial_bid=0.01'
            bids_str = 'bids=0.01'
            avoid_region_long_str = "avoid_region_long=1000"
            avoid_region_short_str = "avoid_region_short=100"
            mode_buffer_str = "mode_buffer=1"


        settings_array = ["active=1",\
                          "busy=0",\
                          quantity_to_trade_str,\
                          "split_order_into_segments=4",\
                          "order_split_time_range=600",\
                          take_profit_str,\
                          stop_loss_str,\
                            "stop_to_limit_spread=0.02",\
                            "is_limit_entry=1",\
                            initial_bid_str,\
                            bids_str,\
                            "manual_trigger_long=0",\
                            "manual_trigger_short=0",\
                            "auto_longs=1",\
                            "auto_shorts=1",\
                            "cancel_linked=0",\
                            "force_close=0",\
                            "rebuild=0",\
                            "use_liq_sl=0",\
                            "dynamic_tp=0",\
                            "use_mail_5m=1",\
                            "use_mail_4h=1",\
                            "use_sup_res=1",\
                            "use_avoid=1",\
                            "use_round=0",\
                            "use_barts=0",\
                            "use_turan=0",\
                            "dynamic_sl=0",\
                            "mode_algo=GOLD",\
                            mode_buffer_str,\
                            "auto_sl_breach=0.01",\
                            "tp_type=FULL",\
                            "sl_type=NONE",\
                            avoid_region_long_str,\
                            avoid_region_short_str,\
                            "orders=[]",\
                            "positions=[]",\
                            "leverage=30",\
                            "req_lev_change=30",\
                            "mode_search_mins=120"]


        return settings_array
      




    def create_Default_Account_Settings_Array(self,account_no):

        dep_address_str = 'dep_address_USDT=0x'


        settings_array = ['active=1',\
                           'busy=0',\
                           'balance=[]',\
                           'last_combo_pos=ETHUSDT',\
                           'last_combo_settings=ETHUSDT',\
                           dep_address_str,\
                           'open_orders=[]',\
                           'open_positions=[]',\
                          'transfer_asset=USDT',\
                          'transfer_asset_amount=0',\
                          'spot_fut=0',\
                          'fut_spot=0',\
                          'withdraw=0',\
                          'maintain_balance=1']



        return settings_array
      


    def create_Default_Settings_Folders(self):
       
        #first count setup folders, derived from number of login files
        count_login_files = self.maths_functions.count_Files('txt/login/')[0]
        print('count_login_files',count_login_files)

        #inside each of these folders, create a first setup file, if none exist...
        for c in range(count_login_files):

            print('C+1',c+1)

            
        
            new_folder_path = 'txt/setup/' + str(c+1)
            

            
            if not os.path.exists(new_folder_path):

                #create missing folder
                os.makedirs(new_folder_path)

        #first count setup folders, derived from number of login files
        count_folders = self.maths_functions.count_Folders('txt/setup/')
        print('count_folders',count_folders)

        for d in range(count_folders):

            #--------------------------------------------#

            #create a default accounts file
            account_file_path = 'txt/setup/' + str(d+1) + '/setup_' + str(d+1) + '.txt'

            if os.path.exists(account_file_path):
                check_val = self.txt_ops.quick_read_txt_file(account_file_path)
                if check_val == '':
                    #add a settings file to it
                    account_settings_array = self.create_Default_Account_Settings_Array(d+1)
                    length = len(account_settings_array)

                    with open(account_file_path,'w') as out:
                        for r in range(length):
                            out.write('{}\n'.format(str(account_settings_array[r])))

            if not os.path.exists(account_file_path):

                #add a settings file to it
                account_settings_array = self.create_Default_Account_Settings_Array(d+1)
                length = len(account_settings_array)

                with open(account_file_path,'w') as out:
                    for r in range(length):
                        out.write('{}\n'.format(str(account_settings_array[r])))

            #--------------------------------------------#
            allowed_symbols_array = ['BTCUSDT','ETHUSDT','ADAUSDT','LTCUSDT','BNBUSDT']
            length_allowed = len(allowed_symbols_array)

            if length_allowed > 0:

                

                for i in range(len(allowed_symbols_array)):

                    pair_symbol = allowed_symbols_array[i]

                    default_file_path = 'txt/setup/' + str(d+1) + '/setup_' + str(d+1) + '_' + pair_symbol + '.txt'

                    print('d+1',d+1)

                    if not os.path.exists(default_file_path):

                        #add a settings file to it
                        line_array = self.create_Default_Pair_Settings_Array(pair_symbol)
                        length = len(line_array)

                        with open(default_file_path,'w') as out:
                            for r in range(length):
                                out.write('{}\n'.format(str(line_array[r])))



        



    def get_API_Tutorial(self):
        url = "https://www.astaroth.tech/quick_start"
        webbrowser.open(url,new=3)


    def create_Default_Files_Man(self):

        self.create_Default_Settings_Folders()

        if self.first_run == True:
            write_spread_active = self.txt_ops.quick_write_txt_file('txt/settings/spread/spread_active.txt',0)
            write_spread_value = self.txt_ops.quick_write_txt_file('txt/settings/spread/spread_value.txt',5)
            write_pnl_file = self.txt_ops.quick_write_txt_file('csv/pnl/global_pnl.csv','0,0,-1\n0,0,1')


    def create_Login_File(self,make_login_str):

        travel_validate_needed = 0

        api_key = self.data_label_add_account_api.text()
        sec_key = self.data_label_add_account_sec.text()
        travel_api_key = self.data_label_add_account_travel_api.text()
        travel_sec_key = self.data_label_add_account_travel_sec.text()

        valid = self.ping_Server(api_key,sec_key)

        if travel_api_key != '' and travel_sec_key != '':
            valid_travel = self.ping_Server(travel_api_key,travel_sec_key)
            travel_validate_needed = 1

        if (travel_validate_needed == 0 and valid == 'connected'):

            #ensure text file is created with two lines or does not work
            prep_login_file = self.txt_ops.quick_write_txt_file_plus(make_login_str,' \n\n\n ')

            with open(make_login_str, "r") as f:
                get_all = f.readlines()

            with open(make_login_str,'w') as f:
                for i,line in enumerate(get_all,1):
                    if i == 1:
                        f.writelines('api_key=' + api_key + '\n')
                    elif i == 2:
                        f.writelines('secret_key=' + sec_key + '\n')
                    else:
                        f.writelines(line)

            self.restart_Omicron()

        if (travel_validate_needed == 1 and valid == 'connected' and valid_travel == 'connected'):

            #ensure text file is created with two lines or does not work
            prep_login_file = self.txt_ops.quick_write_txt_file_plus(make_login_str,' \n\n\n ')

            with open(make_login_str, "r") as f:
                get_all = f.readlines()

            with open(make_login_str,'w') as f:
                for i,line in enumerate(get_all,1):
                    if i == 1:
                        f.writelines('api_key=' + api_key + '\n')
                    elif i == 2:
                        f.writelines('secret_key=' + sec_key + '\n')
                    elif i == 3:
                        f.writelines('em_api_key=' + travel_api_key + '\n')
                    elif i == 4:
                        f.writelines('em_secret_key=' + travel_sec_key + '\n')
                    else:
                        f.writelines(line)
            print("\nNew login file created.")

            self.restart_Omicron()

        else:

            print("\nError: Bad API details.")

            self.statusBar.showMessage("Error: Bad API details. Please try again...")

            #color styles
            create_style_string = "color:red;"
            self.statusBar.setStyleSheet(create_style_string)

            self.data_label_add_account_api.setText('')
            self.data_label_add_account_sec.setText('')




    def create_Login_File_Man(self):

        count_login_files = self.maths_functions.count_Files('txt/login/')[0]

        if os.path.isfile('txt/login/login_1.txt') == False:

            print("\nNo API files detected needed for login...")

            make_login_str = "txt/login/login_1.txt"

            self.create_Login_File(make_login_str)

 
        elif os.path.isfile('txt/login/login_1.txt') == True and count_login_files < 3:

            print("\nAdding new API account...")

            next_tab_num = int( self.master_Tabs_Container.count() ) - 1

            make_login_str = "txt/login/login_" + str(next_tab_num) + ".txt"

            self.create_Login_File(make_login_str)

        





        


###################################################################################################################################


    def progress_Bar(self,it, prefix="", size=60, file=sys.stdout):
        count = len(it)
        def show(j):
            x = int(size*j/count)
            file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
            file.flush()        
        show(0)
        for i, item in enumerate(it):
            yield item
            show(i+1)
        file.write("\n")
        file.flush()





    def request_Change_Leverage_Value(self,value):

        path_str = 'txt/setup/' + str(self.current_tab_id) + '/setup_' + str(self.current_tab_id) +\
                   '_' + str(self.combo_symbols.currentText()) + '.txt'

        lev_str = "req_lev_change=" + str(value)

        self.txt_ops.replace_Specific_Line(path_str,39,lev_str)
        
        print("\nA leverage amount of",value,"has been requested for Account",self.current_tab_id)

        self.data_label_lev.clear()
        
        self.data_label_lev.setText(str(value)+'x')
        if value < 5:
            style = "color:" + ("green") + ";"
        else:
            style = "color:" + ("red") + ";"
        self.data_label_lev.setStyleSheet(style)

  
    def request_Change_Slash_Value(self,value):

        current_tab = self.current_tab_id

        path_str = 'txt/settings/slash/requested/account_' + str(current_tab) + '.txt'
        
        write_lev_request = self.txt_ops.quick_write_txt_file(path_str,value)

        print("\nA increase/decrease percentage amount of",value,"has been requested for Account",current_tab)


    def clear_Stats(self):

        try:

            path_1 = 'txt/data/for_perf/final_pnl.txt'
            path_2 = 'txt/data/for_perf/final_wins.txt'
            path_3 = 'txt/data/for_perf/final_losses.txt'
            path_4 = 'txt/data/for_perf/final_win_events.txt'
            path_5 = 'txt/data/for_perf/final_loss_events.txt'
            path_6 = 'txt/stats/init_balance_1.txt'
            path_7 = 'txt/stats/init_balance_2.txt'

            #init_balance_2

            if os.path.exists(path_1):
                os.remove(path_1)
            if os.path.exists(path_2):
                os.remove(path_2)
            if os.path.exists(path_3):
                os.remove(path_3)
            if os.path.exists(path_4):
                os.remove(path_4)
            if os.path.exists(path_5):
                os.remove(path_5)
            if os.path.exists(path_6):
                os.remove(path_6)
            if os.path.exists(path_7):
                os.remove(path_7)
                
            #show in status bar
            make_string = "Success: Win/Lose stats cache cleared."
            self.statusBar.showMessage(make_string)
            create_style_string = "color:" + ("green") + ";"
            self.statusBar.setStyleSheet(create_style_string)

            #reset data labels live
            self.data_label_dash_global_wins_amount.setText("n/a")
            self.data_label_dash_global_losses_amount.setText("n/a")
            self.data_label_dash_global_difference.setText("n/a")
            self.data_label_dash_global_ratio.setText("n/a")
            self.data_label_dash_global_ratio_event.setText("n/a")

            self.txt_ops.quick_write_txt_file_plus(path_6,'0')
            self.txt_ops.quick_write_txt_file_plus(path_7,'0')

        except:

            print("\nError: Clear stats.")


    def toggle_Button_File_Switch(self,file_path,button_id):
        if button_id.isChecked() == True: 
            self.txt_ops.quick_write_txt_file(file_path,1)
            print("\nActivated!")
        elif button_id.isChecked() == False: 
            self.txt_ops.quick_write_txt_file(file_path,0)
            print("\nDeactivated!")


    def change_Global_Spread(self):

        current_spread_val = self.txt_ops.quick_read_txt_file('txt\settings\spread\spread_value.txt')

        if self.button_global_spread.isChecked() == True: 
            self.txt_ops.quick_write_txt_file('txt\settings\spread\spread_active.txt',1)
            print("\nPrice spread activated, current value:",current_spread_val)

        elif self.button_global_spread.isChecked() == False: 
            self.txt_ops.quick_write_txt_file('txt\settings\spread\spread_active.txt',0)
            print("\nPrice spread de-activated.")


    def set_Positions_Combo_Item_Color(self):
        current_combo_text = str( self.combo_positions.currentText() )
        print("\ncurrent_combo_text:",current_combo_text)
        try:
            side_current_combo_text = str( current_combo_text )[0]
            print("\nside_current_combo_text:",side_current_combo_text)
            if side_current_combo_text == 'L':
                create_style_string = "color:" + ("green") + ";"
                self.combo_positions.setStyleSheet(create_style_string)
            elif side_current_combo_text == 'S':
                create_style_string = "color:" + ("red") + ";"
                self.combo_positions.setStyleSheet(create_style_string)
        except:
            pass


    def force_Close_Method(self):



        playsound('audio/forceclose.wav')

        self.popup_manager.popup_Simple('Force Close')
            
            



    def adjust_Position(self,adjust_type):

        record_stats = Record_Stats(self.current_tab_id)

        print("\nAdjusting position size...")

        pos_size = 0
        percentage_inc = 0.1
        account_no = self.current_tab_id
        error_style = "color:red;"
        pass_style = "color:green;"
        status_code = 0

        #get currently active symbol from combo
        get_account_settings = Settings(account_no).load_Account_Variables()
        last_combo_pos = get_account_settings[3]
        pair_symbol = str(last_combo_pos)

        precision_functions = Precision_Functions(1)
        try:
            amount_prec_str = "%." + str( precision_functions.read_Asset_Precision(pair_symbol)[1] ) + "f"
        except:
            amount_prec_str = "%." + str( precision_functions.request_Asset_Precision(pair_symbol)[1] ) + "f"
        
        print('pair_symbol',pair_symbol)
        
        if pair_symbol != '':

            order_pos_functions = Order_Pos_Functions(account_no)

            pos_array = order_pos_functions.read_Position_Data()
            pos_array_length = len(pos_array)

            if pos_array_length > 0:

                for i in range(pos_array_length):

                    if pair_symbol == pos_array[i][0]:

                        pos_size = float(pos_array[i][1])
                        side = str(pos_array[i][3])
                        
                        #Get the percentage value for increase, default 10%
                        path_str = 'txt/settings/slash/requested/account_' + str(self.current_tab_id) + '.txt'
                        if os.path.exists(path_str): 
                            percentage_inc = int(self.txt_ops.quick_read_txt_file(path_str)) / 100

                        #Calculate amount
                        amount = float(amount_prec_str%(float(pos_size * percentage_inc)))

                        if adjust_type == 'increase':

                            #Finally place market orders
                            if side == 'LONG':

                                print("\nCreated a BUY order for",amount)

                                #cancel all open orders
                                order_pos_functions.cancel_All_Open_Orders_Symbol(pair_symbol)

                                create_market = order_pos_functions.create_Futures_Order(pair_symbol,'BUY','MARKET','null',0,0,amount)
                                status_code = int(create_market[2])
                                

                                if status_code == 200:
                                    record_stats.request_Write_USDT_Balance()
                                    self.statusBar.showMessage("Success: Increased " + pair_symbol + " position by " + str(amount))
                                    self.statusBar.setStyleSheet(pass_style)
                                else:
                                    self.statusBar.showMessage("Error: Cannot increase position (insufficient margin?)")
                                    self.statusBar.setStyleSheet(error_style)
                                    
                                
                            elif side == 'SHORT':
                                print("\nCreated a SELL order for",amount)

                                #cancel all open orders
                                order_pos_functions.cancel_All_Open_Orders_Symbol(pair_symbol)

                                create_market = order_pos_functions.create_Futures_Order(pair_symbol,'SELL','MARKET','null',0,0,amount)
                                status_code = int(create_market[2])

                                if status_code == 200:
                                    record_stats.request_Write_USDT_Balance()
                                    self.statusBar.showMessage("Success: Increased " + pair_symbol + " position by " + str(amount))
                                    #color styles
                                    self.statusBar.setStyleSheet(pass_style)
                                else:
                                    self.statusBar.showMessage("Error: Cannot increase position (insufficient margin?)")
                                    self.statusBar.setStyleSheet(error_style)

                                    
                            print("\nIncreased position",pos_size,pair_symbol,side,"by",amount)

                        elif adjust_type == 'decrease':
                            #Finally place market orders
                            if side == 'LONG':
                                print("\nCreated a SELL order for",amount)

                                #cancel all open orders
                                order_pos_functions.cancel_All_Open_Orders_Symbol(pair_symbol)
                                
                                create_market = order_pos_functions.create_Futures_Order(pair_symbol,'SELL','MARKET','null',0,0,amount)
                                status_code = int(create_market[2])
                                if status_code == 200:
                                    record_stats.request_Write_USDT_Balance()
                                    self.statusBar.showMessage("Success: Decreased " + pair_symbol + " position by " + str(amount))
                                    #color styles
                                    self.statusBar.setStyleSheet(pass_style)
                                else:
                                    self.statusBar.showMessage("Error: Cannot decrease position (insufficient margin?)")
                                    self.statusBar.setStyleSheet(error_style)
                                    

                            elif side == 'SHORT':
                                print("\nCreated a BUY order for",amount)

                                #cancel all open orders
                                order_pos_functions.cancel_All_Open_Orders_Symbol(pair_symbol)
                                
                                create_market = order_pos_functions.create_Futures_Order(pair_symbol,'BUY','MARKET','null',0,0,amount)
                                status_code = int(create_market[2])

                                if status_code == 200:
                                    record_stats.request_Write_USDT_Balance()
                                    self.statusBar.showMessage("Success: Decreased " + pair_symbol + " position by " + str(amount))
                                    self.statusBar.setStyleSheet(pass_style)
                                else:
                                    self.statusBar.showMessage("Error: Cannot decrease position (insufficient margin?)")
                                    self.statusBar.setStyleSheet(error_style)
                            print("\nIncreased position",pos_size,pair_symbol,side,"by",amount)




    def read_Display_Current_Text_Settings(self):

        if self.first_run == False:

            init_dict = {}

            self.current_tab_id = self.master_Tabs_Container.currentIndex()

            make_str = 'txt/setup/' + str(self.current_tab_id) + '/setup_' + str(self.current_tab_id) + '_' + str(self.combo_symbols.currentText()) + '.txt'

            if os.path.exists(make_str):
            
                init_dict = self.txt_ops.create_dict_from_txt(make_str,'=')

                amount = str(init_dict['quantity_to_trade'])
                self.data_label_amount.setText(amount)

                fragments = str(init_dict['split_order_into_segments'])
                self.data_label_fragments.setText(fragments)

                time_range = str(init_dict['order_split_time_range'])
                self.data_label_time_range.setText(time_range)

                take_profit = str(init_dict['take_profit'])
                self.data_label_tp_setting.setText(take_profit)

                stop_loss = str(init_dict['stop_loss'])
                self.data_label_sl_setting.setText(stop_loss)

                entry_bid = str(init_dict['initial_bid'])
                self.data_label_entry_bid.setText(entry_bid)

                post_bids = str(init_dict['bids'])
                self.data_label_post_bids.setText(post_bids)





    def apply_Trade_Settings(self):

        self.current_tab_id = self.master_Tabs_Container.currentIndex()
        make_setup_str = 'txt/setup/' + str(self.current_tab_id) + '/setup_' + str(self.current_tab_id) + '_' + str( self.combo_symbols.currentText() ) + '.txt'
      
        get_trade_amount = 'quantity_to_trade=' + str(self.data_label_amount.text()) + '\n'
        get_split_amount = 'split_order_into_segments=' + str(self.data_label_fragments.text()) + '\n'
        get_time_range = 'order_split_time_range=' + str(self.data_label_time_range.text()) + '\n'
        get_tp = 'take_profit=' + str(self.data_label_tp_setting.text()) + '\n'
        get_sl = 'stop_loss=' + str(self.data_label_sl_setting.text()) + '\n'
        get_bids = 'bids=' + str(self.data_label_post_bids.text()) + '\n'
        get_initial_bid = 'initial_bid=' + str(self.data_label_entry_bid.text()) + '\n'

        def check_Input_Valid():

            input_valid = 'false'

            #if str(self.data_label_pair_symbol.text()) != '':
            if str(self.data_label_amount.text()) != '':
                if str(self.data_label_fragments.text()) != '':
                    if str(self.data_label_time_range.text()) != '':
                        if str(self.data_label_tp_setting.text()) != '':
                            if str(self.data_label_sl_setting.text()) != '':
                                if str(self.data_label_post_bids.text()) != '':
                                    if str(self.data_label_entry_bid.text()) != '':

                                        input_valid = 'true'


            return input_valid

        
        check_input_valid = check_Input_Valid()

        if check_input_valid == 'true':

            #get text input variables and write them to relevant lines in txt file
            with open (make_setup_str, "r") as f:

                get_all=f.readlines()

            with open(make_setup_str,'w') as f:

                for i,line in enumerate(get_all,1):

                
                    if i==3:
                        f.writelines(get_trade_amount)
                    elif i==4:
                        f.writelines(get_split_amount)
                    elif i==5:
                        f.writelines(get_time_range)
                    elif i==6:
                        f.writelines(get_tp)
                    elif i==7:
                        f.writelines(get_sl)
                    elif i==10:
                        f.writelines(get_initial_bid)


                    elif i==11:
                        f.writelines(get_bids)

                    #Check if order is limit or market from buttons
                    elif i==9 and self.button_limit.isChecked() == True:
                        f.writelines('is_limit_entry=1' + '\n')
                    elif i==9 and self.button_limit.isChecked() == False:
                        f.writelines('is_limit_entry=0' + '\n')

                    else:
                        f.writelines(line)

            print("\nSettings file for Account",self.current_tab_id,"updated.")
            #print("\nVariable gotten:",self.data_label_amount.text())

        else:
            print("\nError: Please ensure that no input fields are left blank.")



    def replace_Account_Settings_Line(self,line_num,string_val):

        #get tab index
        self.current_tab_id = self.master_Tabs_Container.currentIndex()

        #create relevant setup file string
        make_setup_str = 'txt/setup/' + str(self.current_tab_id) + '/setup_' + str(self.current_tab_id) + '.txt'

        self.txt_ops.replace_Specific_Line(make_setup_str,line_num,string_val)





    def replace_Pair_Settings_Line(self,line_num,string_val):
        self.current_tab_id = self.master_Tabs_Container.currentIndex()
        #create relevant setup file string
        make_setup_str = 'txt/setup/' + str(self.current_tab_id) + '/setup_' + str(self.current_tab_id) + '_' + str( self.combo_symbols.currentText() ) + '.txt'
        self.txt_ops.replace_Specific_Line(make_setup_str,line_num,string_val)


    def cancel_All_Method(self,cancel_type):

        #import order/pos functions that will apply to this account, determined by active tab
        account_no = self.current_tab_id

        if account_no > 0: #not needed, but good practice
            
            order_pos_functions = Order_Pos_Functions(account_no)

            #playsound('audio/cancelling.wav')

            if cancel_type == 1:

                #determine symbol from currently selected combo item
                get_account_settings = Settings(account_no).load_Account_Variables()
                last_combo_pos = get_account_settings[3]
                pair_symbol = last_combo_pos

                #cancel orders linked to this symbol, leave others alone
                cancel_linked_orders = order_pos_functions.cancel_All_Open_Orders_Symbol(pair_symbol)
                print("\nOmicron GUI | Cancelled open",pair_symbol,"orders for account",account_no)

            elif cancel_type == 2:

                #cancel everything regardless of symbol 
                cancel_all_orders = order_pos_functions.cancel_All_Open_Orders()
                print("\nOmicron GUI | Cancelled all open orders for account",account_no)
                
            #clear relevant UI items
            self.data_label_order_tp.setText('')
            self.data_label_order_sl.setText('')
            self.data_label_entry.setText('')





    def rebuild_Method(self):

        playsound('audio/creating_duo.wav')

        rebuild_type = int(self.txt_ops.quick_read_txt_file('txt/settings/rebuild/rebuild_all.txt'))
        account_no = int(self.current_tab_id)

        if rebuild_type == 0:

            get_account_settings = Settings(account_no).load_Account_Variables()
            last_combo_pos = get_account_settings[3]
            pair_symbol = str(last_combo_pos)
         
            cancel_linked_open_orders = self.cancel_All_Method(1) #cancels only the dropdown pair symbol

            order_pos_functions = Order_Pos_Functions(account_no)
            create_tp_sl_orders = order_pos_functions.create_TP_and_SL(pair_symbol)

            print("\nOmicron GUI | TP/SL orders rebuilt for account",account_no,"with symbol",pair_symbol)

        if rebuild_type == 1:

            cancel_linked_open_orders = self.cancel_All_Method(2)
            
            order_pos_functions = Order_Pos_Functions(account_no)
            get_open_pos = order_pos_functions.request_Position_Information()
            for i in range(len(get_open_pos)):
                curr_symbol = get_open_pos[i][0]
                create_tp_sl_orders = order_pos_functions.create_TP_and_SL(curr_symbol)
            






    def filter_Combo_Positions_Pair_Symbol(self):

        pair_symbol = ''

        get_string = str(self.combo_positions.currentText())

        if 'ADA' in get_string:
            pair_symbol = 'ADAUSDT'
        if 'BTC' in get_string:
            pair_symbol = 'BTCUSDT'
        if 'ETH' in get_string:
            pair_symbol = 'ETHUSDT'
        if 'LTC' in get_string:
            pair_symbol = 'LTCUSDT'
        if 'BNB' in get_string:
            pair_symbol = 'BNBUSDT'
            
        print('\nFiltered pair symbol from combo positions:',pair_symbol)

        return pair_symbol


    def filter_Combo_Settings_Pair_Symbol(self):

        pair_symbol = ''

        get_string = str(self.combo_settings.currentText())

        if 'ADA' in get_string:
            pair_symbol = 'ADAUSDT'
        if 'BTC' in get_string:
            pair_symbol = 'BTCUSDT'
        if 'ETH' in get_string:
            pair_symbol = 'ETHUSDT'
        if 'LTC' in get_string:
            pair_symbol = 'LTCUSDT'
        if 'BNB' in get_string:
            pair_symbol = 'BNBUSDT'
            
        print('\nFiltered pair symbol from combo positions:',pair_symbol)

        return pair_symbol




    def load_Button_Latch_States_Dashboard(self):

        if self.first_run == False:

            def set_Button_State(input_var,button_ID):
                if input_var == 1:
                    button_ID.setChecked(True)
                elif input_var == 0:
                    button_ID.setChecked(False)

            spread_active = int(self.txt_ops.quick_read_txt_file('txt/settings/spread/spread_active.txt'))
            set_Button_State(spread_active,self.button_global_spread)            

            slasher = int(self.txt_ops.quick_read_txt_file('txt/settings/liqs/liqs_protector.txt'))
            set_Button_State(slasher,self.button_slasher)            

            padder = int(self.txt_ops.quick_read_txt_file('txt/settings/liqs/pad_protector.txt'))
            set_Button_State(padder,self.button_padding)            

            auto_move = int(self.txt_ops.quick_read_txt_file('txt/settings/liqs/auto_move.txt'))
            set_Button_State(auto_move,self.button_auto_move)            





    def load_Button_Latch_States_Accounts(self): #loads button states for accounts, only call if index type is account

        if self.first_run == False:

            def set_Button_State(input_var,button_ID):
                if input_var == 1:
                    button_ID.setChecked(True)
                elif input_var == 0:
                    button_ID.setChecked(False)

            def set_Button_State_Special(input_var,button_ID):
                if input_var == 1:
                    button_ID.setChecked(True)
                    #
                    self.data_label_entry_bid.setEnabled(False)
                    self.data_label_post_bids.setEnabled(False)
                elif input_var == 0:
                    button_ID.setChecked(False)
                    #
                    self.data_label_entry_bid.setEnabled(True)
                    self.data_label_post_bids.setEnabled(True)

            #get tab index
            self.current_tab_id = self.master_Tabs_Container.currentIndex()

            #create relevant setup file string
            pair_symbol = self.combo_symbols.currentText()

            make_setup_str = 'txt/setup/' + str(self.current_tab_id) + '/setup_' + str(self.current_tab_id) + '_' + str(pair_symbol) + '.txt'


            make_account_str = 'txt/setup/' + str(self.current_tab_id) + '/setup_' + str(self.current_tab_id) + '.txt'

            if os.path.exists(make_account_str):

                acc_dict = self.txt_ops.create_dict_from_txt(make_account_str,'=')

                try:
                
                    active = int(acc_dict['active'])
                    set_Button_State(active,self.button_allow_auto)
                except:
                    pass
                    

                try:
                    use_round = int(acc_dict['maintain_balance'])
                    set_Button_State(use_round,self.button_maintain_balance)
                except:
                    pass
                
            
            if os.path.exists(make_setup_str):

                init_dict = self.txt_ops.create_dict_from_txt(make_setup_str,'=')

                enable_limit = int(list(init_dict.values())[8])
                set_Button_State(enable_limit,self.button_limit)

                if enable_limit == 1:
                    enable_market = 0
                else:
                    enable_market = 1
                    
                set_Button_State_Special(enable_market,self.button_market)
                auto_longs = int(init_dict['auto_longs'])
                set_Button_State(auto_longs,self.button_allow_longs)            
                auto_shorts = int(init_dict['auto_shorts'])
                set_Button_State(auto_shorts,self.button_allow_shorts)            
                use_sup_res = int(init_dict['use_sup_res'])
                set_Button_State(use_sup_res,self.button_use_sup_res)            
                use_avoid = int(init_dict['use_avoid'])
                set_Button_State(use_avoid,self.button_use_avoid)
                use_liq_sl = int(init_dict['use_liq_sl'])
                set_Button_State(use_liq_sl,self.button_sl_liq_setting)

                use_dynamic_tp = int(init_dict['dynamic_tp'])
                set_Button_State(use_dynamic_tp,self.dynamic_tp)


                use_mail_5m = int(init_dict['use_mail_5m'])
                set_Button_State(use_mail_5m,self.button_use_email_5m)            
                use_mail_4h = int(init_dict['use_mail_4h'])
                set_Button_State(use_mail_4h,self.button_use_email_4h)            
                use_barts = int(init_dict['use_barts'])
                set_Button_State(use_barts,self.button_use_barts)            
                use_turan = int(init_dict['use_turan'])
                set_Button_State(use_turan,self.button_use_turan)
                use_dynamic_sl = int(init_dict['dynamic_sl'])
                set_Button_State(use_dynamic_sl,self.dynamic_sl)

                if use_dynamic_tp == 1:
                    self.data_label_tp_setting.setEnabled(False)
                else:
                    self.data_label_tp_setting.setEnabled(True)

                if use_dynamic_sl == 1 or use_liq_sl == 1:
                    self.data_label_sl_setting.setEnabled(False)
                else:
                    self.data_label_sl_setting.setEnabled(True)


    def spot_Fut_Transfer(self,flip):
        get_symbol = 'USDT'
        error_style = "color:red;"
        pass_style = "color:green;"
        status_code = 0
        get_amount = float(self.data_label_transfer_amount.text())
        if get_amount > 0:
            withdraw_functions = Withdraw_Functions(self.current_tab_id)
            if flip == 0:
                status_code = withdraw_functions.transfer_Spot_Futures(get_symbol,get_amount)
            elif flip == 1:
                status_code = withdraw_functions.transfer_Futures_Spot(get_symbol,get_amount)
            if status_code == 200:
                playsound("audio/transfer_success.wav")
                if flip == 0:
                    self.statusBar.showMessage("Success: Transferred " + str(get_amount) + " " + str(get_symbol) +\
                                               " from your Main Wallet to your Futures Wallet.")
                elif flip == 1:
                    self.statusBar.showMessage("Success: Transferred " + str(get_amount) + " " + str(get_symbol) +\
                                               " from your Futures Wallet to your Main Wallet.")
                self.statusBar.setStyleSheet(pass_style)
            else:
                playsound("audio/transfer_fail.wav")
                self.statusBar.showMessage("Error: Transfer failed with code: " + str(status_code))
                self.statusBar.setStyleSheet(error_style)
        self.data_label_transfer_amount.setText("0.00")


    def fut_Spot_Transfer(self):
        self.spot_Fut_Transfer(1)


    def inject_Account(self):

        padlock = self.txt_ops.quick_write_txt_file('txt/settings/guard/padlock.txt',1)
        current_tab = self.current_tab_id
        target_account = current_tab
        inject_amount = float(self.data_label_transfer_amount.text())
        inject_symbol = 'USDT'
        to_address = ''
        to_account = 0
        from_account = 0
        network = 'BNB'
        address_tag = ''
        status_code = 0
        pass_style = "color:green;"
        error_style = "color:red;"

        if current_tab == 1:
            from_account = 2
            to_account = 1
        elif current_tab == 2:
            from_account = 1
            to_account = 2


        withdraw_functions = Withdraw_Functions(from_account)
        status_code = withdraw_functions.transfer_Futures_Spot(inject_symbol,inject_amount)



        if status_code == 200:

            self.statusBar.showMessage("Success: Transferred " + str(inject_amount) + " " + str(inject_symbol) + " from your Futures Wallet to your Main Wallet.")
            self.statusBar.setStyleSheet(pass_style)

            #get deposit address and tag
            withdraw_functions = Withdraw_Functions(to_account)
            get_to_data = withdraw_functions.request_Deposit_Address('USDT',network)
            to_address = get_to_data[0]
            address_tag = get_to_data[1]

            #withdraw
            withdraw_functions = Withdraw_Functions(from_account)
            status_code = withdraw_functions.withdraw(inject_symbol,inject_amount,to_address,address_tag,network)

            if status_code == 200:
                self.statusBar.showMessage("Success: Withdrawal operation of " + str(inject_amount) + " " + inject_symbol + " to address " +\
                                           to_address + " with tag " + address_tag + " completed.")
                self.statusBar.setStyleSheet(pass_style)
                playsound("audio/transfer_success.wav")
                self.txt_ops.quick_write_txt_file('txt/settings/guard/padlock.txt',0)
            else:
                self.txt_ops.quick_write_txt_file('txt/settings/guard/padlock.txt',0)
                self.statusBar.showMessage("Error: [" + str(status_code) + "] Withdrawal operation of " + str(inject_amount) + " " + inject_symbol + " to address " +\
                                           to_address + " with tag " + address_tag + " failed!")
                self.statusBar.setStyleSheet(error_style)



        elif status_code == -5013:
            playsound("audio/transfer_fail.wav")
            self.statusBar.showMessage("Error: [" + str(status_code) + "] Insufficient balance to complete the transfer of " + str(inject_amount) + " " + str(inject_symbol) +\
                                       " from your Futures Wallet to your Main Wallet on account " + str(from_account) + "!")
            self.statusBar.setStyleSheet(error_style)
            self.txt_ops.quick_write_txt_file('txt/settings/guard/padlock.txt',0)
        else:
            playsound("audio/transfer_fail.wav")
            self.statusBar.showMessage("Unknown Error: [" + str(status_code) + "] Unable to transfer " + str(inject_amount) + " " + str(inject_symbol) +\
                                       " from your Futures Wallet to your Main Wallet!")
            self.statusBar.setStyleSheet(error_style)
            self.txt_ops.quick_write_txt_file('txt/settings/guard/padlock.txt',0)


    

    def my_Withdraw(self,to_address,symbol,memo,network):
        status_code = 0
        amount = float(self.data_label_transfer_amount.text())
        withdraw_functions = Withdraw_Functions(self.current_tab_id)
        if symbol == 'USDT':
            status_code = withdraw_functions.withdraw(symbol,amount,to_address,memo,network)
            if status_code == 200:
                playsound("audio/transfer_success.wav")
                self.statusBar.showMessage("Success: Withdrawal operation of " + str(amount) + " " + "USDT" + " to address " +\
                                           to_address + " with tag " + memo + " completed.")
            else:
                playsound("audio/transfer_fail.wav")
                self.statusBar.showMessage("Error: Withdrawal operation of " + str(amount) + " " + "USDT" + " to address " +\
                                           to_address + " with tag " + memo + " failed!")
        else:
       
            status_code = withdraw_functions.convert_USDT_To_Crypto_Withdraw(symbol,amount,to_address,memo,network)
            if status_code == 200:
                playsound("audio/transfer_success.wav")
                self.statusBar.showMessage("Success: Withdrawal operation of $" + str(amount) + " of " + symbol + " to address " +\
                                           to_address + " with tag " + memo + " completed.")
            else:
                playsound("audio/transfer_fail.wav")
                self.statusBar.showMessage("Error: Withdrawal operation of $" + str(amount) + " of " + symbol + " to address " +\
                                           to_address + " with tag " + memo + " failed!")



    def write_txt_On_Off_Button_State(self,button_ID,line_num,line_var):

        make_on_string = str(line_var) + '=1'
        make_off_string = str(line_var) + '=0'

        if button_ID.isChecked() == True: 
            self.replace_Pair_Settings_Line(line_num,make_on_string)
            print("\n"+line_var,"enabled for Account",self.current_tab_id)
        else:
            self.replace_Pair_Settings_Line(line_num,make_off_string)
            print("\n"+line_var,"disabled for Account",self.current_tab_id)

    def write_txt_On_Off_Button_State_A(self,button_ID,line_num,line_var):

        make_on_string = str(line_var) + '=1'
        make_off_string = str(line_var) + '=0'

        if button_ID.isChecked() == True: 
            self.replace_Account_Settings_Line(line_num,make_on_string)
            print("\n"+line_var,"enabled for Account",self.current_tab_id)
        else:
            self.replace_Account_Settings_Line(line_num,make_off_string)
            print("\n"+line_var,"disabled for Account",self.current_tab_id)

    def allow_Auto_Method(self):
        self.write_txt_On_Off_Button_State_A(self.button_allow_auto,1,'active')

    def allow_Auto_Longs_Method(self):
        self.write_txt_On_Off_Button_State(self.button_allow_longs,14,'auto_longs')

    def allow_Auto_Shorts_Method(self):
        self.write_txt_On_Off_Button_State(self.button_allow_shorts,15,'auto_shorts')

    def use_Sup_Res_Method(self):
        self.write_txt_On_Off_Button_State(self.button_use_sup_res,23,'use_sup_res')

    def use_Liq_Events_Method(self):
        self.write_txt_On_Off_Button_State(self.button_use_avoid,24,'use_avoid')

    def use_Email_5m_Method(self):
        self.write_txt_On_Off_Button_State(self.button_use_email_5m,21,'use_mail_5m')

    def use_Email_4h_Method(self):
        self.write_txt_On_Off_Button_State(self.button_use_email_4h,22,'use_mail_4h')

    def use_Round_Method(self):
        self.write_txt_On_Off_Button_State_A(self.button_maintain_balance,14,'maintain_balance')

    def use_Barts_Method(self):
        self.write_txt_On_Off_Button_State(self.button_use_barts,26,'use_barts')

    def use_Turan_Method(self):
        self.write_txt_On_Off_Button_State(self.button_use_turan,27,'use_turan')

    def go_Manual_Long(self):
        manual_lock = self.txt_ops.quick_write_txt_file('txt/settings/manual_lock.txt',1)
        self.replace_Pair_Settings_Line(12,'manual_trigger_long=1')

    def go_Manual_Short(self):
        manual_lock = self.txt_ops.quick_write_txt_file('txt/settings/manual_lock.txt',1)
        self.replace_Pair_Settings_Line(13,'manual_trigger_short=1')

  
    def count_Global_PNL(self):

        all_files_exist = 0
        final_pnl = 0
        final_wins = 0
        final_losses = 0
        final_win_events = 0
        final_loss_events = 0

        #make sure all files exist:
        if exists('txt/data/for_perf/final_pnl.txt') == True and exists('txt/data/for_perf/final_losses.txt') == True and\
           exists('txt/data/for_perf/final_wins.txt') == True and exists('txt/data/for_perf/final_win_events.txt') == True and\
           exists('txt/data/for_perf/final_loss_events.txt') == True:

            all_files_exist = 1

            final_pnl = float("%.2f"%(float(self.txt_ops.quick_read_txt_file('txt/data/for_perf/final_pnl.txt'))))
            final_wins = float("%.2f"%(float(self.txt_ops.quick_read_txt_file('txt/data/for_perf/final_wins.txt'))))
            final_losses = float("%.2f"%(float(self.txt_ops.quick_read_txt_file('txt/data/for_perf/final_losses.txt'))))
            final_win_events = float("%.2f"%(float(self.txt_ops.quick_read_txt_file('txt/data/for_perf/final_win_events.txt'))))
            final_loss_events = float("%.2f"%(float(self.txt_ops.quick_read_txt_file('txt/data/for_perf/final_loss_events.txt'))))

        if self.first_run == False:

            if all_files_exist == 1:

                self.data_label_dash_global_difference.setText(str(final_pnl))
                self.data_label_dash_global_losses_amount.setText(str(final_losses))
                self.data_label_dash_global_wins_amount.setText(str(final_wins))
                win_loss_ratio_str = str(int(final_win_events)) + ':' + str(int(final_loss_events))
                self.data_label_dash_global_ratio_event.setText(win_loss_ratio_str)

                if final_losses != 0:
                    ratio = float("%.2f"%(float(final_wins / final_losses)))
                    ratio = abs(ratio)
                    ratio_str = str(ratio) + ":1"
                    self.data_label_dash_global_ratio.setText(ratio_str)

            else:
                self.data_label_dash_global_difference.setText('n/a')
                self.data_label_dash_global_losses_amount.setText('n/a')
                self.data_label_dash_global_wins_amount.setText('n/a')
                self.data_label_dash_global_ratio_event.setText('n/a')
                self.data_label_dash_global_ratio.setText('n/a')
                    
       


                    



    def sum_All_Balances(self):

        try:

            total_balance = 0
            total_margin = 0
            diff = 0
            
            if self.first_run == False:

                balance_array = []
                margin_array = []
                
                account_num = self.maths_functions.count_Files('txt/login/')[0]


                print("\nTotal number of Account tabs:",account_num)

                for i in range(account_num):

                    balance_functions = Balance_Functions(i+1)
                    get_balances = balance_functions.read_Futures_Balances()

                    if get_balances[0] != '':
                        balance_array.append(float(get_balances[0]))

                    if get_balances[1] != '':
                        margin_array.append(float(get_balances[1]))
                        
                    total_balance = float("%.2f"%(sum(balance_array)))
                    total_margin = float("%.2f"%(sum(margin_array)))
                    diff = float("%.2f"%(total_margin-total_balance))


                self.data_label_dash_balances_total.setText(str(  float("%.2f"%(total_balance)  )))
                self.data_label_dash_margins_total.setText(str(float("%.2f"%(total_margin))))
                self.data_label_dash_pnl_total.setText(str(diff))

        except:

            print("\nSum Balances Error.")

        return total_balance,total_margin


    def use_Market_Order(self):
        if self.button_market.isChecked() == True: 
            self.replace_Pair_Settings_Line(9,'is_limit_entry=0')
            self.data_label_entry_bid.setEnabled(False)
            self.data_label_post_bids.setEnabled(False)
        else:
            self.button_market.toggle()

        if self.button_limit.isChecked() == True:
            self.button_limit.toggle()


    def use_Limit_Order(self):
        if self.button_limit.isChecked() == True: 
            self.replace_Pair_Settings_Line(9,'is_limit_entry=1')
            self.data_label_entry_bid.setEnabled(True)
            self.data_label_post_bids.setEnabled(True)
        else:
            self.button_limit.toggle()
        if self.button_market.isChecked() == True:
            self.button_market.toggle()


    def use_Dynamic_TP(self):


        if self.dynamic_tp.isChecked() == True: 

            print("\nUse Dynamic TP button checked.")
            self.write_txt_On_Off_Button_State(self.dynamic_tp,20,'dynamic_tp')
            self.data_label_tp_setting.setEnabled(False)

            self.replace_Pair_Settings_Line(20,'dynamic_tp=1')

        elif self.dynamic_tp.isChecked() == False:

            print("\nUse Dynamic TP button unchecked.")

            self.data_label_tp_setting.setEnabled(True)
            self.replace_Pair_Settings_Line(20,'dynamic_tp=0')






    def use_Dynamic_SL(self):

        if self.dynamic_sl.isChecked() == True: 

            print("\nUse Dynamic SL button checked.")
            #
            self.write_txt_On_Off_Button_State(self.dynamic_sl,28,'dynamic_sl')
            self.data_label_sl_setting.setEnabled(False)
            self.replace_Pair_Settings_Line(28,'dynamic_sl=1')

        elif self.dynamic_sl.isChecked() == False: 
            print("\nUse Dynamic SL button unchecked.")
            self.data_label_sl_setting.setEnabled(True)
            self.replace_Pair_Settings_Line(28,'dynamic_sl=0')


        if self.button_sl_liq_setting.isChecked() == True:
            self.button_sl_liq_setting.toggle()
            self.replace_Pair_Settings_Line(19,'use_liq_sl=0')




    def use_Liq_SL(self):
        
        if self.button_sl_liq_setting.isChecked() == True: 

            print("\nUse Liq SL button checked.")
            #
            self.write_txt_On_Off_Button_State(self.button_sl_liq_setting,24,'use_liq_sl')
            self.data_label_sl_setting.setEnabled(False)
            self.replace_Pair_Settings_Line(19,'use_liq_sl=1')

        elif self.button_sl_liq_setting.isChecked() == False: 
            print("\nUse Liq SL button unchecked.")
            self.data_label_sl_setting.setEnabled(True)
            self.replace_Pair_Settings_Line(19,'use_liq_sl=0')

        if self.dynamic_sl.isChecked() == True:
            self.dynamic_sl.toggle()
            self.replace_Pair_Settings_Line(28,'dynamic_sl=0')


########################## DYNAMIC UPDATE ########################################################################

    def calc_Color(self,input_value):
        if input_value < 0:
            pnl_color = 'red'
        else:
            pnl_color = 'green'
        return pnl_color

    def get_Balances(self):
        balance=0
        margin=0
        spot_balance=0
        pnl_value=0
        pnl_value_pos_str = ''
        pnl_value_pos = 0
        balance_functions = Balance_Functions(self.current_tab_id)
        get_balances = balance_functions.read_Futures_Balances()
        if len(get_balances) > 0:
            balance = float("%.2f"%(float(get_balances[0])))
            margin = float("%.2f"%(float(get_balances[1])))
            risk_ratio = float("%.2f"%(balance/margin))
            spot_balance = float("%.2f"%(float(get_balances[2])))
            pnl_value = float(margin) - float(balance)
            pnl_value = float("%.2f"%(float(pnl_value)))
            pnl_value_pos_str = self.txt_ops.quick_read_txt_file('txt/auto_data/pos_pnl/pos_pnl.txt')
            pnl_value_pos = float("%.2f"%(float(pnl_value_pos_str)))
        #set texts
        self.data_label_balance.setText(str(balance))
        self.data_label_margin.setText(str(margin))
        self.data_label_spot_usdt_balance.setText(str(spot_balance))
        self.data_label_PNL.setText(str(pnl_value))
        self.data_label_PNL_pos.setText(pnl_value_pos_str)
        self.data_label_risk_ratio.setText(str(risk_ratio))
        #set PNL style
        create_style_string = "color:grey;"
        self.data_label_PNL.setStyleSheet(create_style_string)
        #set PNL_POS style
        create_style_string_pos = "color:" + (   self.calc_Color(pnl_value_pos)    ) + ";"
        self.data_label_PNL_pos.setStyleSheet(create_style_string_pos)
        #set leverage tooltip to show correct amount
        settings = Settings(self.current_tab_id)
        read_requested_value = int(settings.load_Trade_Variables(self.combo_symbols.currentText())[38])
        make_x_string = str(read_requested_value) + 'x Leverage.<br>'
        self.lev_Slider.setToolTip(make_x_string)



    def get_Deposit_Address(self):
        pass


    def get_Positions(self):

        #local vars
        filtered_pos_array = []
        liq_price = 0
        pos_string = ''
        warning_range = 90
        to_liq = 0
        to_go = 0
        to_go_str = '0'
        pair_symbol = ''
        pos_side = ''
        pos_entry_str = ''
        liq_price_str = '0'
        current_price = 0
        create_style = ''
        price_style = "color:grey;"

        self.current_pair_selected = self.combo_symbols.currentText()

        #set text
        self.data_label_liq_price.setText('')
        self.data_label_current_price.setText('')
        self.data_label_current_price.setText('')

        #always get current price for tab asset
        current_price_str = self.txt_ops.quick_read_txt_file('txt/tab_data/prices/price_average.txt')
        print("\ncurrent_price_str:",current_price_str)

        #>>>SET TEXT
        self.data_label_current_price.setText(current_price_str)

        #analyze signals
        file_path_long = 'txt/mode/recommends/' + self.current_pair_selected + '_LONG.txt'
        file_path_short = 'txt/mode/recommends/' + self.current_pair_selected + '_SHORT.txt'
        read_long_status = self.txt_ops.quick_read_txt_file(file_path_long)
        read_short_status = self.txt_ops.quick_read_txt_file(file_path_short)

        if read_long_status == 'SAFE':
            price_style = "color:green;"
        elif read_short_status == 'SAFE':
            price_style = "color:red;"

        #style
        self.data_label_current_price.setStyleSheet(price_style)


        #get number of positions
        order_pos_functions = Order_Pos_Functions(self.current_tab_id)
        pos_array = order_pos_functions.read_Position_Data()
        #print('\nReading position array:',pos_array)
        no_of_positions = len(pos_array)

        if no_of_positions == 0:
            self.header_positions.setText("Positions")

        if no_of_positions > 0:

            for i in range(no_of_positions):

                #set text
                self.header_positions.setText("Positions (" + str(no_of_positions) + ")")

                #filter string
                pair_symbol = str(pos_array[i][0])

                precision_functions = Precision_Functions(1)
                try:
                    price_prec_str = "%." + str( precision_functions.read_Asset_Precision(pair_symbol)[0] ) + "f"
                except:
                    price_prec_str = "%." + str( precision_functions.request_Asset_Precision(pair_symbol)[0] ) + "f"


                
                pos_side = str(pos_array[i][3])
                self.tab_position_side = pos_side
                pos_entry_str = str(float(price_prec_str%(float(pos_array[i][2]))     ))
                pos_string = pos_side[0] + ' ' + str(pos_array[i][1]) + ' ' +\
                pair_symbol.replace('USDT','') + ' @ ' + pos_entry_str

                #append filtered string
                filtered_pos_array.append(pos_string)

                #for another data field
                if self.filter_Combo_Positions_Pair_Symbol() == pair_symbol:

                    liq_price_str = str(float(price_prec_str%(float(pos_array[i][4]))))
                    print("Liquidation price string:",liq_price_str)

                    try:
                        liq_price = float(liq_price_str)
                    except:
                        liq_price = 0

                    try:
                        current_price = float(current_price_str)
                    except:
                        current_price = 0
                    


                    if liq_price > 0 and current_price > 0:

                        #calculate percentage of progress to liq price from current
                        if pos_side == 'SHORT':
                            to_go = round((current_price * 100) / liq_price)
                        elif pos_side == 'LONG':
                            to_go = round((liq_price * 100) / current_price)

                        #color depending on progress
                        if to_go > warning_range:
                            create_style = "color:" + ("red") + ";"
                            print("\n\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
                            print("\nWarning: Account Liquidation imminent!")
                            print("\n\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
                        else:
                            create_style = "color:" + ("grey") + ";"

                        #formatting
                        if to_go < 0.1 or to_go > 100:
                            to_go_str = '...'
                            create_style = "color:" + ("grey") + ";"
                        else:
                            to_go_str = str(to_go) + '%'

                    self.data_label_liq_progress.setStyleSheet(create_style)
                    self.data_label_liq_price.setText(liq_price_str)
                    self.data_label_liq_price.setStyleSheet(create_style)
                    self.data_label_liq_progress.setText(to_go_str)



    def get_Orders(self):
        self.current_tab_id = int(self.master_Tabs_Container.currentIndex())
        pair_symbol = self.filter_Combo_Positions_Pair_Symbol()
        if pair_symbol != '':
            order_pos_functions = Order_Pos_Functions(self.current_tab_id)
            total_orders_num = len(order_pos_functions.read_Open_Orders_Data())
            get_proc_orders_data = order_pos_functions.process_Open_Orders_Data(pair_symbol) #process_Open_Orders_Data(tab_index)
            open_orders_num = int(get_proc_orders_data[0])
            if open_orders_num == 0:
                self.header_linked_orders.setText("Linked orders")
                self.data_label_order_tp.setText('')
                self.data_label_order_sl.setText('')
                self.data_label_entry.setText('')

                #Entry
                #self.data_label_entry.setText(make_entry_order_string)
                #create_entry_style_string = "color:" + ("orange") + ";"
                #self.data_label_entry.setStyleSheet(create_entry_style_string)
                
            #if there are orders, sort them
            elif open_orders_num > 0:
                #refresh header text
                self.header_linked_orders.setText("Linked orders (" + str(open_orders_num) + "/" + str(total_orders_num) + ")")
                #get premade strings from the process orders function
                make_tp_string = str(get_proc_orders_data[1])
                make_sl_string = str(get_proc_orders_data[2])
                make_entry_order_string = str(get_proc_orders_data[3])
                #set data text labels -------------------------------
                self.data_label_order_tp.setText(make_tp_string)
                create_tp_style_string = "color:" + ("green") + ";"
                self.data_label_order_tp.setStyleSheet(create_tp_style_string)
                #SL
                self.data_label_order_sl.setText(make_sl_string)
                create_sl_style_string = "color:" + ("red") + ";"
                self.data_label_order_sl.setStyleSheet(create_sl_style_string)
                #Entry
                self.data_label_entry.setText(order_pos_functions.check_Symbol_Entering())
                create_entry_style_string = "color:" + ("orange") + ";"
                self.data_label_entry.setStyleSheet(create_entry_style_string)


    def update_Dynamic_Labels(self):
        
        if self.tab_type == 'Accounts':

            try:
                self.get_Balances()
            except:
                print("\nError: self.get_Balances()")

            try:
                self.get_Positions()
            except:
                print("\nError: self.get_Positions()")

            try:
                self.set_Positions_Combo_Item_Color()
            except:
                print("\nError: self.set_Positions_Combo_Item_Color()")

            try:
                self.get_Orders()
            except:
                print("\nError: self.get_Orders()")

            #self.style_All_Tabs() 


########################## END DYNAMIC UPDATE ########################################################################



    def popup_Withdraw(self):
        
        read_value_addy = str(self.txt_ops.quick_read_txt_file('txt/withdraw_address_USDT.txt'))
        read_value_symbol = str(self.txt_ops.quick_read_txt_file('txt/withdraw_symbol.txt'))
        read_value_memo = str(self.txt_ops.quick_read_txt_file('txt/withdraw_memo.txt'))
        read_value_network = str(self.txt_ops.quick_read_txt_file('txt/withdraw_network.txt'))
        
        def apply_Method(Dialog,to_address,symbol,memo,network):

            print("\nApply clicked.")
            
            write_value_a = self.txt_ops.quick_write_txt_file('txt/withdraw_address_USDT.txt',to_address)
            write_value_b = self.txt_ops.quick_write_txt_file('txt/withdraw_symbol.txt',symbol)
            write_value_c = self.txt_ops.quick_write_txt_file('txt/withdraw_memo.txt',memo)
            write_value_d = self.txt_ops.quick_write_txt_file('txt/withdraw_network.txt',network)
            
            self.my_Withdraw(to_address,symbol,memo,network)

            Dialog.close()

        def cancel_Method(Dialog):

            print("\nCancel clicked.")
            
            Dialog.close()

        to_address_dialog = QDialog(self)

        #Window settings
        to_address_dialog.setWindowTitle(" Withdrawals Manager")
        to_address_dialog.resize(392, 180)

        #PLAIN LABEL - ASSET TYPE
        label_asset_type = QtWidgets.QLabel(to_address_dialog)
        label_asset_type.setGeometry(QtCore.QRect(30,20,60,20))
        label_asset_type.setObjectName("label_asset_type")
        label_asset_type.setText("Symbol")
        #DATA LABEL - ASSET TYPE
        data_label_asset_type = QtWidgets.QLineEdit(to_address_dialog)
        data_label_asset_type.setGeometry(QtCore.QRect(80,20,60,20))
        data_label_asset_type.setObjectName("data_label_asset_type")
        data_label_asset_type.setText(read_value_symbol)

        #PLAIN LABEL - BUFFER
        label_to_address = QtWidgets.QLabel(to_address_dialog)
        label_to_address.setGeometry(QtCore.QRect(30,50,110,20))
        label_to_address.setObjectName("label_to_address")
        label_to_address.setText("Address")
        #DATA LABEL - BUFFER
        data_label_to_address = QtWidgets.QLineEdit(to_address_dialog)
        data_label_to_address.setGeometry(QtCore.QRect(80,50,280,20))
        data_label_to_address.setObjectName("data_label_to_address")
        data_label_to_address.setText(read_value_addy)

        #PLAIN LABEL - BUFFER
        label_memo = QtWidgets.QLabel(to_address_dialog)
        label_memo.setGeometry(QtCore.QRect(30,80,110,20))
        label_memo.setObjectName("label_memo")
        label_memo.setText("Memo")
        #DATA LABEL - BUFFER
        data_label_memo = QtWidgets.QLineEdit(to_address_dialog)
        data_label_memo.setGeometry(QtCore.QRect(80,80,280,20))
        data_label_memo.setObjectName("data_label_memo")
        data_label_memo.setText(read_value_memo)

        #PLAIN LABEL - BUFFER
        label_network = QtWidgets.QLabel(to_address_dialog)
        label_network.setGeometry(QtCore.QRect(30,110,110,20))
        label_network.setObjectName("label_network")
        label_network.setText("Network")
        #DATA LABEL - BUFFER
        data_label_network = QtWidgets.QLineEdit(to_address_dialog)
        data_label_network.setGeometry(QtCore.QRect(80,110,280,20))
        data_label_network.setObjectName("data_label_network")
        data_label_network.setText(read_value_network)

        #BUTTON - APPLY
        button_apply = QtWidgets.QPushButton(to_address_dialog)
        button_apply.setGeometry(QtCore.QRect(90,145,70,20))
        button_apply.setObjectName("button_apply")
        button_apply.setText("Withdraw")
        button_apply.clicked.connect(lambda:apply_Method(to_address_dialog,str( data_label_to_address.text()),str( data_label_asset_type.text()),\
                                                        str(data_label_memo.text()),str( data_label_network.text())))
        #BUTTON - CANCEL
        button_cancel = QtWidgets.QPushButton(to_address_dialog)
        button_cancel.setGeometry(QtCore.QRect(230,145,70,20))
        button_cancel.setObjectName("button_cancel")
        button_cancel.setText("Cancel")
        button_cancel.clicked.connect(lambda:cancel_Method(to_address_dialog))
        to_address_dialog.exec_()


    def update_Pos_Combo(self):      
        filtered_pos_array = []
        if self.current_tab_id > 0:
            order_pos_functions = Order_Pos_Functions(self.current_tab_id)
            pos_array = order_pos_functions.read_Position_Data()
            no_of_positions = len(pos_array)
            if no_of_positions > 0:
                for i in range(no_of_positions):
                    pair_symbol = str(pos_array[i][0])
                    precision_functions = Precision_Functions(1)
                    try:
                        prec_str = "%." + str(precision_functions.read_Asset_Precision(pair_symbol)[0]) + "f"
                    except:
                        prec_str = "%." + str(precision_functions.request_Asset_Precision(pair_symbol)[0]) + "f"
                    pos_side = str(pos_array[i][3])
                    pos_entry_str = str(float(prec_str%(float(pos_array[i][2]))))
                    pos_string = pos_side[0] + ' ' + str(pos_array[i][1]) + ' ' +\
                    pair_symbol.replace('USDT','') + ' @ ' + pos_entry_str
                    filtered_pos_array.append(pos_string)
        self.combo_positions.clear()
        self.combo_positions.addItems(filtered_pos_array)


    def read_Leverage_Slider_Value(self):
        try:
            settings = Settings(self.current_tab_id)
            read_req_value = settings.load_Trade_Variables(self.combo_symbols.currentText())[38]
            self.lev_Slider.setValue(read_req_value)
            string_x = str(read_req_value) + 'x'
            self.data_label_lev.clear()
            self.data_label_lev.setText(string_x)
        except:
            self.data_label_lev.setText('...')
        

    def set_Tab_Text_Color(self,index,clr):
        self.master_Tabs_Container.tabBar().setTabTextColor(index,clr)


    def style_All_Tabs(self):

        #set tab text colors
        account_numbers = []
        main_clr = QtGui.QColor()
        main_clr.setRgb(0,0,0)

        for i in range(self.number_of_tabs):
            account_numbers.append(i)

        account_numbers.pop(0)
        account_numbers.pop(-1)

        for j in range(len(account_numbers)):
            try:
                read_pos = read_Position_Data_For_Combo(j+1)
                length = len(read_pos)
                if length > 0:
                    read_pos_side = read_pos[-1][3]
                    if read_pos_side == 'LONG':
                        main_clr.setRgb(18, 200, 110) #green
                    elif read_pos_side == 'SHORT':
                        main_clr.setRgb(255, 32, 69) #red
                else:
                    main_clr.setRgb(0, 0, 0) #black
                self.set_Tab_Text_Color(j+1,main_clr)
            except:
                pass


    def on_Combo_Symbols_Changed(self):

        print("\nPair symbol in combobox changed.")

        make_str = 'txt/setup/' + str(self.current_tab_id) + '/setup_' + str(self.current_tab_id) + '.txt'

        pair_symbol = self.combo_symbols.currentText()

        string_val = "last_combo_settings=" + pair_symbol

        self.txt_ops.replace_Specific_Line(make_str,5,string_val)
      
        self.read_Leverage_Slider_Value()
        self.read_Display_Current_Text_Settings()
        self.load_Button_Latch_States_Accounts()



    def on_Combo_Positions_Changed(self):
        pair_symbol = ''
        if self.current_tab_id > 0:
            make_str = 'txt/setup/' + str(self.current_tab_id) + '/setup_' + str(self.current_tab_id) + '.txt'
            pair_symbol = self.filter_Combo_Positions_Pair_Symbol()
            string_val = "last_combo_pos=" + pair_symbol
            self.txt_ops.replace_Specific_Line(make_str,4,string_val)

            
    def analyze_Stats_Data_Write(self):
        a = Record_Stats(1)
        d = a.analyze_Log_Folder()


    def on_Tab_Change(self):

        #clear liq/current/progress
        self.data_label_liq_price.setText('')
        self.data_label_current_price.setText('')
        self.data_label_liq_progress.setText('')
        
        #read/write tab index ops
        self.current_tab_id = int(self.master_Tabs_Container.currentIndex())
        self.txt_ops.quick_write_txt_file('txt/tab_account.txt',self.current_tab_id)

        if self.current_tab_id not in self.tabs_looked_at:
            self.tabs_looked_at.append(self.current_tab_id)
            print("\nself.tabs_looked_at",self.tabs_looked_at)
        
        self.number_of_tabs = int(self.master_Tabs_Container.count())

        if self.current_tab_id == 0:
            self.tab_type = 'Dashboard'
            print("\nTab type |",self.tab_type)
            self.sum_All_Balances()

            try:
                self.analyze_Stats_Data_Write()
            except:
                pass
            
            self.count_Global_PNL()
            self.load_Button_Latch_States_Dashboard()
            self.configure_Dashboard_UI()

        elif self.current_tab_id == (self.number_of_tabs - 1):
            self.tab_type = 'Plus'
            print("\nTab type |",self.tab_type)
            self.configure_Plus_UI()

        else:
            self.tab_type = 'Accounts'
            print("\nTab type |",self.tab_type)
            self.txt_ops.quick_write_txt_file('txt/last_tab_account.txt',self.current_tab_id)

            #clear all dynamic data labels
            self.header_positions.setText("Positions")
            self.combo_positions.clear()
            self.data_label_liq_price.setText(' ... ')
            self.data_label_current_price.setText(' ... ')
            self.header_linked_orders.setText("Linked orders")
            self.data_label_order_tp.setText('')
            self.data_label_order_sl.setText('')
            self.data_label_entry.setText('')
            self.configure_Accounts_UI()
            self.read_Display_Current_Text_Settings()
            self.load_Button_Latch_States_Accounts()
            self.update_Dynamic_Labels()

            #read leverage
            self.read_Leverage_Slider_Value()

            try:
                account_no = int(self.current_tab_id)
                get_account_settings = Settings(account_no).load_Account_Variables()
                last_combo_pos = get_account_settings[4]
                pair_symbol = str(last_combo_pos)
                index = self.combo_symbols.findText(pair_symbol,QtCore.Qt.MatchFixedString)
                if index >= 0:
                     self.combo_symbols.setCurrentIndex(index)
            except:
                pass

            self.update_Pos_Combo()


    def run_Timer(self):
        self.Timer = QtCore.QTimer(self)
        self.Timer.timeout.connect(self.update_Dynamic_Labels)
        self.Timer.start(self.refresh_ms)


if __name__ == '__main__':

    app = QApplication(['Omicron 2.0'])
    w = Window()
    #
    w.configure_Plus_UI()
    w.create_Default_Files_Man()
    #
    #w.analyze_Stats_Data_Write()
    w.count_Global_PNL()
    w.sum_All_Balances()
    w.load_Button_Latch_States_Dashboard()
    w.configure_Dashboard_UI()
    #
    w.check_Updates()
    #
    w.run_Timer()
    #
    w.show()
    #
    sys.exit(app.exec_())







