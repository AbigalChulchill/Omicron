from bitcoinlib.wallets import Wallet
from bitcoinlib.keys import Key
import time

class BTC_Net_Functions:

    def __init__(self):

        self.wallet_name = str(time.time() * 1000000)

        #self.exodus_public_old = '146EMVvFUJgd7dY2CC1jX1wjbosTWQDpMe'
        #self.exodus_priv_old = 'L26HBgGmAPbE4TXgVq1VEk4VBX8YVGstMTfq4EbPRN5HGWREh7AL'
        #self.sender_pub = '1HH9L5Nms4C8FM1bpeWfN9HhHjMsyfm5Jh'
        #self.sender_priv = '5K9KpNFNytuehGMi7sYvQdYyWQ9YCYgoPZK4UokGVedycb1KDGt'


    def send_BTC(self,sender_priv,receive_addy,amount):

        amount_str = str(amount) + ' ' + 'BTC'

        w = Wallet.create(self.wallet_name,keys=sender_priv,scheme='single')
        #public_key = w.get_key()

        w.scan()
        w.info()

        try:
            t = w.send_to(receive_addy,amount_str)
            t.info()
            print("\nBTC sent successfully!")
        except:
            print("\nError: Failed to execute BTC send!")


if __name__ == '__main__':

    b = BTC_Net_Functions()
    send_btc = b.send_BTC('5K9KpNFNytuehGMi7sYvQdYyWQ9YCYgoPZK4UokGVedycb1KDGt','146EMVvFUJgd7dY2CC1jX1wjbosTWQDpMe',0.001)




