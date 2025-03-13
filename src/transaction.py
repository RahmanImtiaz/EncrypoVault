class Transaction:
    def __init__(self, timestamp, amount, hash, sender, receiver, name):
        self.timestamp = timestamp
        self.amount = amount
        self.hash = hash
        self.sender = sender
        self.receiver = receiver
        self.name = name
        
        
        
    def __str__(self):
        return f"Transaction({self.timestamp}, {self.amount}, {self.hash}, {self.sender}, {self.receiver}, {self.name})"
    
    
    
        
        
        