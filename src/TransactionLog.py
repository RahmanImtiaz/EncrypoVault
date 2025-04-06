import datetime
import json
from typing import List

from Transaction import Transaction
from util import to_json_recursive


class TransactionLog:
    _log: List[Transaction]
    def __init__(self):
        self._log = []
        
    def search(self,
               timestamp: datetime = None,
               amount: float = None,
               tx_hash: str = None,
               sent_to: str = None,
               sent_by: str = None):
        for transaction in self._log:
            if (transaction.timestamp == timestamp and
                    transaction.amount == amount and
                    transaction.hash == tx_hash and
                    transaction.receiver == sent_to and
                    transaction.sender == sent_by):
                return transaction
        return None
    
    def add_to_transaction_log(self, transaction: Transaction):
        self._log.append(transaction)

    def toJSON(self):
        return to_json_recursive(self._log)