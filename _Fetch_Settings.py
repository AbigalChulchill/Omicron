######

from _Maths_Functions import *
import os

class Settings():

    def __init__(self,account_no):

        self.account_no = account_no

    def load_Trade_Variables(self,pair_symbol):

        init_dict = {}
        parts = []
        #
        active = 0 #0
        busy = 0 #1
        quantity_to_trade = 0 #2
        split_order_segments = 0 #3
        order_split_time_range = 0 #4
        take_profit = 0 #5
        stop_loss = 0 #6
        stop_to_limit_spread = 0 #7
        is_limit_entry = 0 #8
        initial_bid = 0 #9
        bids = 0 #10
        manual_trigger_long = 0 #11
        manual_trigger_short = 0 #12
        auto_longs = 0 #13
        auto_shorts = 0 #14
        cancel_linked = 0 #15
        force_close = 0 #16
        rebuild = 0 #17
        use_liq_sl = 0 #18
        dynamic_tp = 0 #19
        use_mail_5m = 0 #20
        use_mail_4h = 0 #21
        use_sup_res = 0 #22
        use_avoid = 0 #23
        use_round = 0 #24
        use_barts = 0 #25
        use_turan = 0 #26
        dynamic_sl = 0 #27
        mode_algo = '' #28
        mode_buffer = 0 #29
        auto_sl_breach = 0 #30
        tp_type = '' #31
        sl_type = '' #32
        avoid_region_long = 0 #33
        avoid_region_short = 0 #34
        orders = '' #35
        positions = '' #36
        leverage = 5 #37
        req_lev_change = 5 #38
        pair_settings_path = 'txt/setup/' + str(self.account_no) + '/setup_' + str(self.account_no) + '_' + str(  pair_symbol  ) + '.txt'


        if os.path.isfile(pair_settings_path):

            with open (pair_settings_path, "r") as hfile:
                sp = hfile.read()
            lines = sp.split("\n")

            for line in lines:
                if line!='':
                    parts = line.split("=")
                init_dict[parts[0]] = parts[1]

            active = int(init_dict['active'])
            busy = int(init_dict['busy'])
            quantity_to_trade = float(init_dict['quantity_to_trade'])
            split_order_segments = int(init_dict['split_order_into_segments'])
            order_split_time_range = int(init_dict['order_split_time_range'])
            take_profit = float(init_dict['take_profit'])
            stop_loss = float(init_dict['stop_loss'])
            stop_to_limit_spread = float(init_dict['stop_to_limit_spread'])
            is_limit_entry = int(init_dict['is_limit_entry'])
            initial_bid = float(init_dict['initial_bid'])
            bids = float(init_dict['bids'])
            manual_trigger_long = int(init_dict['manual_trigger_long'])
            manual_trigger_short = int(init_dict['manual_trigger_short'])
            auto_longs = int(init_dict['auto_longs'])
            auto_shorts = int(init_dict['auto_shorts'])
            cancel_linked = int(init_dict['cancel_linked'])
            force_close = int(init_dict['force_close'])
            rebuild = int(init_dict['rebuild'])
            use_liq_sl = int(init_dict['use_liq_sl'])
            dynamic_tp = int(init_dict['dynamic_tp'])
            use_mail_5m = int(init_dict['use_mail_5m'])
            use_mail_4h = int(init_dict['use_mail_4h'])
            use_sup_res = int(init_dict['use_sup_res'])
            use_avoid = int(init_dict['use_avoid'])
            use_round = int(init_dict['use_round'])
            use_barts = int(init_dict['use_barts'])
            use_turan = int(init_dict['use_turan'])
            dynamic_sl = int(init_dict['dynamic_sl'])
            mode_algo = str(init_dict['mode_algo'])
            mode_buffer = float(init_dict['mode_buffer'])
            auto_sl_breach = float(init_dict['auto_sl_breach'])
            tp_type = str(init_dict['tp_type'])
            sl_type = str(init_dict['sl_type'])
            avoid_region_long = float(init_dict['avoid_region_long'])
            avoid_region_short = float(init_dict['avoid_region_short'])
            orders = str(init_dict['orders'])
            positions = str(init_dict['positions'])
            leverage = int(init_dict['leverage'])
            req_lev_change = int(init_dict['req_lev_change'])

        else:

            print("\nError: Pair symbol settings file does not exist!")

        return active,\
               busy,\
               quantity_to_trade,\
               split_order_segments,\
               order_split_time_range,\
               take_profit,\
               stop_loss,\
               stop_to_limit_spread,\
               is_limit_entry,\
               initial_bid,\
               bids,\
               manual_trigger_long,\
               manual_trigger_short,\
               auto_longs,\
               auto_shorts,\
               cancel_linked,\
               force_close,\
               rebuild,\
               use_liq_sl,\
               dynamic_tp,\
               use_mail_5m,\
               use_mail_4h,\
               use_sup_res,\
               use_avoid,\
               use_round,\
               use_barts,\
               use_turan,\
               dynamic_sl,\
               mode_algo,\
               mode_buffer,\
               auto_sl_breach,\
               tp_type,\
               sl_type,\
               avoid_region_long,\
               avoid_region_short,\
               orders,\
               positions,\
               leverage,\
               req_lev_change

                                                                                            
    def load_Account_Variables(self):

        init_dict = {}
        parts = []
        #
        active=0  #0
        busy=0  #1
        balance=''   #2
        last_combo_pos=''  #3
        last_combo_settings=''  #4
        dep_address_USDT=''  #5
        open_orders=''  #6
        open_positions=''  #7
        transfer_asset=''  #8
        transfer_asset_amount=0  #9
        spot_fut=0  #10
        fut_spot=0  #11
        withdraw=0  #12
        maintain_balance=0 #13
        account_settings_path = 'txt/setup/' + str(self.account_no) + '/setup_' + str(self.account_no) + '.txt'


        if os.path.isfile(account_settings_path):
            with open (account_settings_path, "r") as hfile:
                sp = hfile.read()
            lines = sp.split("\n")

            for line in lines:
                if line != '':
                    parts = line.split("=")
                init_dict[parts[0]] = parts[1]

            #print(init_dict)

            active = int(init_dict['active'])
            busy = int(init_dict['busy'])
            balance = str(init_dict['balance'])
            last_combo_pos = str(init_dict['last_combo_pos'])
            last_combo_settings = str(init_dict['last_combo_settings'])
            dep_address_USDT = str(init_dict['dep_address_USDT'])
            open_orders =  str(init_dict['open_orders'])
            open_positions = str(init_dict['open_positions'])
            transfer_asset = str(init_dict['transfer_asset'])
            transfer_asset_amount = str(init_dict['transfer_asset_amount'])
            spot_fut = str(init_dict['spot_fut'])
            fut_spot = str(init_dict['fut_spot'])
            withdraw = str(init_dict['withdraw'])
            maintain_balance = int(init_dict['maintain_balance'])
        else:
            
            print("\nError: Account settings file does not exist!")

        return active,\
    busy,\
    balance,\
    last_combo_pos,\
    last_combo_settings,\
    dep_address_USDT,\
    open_orders,\
    open_positions,\
    transfer_asset,\
    transfer_asset_amount,\
    spot_fut,\
    fut_spot,\
    withdraw,\
    maintain_balance


if __name__ == '__main__':

    #example use
    settings = Settings(1)
    b = settings.load_Trade_Variables('ETHUSDT')
    print(b)

    #example use
    #settings = Settings(1)
    #a = settings.load_Account_Variables()[4]
    #print(a)






