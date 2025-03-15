
from CryptoObserver import CryptoObserver

class Wallet(CryptoObserver):
    def __init__(self, name: str):
        self.balance = 0.0
        self.address = None
        self.name = name
        self.holdings = {}
        
    def update(self, crypto_name: str, new_price: float):
        if crypto_name in self.holdings:
            quantity = self.holdings[crypto_name]
            value = quantity * new_price
            self.holdings[crypto_name] = value
            print("Updated " + crypto_name + " value to " + str(value))
        else:
            print("Could not update " + crypto_name + " value")



            
            
            
