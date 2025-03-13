import datetime
from transaction import Transaction

class transaction_log:
    def __init__(self):
        self._log = []
        
    def search(timestamp: datetime, amount: float, hash: str, sentTo: str, sentBy: str):
        for transaction in self._log:
            if transaction.timestamp == timestamp and transaction.amount == amount and transaction.hash == hash and transaction.sentTo == sentTo and transaction.sentBy == sentBy:
                return transaction
        return None
        
    
    def add_to_transaction_log(transaction: Transaction):
        self._log.append(transaction)
        