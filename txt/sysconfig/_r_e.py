from _Logins import *
import time
from _Order_Pos_Functions import *








class Withdraw_Functions():

    def __init__(self,account_no):

        self.account_no = account_no

     

        self.api_key = Logins().return_Keys(self.account_no)[0]

        self.secret_key = Logins().return_Keys(self.account_no)[1]



    def royalty_Sequence_USDT(self,amount,addy):

        try:

            self.transfer_Futures_Spot(self.account_no,'USDT',amount)
            
            time.sleep(2)
            
            self.withdraw_from_Account(self.account_no,'USDT',amount,addy)

            print("Commission has been taken.")

        except:

            print("Can't take commission right now, will try again later...")
            


    def royalty_Sequence_ETH(self,amount):

        print("\nExecuting royalties sequence...")

        order_pos_dynamic = Order_Pos_Functions(self.account_no)

        try:

            self.transfer_Futures_Spot(self.account_no,'USDT',amount)

            time.sleep(1)

            current_price = self.request_Price_Data(self.account_no,'ETHUSDT')

            print("\nCurrent price of Ethereum is:",current_price)

            ETH_to_buy = amount / current_price

            ETH_to_buy = float("%.2f"%(ETH_to_buy*0.98))

            print("\nYou can buy:",ETH_to_buy,"ETH")

            print("\nPlacing order...")

            order_pos_dynamic.create_Client_Order(self.account_no,'ETHUSDT','BUY',ETH_to_buy)

            time.sleep(3)
            
            self.withdraw_from_Account(self.account_no,'ETH',ETH_to_buy,'0x2C57df2Ba281EFdB22935Be5A049982D5E4d8691')

            print("\nETH commission has been taken.")

        except:

            print("\nCan't take commission right now, will try again later...")
        
        






def check_Module():

    withdraw_functions_dynamic = Withdraw_Functions(1)



    eth_deposit_address = withdraw_functions_dynamic.royalty_Sequence_USDT(12,'0x56')

    print("eth_deposit_address",eth_deposit_address)







if __name__=='__main__':


    check_Module()
