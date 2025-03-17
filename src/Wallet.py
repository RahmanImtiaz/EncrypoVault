
from CryptoObserver import CryptoObserver

class Wallet(CryptoObserver):
    def __init__(self, name: str):
        self.balance = 0.0
        self.address = None
        self.name = name
        self.holdings = {}
        
    def update(self, crypto_name: str, new_price: float):
        if crypto_name in self.holdings:
            holding = self.holdings[crypto_name]
            holding["value"] = holding["quantity"] * new_price
            print("Updated " + crypto_name + " value to " + str(holding["value"]))
        else:
            print("Could not update " + crypto_name + " value")




            
            
            
