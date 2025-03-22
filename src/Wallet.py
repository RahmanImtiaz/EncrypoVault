from abc import ABC, abstractmethod

from CryptoObserver import CryptoObserver
from Crypto import Crypto

class Wallet(CryptoObserver, ABC):
    def __init__(self, name: str):
        self.balance = 0.0
        self.address = None
        self.name = name
        self.holdings = {}
        # the holdings will be a dictionary with an object of Crypto as the key and the amount of the crypto as the value
        # e.g. {Crypto: 0.5, Crypto: 1.0}

    @staticmethod
    @abstractmethod
    def create_wallet(name):
        pass

    @abstractmethod
    def toJSON(self):
        pass

    def update(self, crypto_id: str, crypto_data: dict):
        if crypto_id in self.holdings:
            crypto = self.holdings[crypto_id]["crypto"]
            crypto.update(crypto_id, crypto_data)
            print(f"Updated {crypto_id}")
        else:
            print(f"Could not update {crypto_id}, not found in holdings")
            
            
    def _calcualte_total_balance(self):
        self.balance = 0.0
        for crypto in self.holdings:
            self.balance += crypto.current_price * self.holdings[crypto]
            
            
    def get_total_balance(self):
        return self.balance

