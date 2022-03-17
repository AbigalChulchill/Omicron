import os
from web3 import Web3
from _Price_Functions import *


class ETH_Net_Functions:

    def __init__(self,network_ID):

        self.network_ID = network_ID

        #set to Mainnet by default
        self.network = 'https://mainnet.infura.io/v3/f26ad2fd49db49bda46c88eb08947586'

        #other network options
        if self.network_ID == 4:
            self.network = 'https://rinkeby.infura.io/v3/f26ad2fd49db49bda46c88eb08947586'

        self.w3 = Web3(Web3.HTTPProvider(self.network))
        self.connected = self.w3.isConnected()
        print("Connected to",self.network,self.connected)

    def send_ETH(self,address_sender,address_receiver,priv_key,eth_to_send,max_gas,gas_unit):

        address_sender = Web3.toChecksumAddress(address_sender)
        address_receiver = Web3.toChecksumAddress(address_receiver)

        private_key = os.getenv('',priv_key)

        #prevents multi spend
        nonce = self.w3.eth.getTransactionCount(address_sender)

        #VARS
        print('\nETH to send:',eth_to_send)
        print('\nMax gas:',max_gas)
        print('\nMax Gwei spend per gas unit:',gas_unit)
        gas_total = max_gas * gas_unit
        print('\nTotal Gwei cost:',gas_total)
        eth_value = gas_total * 0.000000001
        print('\nETH cost of transaction:',eth_value)
        get_eth_spot_price = Price_Functions().request_Spot_Price_Data('ETHUSDT')
        cost_in_dollars = eth_value * get_eth_spot_price
        print('\nDollar cost of transaction: $' + str(cost_in_dollars))

        tx = {
            'chainId':self.network_ID,
            'nonce':nonce,
            'from':address_sender,
            'to':address_receiver,
            'gas':max_gas,
            'gasPrice':self.w3.toWei(gas_unit,'gwei'),
            'value':self.w3.toWei(eth_to_send,'ether'),
        }

        try:
            signed_tx = self.w3.eth.account.signTransaction(tx,private_key)
            print('\nsigned_tx',signed_tx)
            tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print('\ntx_hash',tx_hash)
        except:
            ("\nError: Transaction send error")


if __name__ == '__main__':

    connect_to_mainnet = ETH_Net_Functions(1)

    send_eth = connect_to_mainnet.send_ETH('0x9fad2a49373b3d760236ad5b71a11a8585e9a9f9',\
    '0xC6f75453291a53a42700348F41E3A149a5a7A4ED',\
    'ddb05be3b7f13845b3f99f14e07b3fb690c386ae5d15d46e7b9e5737b972d779',\
    0.001,\
    21001,\
    62)


