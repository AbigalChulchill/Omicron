import sys
sys.path.insert(1,'lib')
import email,imaplib
from _txt_Ops import *
from _csv_Ops import *
#from _Email_Signals import *
from _Maths_Functions import *
from _Price_Functions import *
from _Fetch_Settings import *
from _Time_Functions import *
from _Order_Pos_Functions import *
from _Encryptor import *

class Signals():

    def __init__(self,account_no):
        #super().__init__()
        self.account_no = account_no 
        self.txt_ops = txt_Ops()
        self.csv_ops = csv_Ops()
        self.maths_functions = Maths_Functions(account_no)
        self.price_functions = Price_Functions(account_no)
        self.time_functions = Time_Functions()
        self.settings = Settings(account_no)
        #self.order_pos_functions = Order_Pos_Functions(account_no)


    def find_Top_Bottom_Lines(self,pair_symbol,input_array):
        top_line = 0
        bottom_line = 0
        get_gold_silver = self.maths_functions.calc_Gold_Silver(pair_symbol,input_array)
        gold = get_gold_silver[0]
        silver = get_gold_silver[1]
        if gold >= silver:
            top_line = gold
            bottom_line = silver
        elif gold < silver:
            top_line = silver
            bottom_line = gold

        print("\nTop region is:",top_line)
        print("Bottom region is:",bottom_line)
        return gold,silver,top_line,bottom_line

        




    def mode_Safety(self,pair_symbol,pos_side):

        print('\n┌--------------------------- SIGNALS | MODE SAFETY ---------------------------┐\n')

        #local vars
        status = 'NONE'
        diff = 0
        min_scalp = 0
        target = 0
        gold = 0
        silver = 0
        top_line = 0
        bottom_line = 0
        algo_type = ''
        percentage_min_scalp = 0
        time_back_mins = int(self.txt_ops.quick_read_txt_file('txt/settings/mode/mode_back.txt'))

        #dict
        init_dict = {}
        folder_path = 'txt/setup/' + str(self.account_no) + '/'
        make_str = folder_path + 'setup_' + str(self.account_no) + '_' + pair_symbol + '.txt'
        init_dict = self.txt_ops.create_dict_from_txt(make_str,'=')

        #fetch klines
        get_all_klines_data = self.price_functions.request_Klines(pair_symbol,time_back_mins)

        if len(get_all_klines_data) > 0:
            
            all_klines_array = get_all_klines_data[0]

            get_gold_silver = self.find_Top_Bottom_Lines(pair_symbol,all_klines_array)

            gold = get_gold_silver[0]
            silver = get_gold_silver[1]
            top_line = get_gold_silver[2]
            bottom_line = get_gold_silver[3]

            print("\nMode Safety values [gold,silver,top,bottom]:",gold,silver,top_line,bottom_line)

            #get current price  
            get_price_data = self.price_functions.request_Price_Data(pair_symbol)
            current_price = get_price_data[0]
            print(pair_symbol,"current price:",current_price)

            #calculate min scalp or distance required from bands
            try:
                algo_type = str(list(init_dict.values())[28])
                percentage_min_scalp = float(list(init_dict.values())[29])
            except:
                print("\nError: List index out of range, skipping...")
            
            min_scalp = current_price * (percentage_min_scalp / 100) 

            if pos_side == 'LONG':

                if algo_type == 'EITHER':
                    target = top_line - min_scalp

                if algo_type == 'GOLD':
                    target = gold - min_scalp

                if algo_type == 'SILVER':
                    target = silver - min_scalp
                        
                if algo_type == 'BOTH':
                    target = bottom_line - min_scalp

                #diff is for stats report reason only
                if target != 0:
                    diff = (current_price * 100) / target
                    diff = diff - 100
                    diff = float("%.2f"%(diff))

                if current_price < target:
                    status = 'SAFE'
                else:
                    status = 'UNSAFE'

            if pos_side == 'SHORT':

                if algo_type == 'EITHER':
                    target = bottom_line + min_scalp

                if algo_type == 'GOLD':
                    target = gold + min_scalp

                if algo_type == 'SILVER':
                    target = silver + min_scalp

                if algo_type == 'BOTH':
                    target = top_line + min_scalp

                #diff is for stats report reason only
                diff = (current_price * 100) / target
                diff = 100 - diff
                diff = float("%.2f"%(diff))
                
                if current_price > target:
                    status = 'SAFE'
                else:
                    status = 'UNSAFE'

            print("\nSide:",pos_side,"| Status:",status,"| Difference:",str(diff))

        print('\n\n└------------------------- SIGNALS | END MODE SAFETY -------------------------┘\n\n')
        return status,target,diff,min_scalp,top_line,bottom_line




    def simple_Mode_Safety(self,pair_symbol,pos_side):

        time_back_mins = int(self.txt_ops.quick_read_txt_file('txt/settings/mode/mode_back.txt'))
        status = 'NONE'
        gold = 0

        get_all_klines_data = self.price_functions.request_Klines(pair_symbol,time_back_mins)

        if len(get_all_klines_data) > 0:
            
            all_klines_array = get_all_klines_data[0]
            get_gold_silver = self.find_Top_Bottom_Lines(pair_symbol,all_klines_array)
            gold = get_gold_silver[0]
 
            get_price_data = self.price_functions.request_Price_Data(pair_symbol)
            current_price = get_price_data[0]
   
            if pos_side == 'LONG':
                if current_price < gold:
                    status = 'SAFE'
                else:
                    status = 'UNSAFE'

            if pos_side == 'SHORT':
                if current_price > gold:
                    status = 'SAFE'
                else:
                    status = 'UNSAFE'

            file_path = 'txt/mode/recommends/' + pair_symbol + '_' + pos_side + '.txt'

            write_val = self.txt_ops.quick_write_txt_file_plus(file_path,status)

        return status





    def spread_Safety(self,pair_symbol,input_entry_side,input_enter_price):

   
        print("\n")
        print("\\\\ Spread Safety | Start Report \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
        print("\n")
        print("Spread Safety | Analyzing for:",pair_symbol,input_entry_side,input_enter_price)
        
        #vars
        status = ''
        entry_price = 0
        entry_side = ''
        entry_symbol = ''
        spread_value = int(self.txt_ops.quick_read_txt_file('txt/settings/spread/spread_value.txt'))
        print("\nSpread Safety | Spread value is: $" + str(spread_value))
        login_count = self.maths_functions.count_Files('txt/login/')[0]
        print("\nSpread Safety | Number of Accounts:",login_count)

        #price_difference = 0
        #price_difference_abs = 0


        

        for i in range(login_count):

            order_pos_functions = Order_Pos_Functions(i+1)
            get_pos_data = order_pos_functions.read_Position_Data()

            if len(get_pos_data) > 0:

                print("\nSpread Safety | Pulling position data for Account:",i+1)

                entry_symbol = get_pos_data[-1][0]
                print("--Entry Symbol:",entry_symbol)

                entry_price = get_pos_data[-1][2]
                print("--Entry Price:",entry_price)

                entry_side = get_pos_data[-1][3]
                print("--Entry Side:",entry_side)


                price_difference = float(entry_price) - input_enter_price
                price_difference_abs = abs(price_difference)
                #i.e. LONG entry price was 3400, current price is 3500 = -100
                #if long this value will be negative if price rose above entry / short pos
                print("--Distance:",price_difference)

                
                
                if (pair_symbol == entry_symbol) and (input_entry_side == entry_side) and (price_difference_abs < spread_value):
                    status = 'UNSAFE'
                    break #once it finds any match, breaks out loop
                #elif entry_side == 'LONG' and price_difference < 0:
                    #status = 'UNSAFE'
                    #break 
                #elif entry_side == 'SHORT' and price_difference > 0:
                    #status = 'UNSAFE'
                    #break
                else:
                    status = 'SAFE'

        if status == 'SAFE':
            print("\nNo spread matches found.")
        elif status == 'UNSAFE':
            print("\nA",entry_side,"entered at",entry_price,"exists.\n--Difference:",price_difference,price_difference_abs)




            
        return status




    def connect_Read_Email_Title(self,pair_symbol,timeframe,signal_type):
        email_addy = self.txt_ops.quick_read_txt_file('txt/settings/email/account/email.txt')
        get_email_pass = self.txt_ops.quick_read_txt_file('txt/settings/email/account/app_pass.txt')

        if email_addy == 'haas.alerts.email@gmail.com':
            e = Encryptor()
            email_pass = e.decrypt_Bytes_As_String(get_email_pass)
        else:
            email_pass = get_email_pass

        email_imap = 'imap.gmail.com'
        environment = 'NONE'
        unix_time = 0
        last_signal_side = ''
        switch_over_time = ''
        switch_over_time_real = ''
        while True:
            mail = imaplib.IMAP4_SSL(email_imap)
            r, d = mail.login(email_addy,email_pass)
            assert r == 'OK', 'login failed'
            mail.list()
            mail.select("inbox")
            middle_string = str('"%s"'%(signal_type + ' ' + pair_symbol + ' ' + timeframe))
            make_string = "(SUBJECT " + middle_string + ")"
            result,data = mail.search(None,str(make_string))
            ids = data[0]
            id_list = ids.split()
            length_matches = len(id_list)
            if length_matches > 0:
                def return_Time_And_Subject(id_index):
                    side = ''
                    curr_email_id = id_list[id_index]
                    result, data = mail.fetch(curr_email_id, "(RFC822)")
                    raw_email = data[0][1].decode('utf-8')
                    read_email_title = str(raw_email)
                    msg = email.message_from_string(raw_email)
                    unix_timestamp_str = msg['X-Received']
                    chars_before_symbol = self.txt_ops.find_Chars_Before_Symbol(unix_timestamp_str,';',13)
                    unix_time = int(str(chars_before_symbol)[0:10])
                    real_time = self.time_functions.convert_Time(unix_time)
                    subject = str(msg['Subject'])
                    if subject.find('LONG') > 0:
                        side = 'LONG'
                    else:
                        side = 'SHORT'
                    return unix_time,real_time,side
                get_last_signal_data = return_Time_And_Subject(-1)
                last_signal_unix_time = get_last_signal_data[0]
                last_signal_real_time = get_last_signal_data[1]
                last_signal_side = get_last_signal_data[2]
                print('┌--------------------------------------------┐')
                print('\n Last signal data for:\n',pair_symbol,timeframe,signal_type,'\n',last_signal_unix_time,last_signal_real_time,last_signal_side)
                print('\n└--------------------------------------------┘')
                for i in reversed(id_list):
                    index = id_list.index(i)
                    get_data = return_Time_And_Subject(index)
                    curr_unix_time = get_data[0]
                    curr_real_time = get_data[1]
                    curr_side = get_data[2]
                    if curr_side == last_signal_side:
                        print('\n\n\nEmail ID:',i,"Sent:",curr_real_time,"Side:",curr_side)
                        switch_over_time = curr_unix_time
                        switch_over_time_real = curr_real_time
                    else:
                        break
                print('\n')
                print('\n┌--------------------------------------------┐')
                print('\n Oldest Email in chain:\n',switch_over_time,switch_over_time_real,last_signal_side)
                print('\n└--------------------------------------------┘\n')
                if last_signal_side == 'SHORT':
                    environment = 'BEARISH'
                if last_signal_side == 'LONG':
                    environment = 'BULLISH'
            mail.logout()
            break
        return environment,switch_over_time









    def check_Email_Signal(self,pair_symbol,entry_side,timeframe,signal_type):
        print('\n┌-------------------------- SIGNALS | EMAIL MANAGER --------------------------┐')
        status = 'UNSAFE'
        environment = 'NONE'
        unix_time = 0
        stale_mins_3m = float(self.txt_ops.quick_read_txt_file('txt/settings/email/3m_stale_mins.txt'))
        stale_mins_4h = float(self.txt_ops.quick_read_txt_file('txt/settings/email/4h_stale_mins.txt'))

        email_addy = self.txt_ops.quick_read_txt_file('txt/settings/email/account/email.txt')
        get_email_pass = self.txt_ops.quick_read_txt_file('txt/settings/email/account/app_pass.txt')

        if email_addy == 'haas.alerts.email@gmail.com':
            e = Encryptor()
            email_pass = e.decrypt_Bytes_As_String(get_email_pass)
        else:
            email_pass = get_email_pass



        email_imap = 'imap.gmail.com'
        print('\n\nAttempting Email connection...\n\n')
        grab_data = self.connect_Read_Email_Title(pair_symbol,timeframe,signal_type)
        print(grab_data)
        environment = str(grab_data[0])
        unix_time = int(grab_data[1])
        current_unix_time = int(time.time())
        email_unix_time = unix_time
        diff_mins = int((current_unix_time - email_unix_time) / 60)
        print('\nOldest Email in chain was sent',diff_mins,"minutes ago...\n")

        if (timeframe == '3m' and diff_mins >= stale_mins_3m):
            print('\n* 3m signal older than ' + str(stale_mins_3m) + ' minutes (STALE), ignoring... *\n')
        if (timeframe == '3m' and diff_mins < stale_mins_3m) and entry_side == 'LONG' and environment == 'BULLISH':
            status = 'SAFE'
            print('\nEmail Manager |',signal_type,pair_symbol,timeframe,'LONG entries are SAFE. [',environment,']')
        if (timeframe == '3m' and diff_mins < stale_mins_3m) and entry_side == 'SHORT' and environment == 'BEARISH':
            status = 'SAFE'
            print('\nEmail Manager |',signal_type,pair_symbol,timeframe,'SHORT entries are SAFE. [',environment,']')
        #############################################################################
        if (timeframe == '4h' and diff_mins >= stale_mins_4h):
            print('\n* 4h signal older than ' + str(stale_mins_4h) + ' minutes (STALE), ignoring... *\n')
        if (timeframe == '4h' and diff_mins < stale_mins_4h) and entry_side == 'LONG' and environment == 'BULLISH':
            status = 'SAFE'
            print('\nEmail Manager |',signal_type,pair_symbol,timeframe,'LONG entries are SAFE. [',environment,']')
        if (timeframe == '4h' and diff_mins < stale_mins_4h) and entry_side == 'SHORT' and environment == 'BEARISH':
            status = 'SAFE'
            print('\nEmail Manager |',signal_type,pair_symbol,timeframe,'SHORT entries are SAFE. [',environment,']')
        print('\n└------------------------ SIGNALS | END EMAIL MANAGER ------------------------┘\n\n')
        return status,environment,unix_time





    def avoid_Regions(self,pair_symbol,pos_side):

        print('\n┌-------------------------- SIGNALS | AVOID REGIONS --------------------------┐\n\n')

        status = 'UNSAFE'
        diff = 0

        get_pair_settings = self.settings.load_Trade_Variables(pair_symbol)
        long_limit = float(get_pair_settings[33])
        short_limit = float(get_pair_settings[34])

        print('Checking avoid regions for',pair_symbol)
        print('\nNo LONGS above:',long_limit)
        print('\nNo SHORTS below:',short_limit)
      
        current_price = float(self.price_functions.request_Price_Data(pair_symbol)[0])
        print("\nThe price of",pair_symbol,"is",current_price)

        if pos_side == 'LONG' and current_price > long_limit:
            status = 'UNSAFE'
            print("\nUNSAFE box zone for",pos_side,"entry.")
            
        if pos_side == 'LONG' and current_price < long_limit:
            status = 'SAFE'
            print("\nSAFE box zone for",pos_side,"entry.")

        if pos_side == 'SHORT' and current_price < short_limit:
            status = 'UNSAFE'
            print("\nUNSAFE box zone for",pos_side,"entry.")

        if pos_side == 'SHORT' and current_price > short_limit:
            status = 'SAFE'
            print("\nSAFE zone for",pos_side,"entry.")

        print('\n\n└------------------------ SIGNALS | END AVOID REGIONS ------------------------┘\n\n')

        return status
        




    def final_Status(self,pair_symbol,side):

        print('\n*******************************************************************************')
        print('┌-------------------- SIGNALS | FINAL VERDICT',pair_symbol,side,'-------------------┐\n')

        points = 0
        total_points_possible = 4
        final_status = 'UNSAFE'
        enabled_3m = 1
        enabled_4h = 1
        enabled_mode = 1
        enabled_avoid = 1
        email_3m_status = 'UNSAFE'
        email_4h_status = 'UNSAFE'

        #check what signals are enabled
        print("\nSignals picked:")
        enabled_3m = int(self.settings.load_Trade_Variables(pair_symbol)[20])
        print("Email 3m:",enabled_3m)
        enabled_4h = int(self.settings.load_Trade_Variables(pair_symbol)[21])
        print("Email 4h:",enabled_4h)
        enabled_mode = int(self.settings.load_Trade_Variables(pair_symbol)[22])
        print("Mode average:",enabled_mode)
        enabled_avoid = int(self.settings.load_Trade_Variables(pair_symbol)[23])
        print("Avoid regions:",enabled_avoid)

        #fetch email 3m signals
        try:
            rsi_check_3m = self.check_Email_Signal(pair_symbol,side,'3m','RSI')[0]
        except:
            rsi_check_3m = 'UNSAFE'

        try:
            macd_check_3m = self.check_Email_Signal(pair_symbol,side,'3m','MACD')[0]
        except:
            macd_check_3m = 'UNSAFE'


        #-----------------------------------------------------------------------------------#
        use_rsi_3m = int(self.txt_ops.quick_read_txt_file('txt/settings/email/use_rsi_3m.txt'))
        use_macd_3m = int(self.txt_ops.quick_read_txt_file('txt/settings/email/use_macd_3m.txt'))

        if use_rsi_3m == 1 and use_macd_3m == 1:
            if rsi_check_3m == 'SAFE' or macd_check_3m == 'SAFE':
                email_3m_status = 'SAFE'
                print("\nJoint email 3m signal is:",email_3m_status)


        if use_rsi_3m == 2 and use_macd_3m == 2:
            if rsi_check_3m == 'SAFE' and macd_check_3m == 'SAFE':
                email_3m_status = 'SAFE'
                print("\nJoint email 3m signal is:",email_3m_status)

        if use_rsi_3m == 0 and use_macd_3m == 1:
            if macd_check_3m == 'SAFE':
                email_3m_status = 'SAFE'
                print("\nJoint email 3m signal is:",email_3m_status)

        if use_rsi_3m == 1 and use_macd_3m == 0:
            if rsi_check_3m == 'SAFE':
                email_3m_status = 'SAFE'
                print("\nJoint email 3m signal is:",email_3m_status)


                
        #-----------------------------------------------------------------------------------#



        #fetch email 4h signals
            
        try:
            rsi_check_4h = self.check_Email_Signal(pair_symbol,side,'4h','RSI')[0]
        except:
            rsi_check_4h = 'UNSAFE'

        try:
            macd_check_4h = self.check_Email_Signal(pair_symbol,side,'4h','MACD')[0]
        except:
            macd_check_4h = 'UNSAFE'



        if rsi_check_4h == 'SAFE' or macd_check_4h == 'SAFE':
            email_4h_status = 'SAFE'
            print("\nJoint email 4h signal is:",email_4h_status)

        #fetch mode values
        mode_safety = self.mode_Safety(pair_symbol,side)[0]

        #fetch avoid regions
        avoid_regions_safety = self.avoid_Regions(pair_symbol,side)

        #if signal is disabled a point is earned anyway, if enabled, needs to pass safety checks to gain a point
        #this is to avoid waiting endlessly for a broken signal module 
        if (enabled_3m == 0) or (enabled_3m == 1 and email_3m_status == 'SAFE'):
            points += 1
            print("\n+1 Point earned from 3m RSI or MACD")
        elif enabled_3m == 1 and email_3m_status == 'UNSAFE':
            print("\n-1 No points earned from 3m RSI or MACD")

        if (enabled_4h == 0) or (enabled_4h == 1 and email_4h_status == 'SAFE'):
            points += 1
            print("\n+1 Point earned from 4h RSI or MACD")
        elif enabled_4h == 1 and email_4h_status == 'UNSAFE':
            print("\n-1 No points earned from 4h RSI or MACD")

        if (enabled_mode == 0) or (enabled_mode == 1 and mode_safety == 'SAFE'):
            points += 1
            print("\n+1 Point earned from MODE AVERAGE")
        elif enabled_mode == 1 and mode_safety == 'UNSAFE':
            print("\n-1 No points earned from MODE AVERAGE")

        if (enabled_avoid == 0) or (enabled_avoid == 1 and avoid_regions_safety == 'SAFE'):
            points += 1
            print("\n+1 Point earned from AVOID REGIONS")
        elif enabled_avoid == 1 and avoid_regions_safety == 'UNSAFE':
            print("\n-1 No points earned from AVOID REGIONS")

        print("\n",mode_safety,avoid_regions_safety,email_3m_status,email_4h_status)
        
        print("\nTotal points:",points)

        if points == 4:
            final_status = 'SAFE'
        else:
            final_status = 'UNSAFE'

        print("\nVerdict:",final_status)

        print('\n\n\n└------------------ SIGNALS | END FINAL VERDICT',pair_symbol,side,'-----------------┘')
        print('*******************************************************************************\n')

        return final_status







if __name__ == '__main__':

    signal_functions = Signals(1)

    #get_avoid = signal_functions.avoid_Regions('LTCUSDT','SHORT')
    #print(get_avoid)

    get_final = signal_functions.final_Status('ADAUSDT','LONG')
    print(get_final)
    get_final = signal_functions.final_Status('BTCUSDT','LONG')
    print(get_final)

    #e = signal_functions.check_Email_Signal('BTCUSDT','LONG','4h','RSI')
    #e = signal_functions.check_Email_Signal('ETHUSDT','LONG','4h','RSI')
    #e = signal_functions.check_Email_Signal('ADAUSDT','LONG','4h','RSI')
    #e = signal_functions.check_Email_Signal('BNBUSDT','LONG','4h','RSI')
    #e = signal_functions.check_Email_Signal('LTCUSDT','LONG','4h','RSI')
    
