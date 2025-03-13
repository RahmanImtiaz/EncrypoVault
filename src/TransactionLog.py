import datetime
from Transaction import Transaction

class TransactionLog:
    def __init__(self):
        self._log = []
        
    def search(self, timestamp: datetime, amount: float, tx_hash: str, sent_to: str, sent_by: str):
        for transaction in self._log:
            if transaction.timestamp == timestamp and transaction.amount == amount and transaction.hash == tx_hash and transaction.sentTo == sent_to and transaction.sentBy == sent_by:
                return transaction
        return None
        
    
    def add_to_transaction_log(self, transaction: Transaction):
        self._log.append(transaction)
        