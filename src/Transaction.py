import json


class Transaction:
    def __init__(self, timestamp, amount, tx_hash, sender, receiver, name):
        self.timestamp = timestamp
        self.amount = amount
        self.hash = tx_hash
        self.sender = sender
        self.receiver = receiver
        self.name = name
        

    # def __dict__(self):
    #     return {
    #         "timestamp": self.timestamp,
    #         "amount": self.amount,
    #         "hash": self.hash,
    #         "sender": self.sender,
    #         "receiver": self.receiver,
    #         "name": self.name,
    #     }
        
    def __str__(self):
        return f"Transaction({self.timestamp}, {self.amount}, {self.hash}, {self.sender}, {self.receiver}, {self.name})"

    def toJSON(self):
        return json.dumps({
            "timestamp": self.timestamp,
            "amount": self.amount,
            "hash": self.hash,
            "sender": self.sender,
            "receiver": self.receiver,
            "name": self.name,
        })
    
    
    
        
        
        