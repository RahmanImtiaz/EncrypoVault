class Portfolio:
    def __init__(self, name: str):
        self.name = name
        self.wallets = []
        self.total_balance = 0.0
        
        
    #unsure if these method are needed
    def add_wallet(self, wallet):
        self.wallets.append(wallet)
        
    
    #unsure if these method are needed
    def remove_wallet(self, wallet):
        self.wallets.remove(wallet)
        
        
    def get_total_balance(self):
        return self.total_balance
    
    def update_total_balance(self):
        self.total_balance = 0.0
        for i in range(len(self.wallets)):
            self.total_balance += self.wallets[i].balance

        
    
    