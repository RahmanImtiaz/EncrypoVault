import csv
import os
from abc import ABC, abstractmethod


# THE API I RECOMMED IS THE CRYPTO API, IT PROVIDES ACCESS TO THE BLOCKCHAIN BUT ALSO LETS US HANDLE THE PRIVATE KEYS, COINBASE API
# DOES NOT LET US DO THIS!!! 
# ALSO HAS A SANDBOX FEATURE TO ALLOW US TO TEST WHETHER OUR CODE WORKS OR NOT


class CryptoTransactionStrategy(ABC):
    
    @abstractmethod
    def buy_crypto(self, crypto_name: str, amount: float):
        pass

    # EACH TIME WE BUY WE MUST ENCRYPT AND DECRYPT THE FILE THAT STORES OUR PRIVATE KEYS
    
    @abstractmethod
    def sell_crypto(self, crypto_name: str, amount: float):
        pass

    # EACH TIME WE SELL WE MUST ENCRYPT AND DECRYPT THE FILE THAT STORES OUR PRIVATE KEYS
    
    @abstractmethod
    def send_crypto(self, send_to: str, amount: float):
        pass

# NOT SURE HOW TO SEND CRYPTO AS OF RIGHT NOW, BUT I BELIEVE CRYPTO APIS HAS SOME DOCUMENTATION FOR THIS
    
    @abstractmethod
    def receive_crypto(self, wallet_address: str):
        pass


# CRYPTO API CAN GENERATE WALLET ADDRESSES FOR OUR USERS. 
    
    @abstractmethod
    def generate_qr_code(self, wallet_address: str):
        pass
    

    
class RealTransaction(CryptoTransactionStrategy):
    
    def buy_crypto(self, crypto_name: str, amount: float):
        pass

    def sell_crypto(self, crypto_name: str, amount: float):
        pass
    
    def send_crypto(self, send_to: str, amount: float):
        pass
    
    def receive_crypto(self, wallet_address: str):
        pass
    
    def generate_qr_code(self, wallet_address: str):
        pass
    
    
    
class MockTransaction(CryptoTransactionStrategy):
    
    def buy_crypto(self, crypto_name: str, amount: float):
        pass
    
    def sell_crypto(self, crypto_name: str, amount: float):
        pass
    
    def send_crypto(self, send_to: str, amount: float):
        pass
    
    def receive_crypto(self, wallet_address: str):
        pass
    
    def generate_qr_code(self, wallet_address: str):
        pass
