from abc import ABC, abstractmethod
from CryptoObserver import CryptoObserver
from Crypto import Crypto

class Wallet(CryptoObserver):
    def __init__(self, name: str, initial_balance: float = 0.0):
        self.name = name
        self.balance = initial_balance
        self.address = None
        self.holdings = {}  # Now using {crypto_id: {"crypto": Crypto, "amount": float}}

    @staticmethod
    def create_wallet(name: str):
        return Wallet(name)

    def toJSON(self):
        return {
            "name": self.name,
            "balance": self.balance,
            "address": self.address,
            "holdings": {
                crypto_id: {
                    "crypto": data["crypto"].crypto_id,
                    "amount": data["amount"]
                }
                for crypto_id, data in self.holdings.items()
            }
        }

    def update(self, crypto_id: str, crypto_data: dict):
        if crypto_id in self.holdings:
            self.holdings[crypto_id]["crypto"].update(crypto_id, crypto_data)
            print(f"Updated {crypto_id} in wallet {self.name}")
        else:
            print(f"Crypto {crypto_id} not found in wallet {self.name}")

    def _calculate_total_balance(self):
        self.balance = sum(
            data["crypto"].current_price * data["amount"]
            for data in self.holdings.values()
            if data["crypto"].current_price is not None
        )

    def get_total_balance(self):
        self._calculate_total_balance()
        return self.balance