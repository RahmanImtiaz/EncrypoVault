from abc import ABC, abstractmethod

from CryptoObserver import CryptoObserver


class Wallet(CryptoObserver, ABC):
    def __init__(self, name: str):
        self.balance = 0.0
        self.address = None
        self.name = name
        self.holdings = {}

    @staticmethod
    @abstractmethod
    def create_wallet(name):
        pass

    @abstractmethod
    def toJSON(self):
        pass

    def update(self, crypto_id: str, crypto_data: dict):
        if crypto_id in self.holdings:
            holding = self.holding[crypto_id]
            new_price = crypto_data["current_price"]
            holding["value"] = holding["quantity"] * new_price
            print("Updated " [crypto_id] + " value to " + str(holding["value"]))
            self._calcualte_total_balance()
        else:
            print("Could not update " [crypto_id] + " value")
            
            
    def _calcualte_total_balance(self):
        self.balance = 0.0
        for holding in self.holdings.values():
            self.balance += holding["value"]
            
            
    def get_total_balance(self):
        return self.balance

