import datetime

class Crypto:
    def __init__(self, name: str):
        self.name = name
        self.conversion_rate = 0.0
        self.last_updated = None
        
        
    def update_price(self, new_price: float):
        self.conversion_rate = new_price
        self.last_updated = datetime.datetime.now()
    
        
        
        