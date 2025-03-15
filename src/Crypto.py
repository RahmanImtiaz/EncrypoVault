import datetime
from CryptoObserver import CryptoObserver

class Crypto(CryptoObserver):
    def __init__(self, name: str):
        self.name = name
        self.conversion_rate = 0.0
        self.last_updated = None
        

    
    
    def update(self, crypto_name: str, new_price: float):
        if self.name == crypto_name:
            self.last_updated = datetime.datetime.now()
            print("Updated " + crypto_name + " price to " + str(new_price))

        
        
        
        
