import blockcypher
import requests  # Add this import

from ConcreteCryptoObserver import ConcreteCryptoObserver
from CryptoObserver import CryptoObserver
import json
import os
from typing import Optional

from crypto_impl.BitcoinWalletHandler import BitcoinWalletHandler
from crypto_impl.WalletType import WalletType


class Wallet(CryptoObserver):
    def __init__(self, 
                 name: str,
                 wallet_type: WalletType,
                 address: Optional[str] = None):
        self.name = name
        self.wallet_type = wallet_type
        self.holdings = {}
        match wallet_type:
            case WalletType.BITCOIN:
                self.crypto_handler = BitcoinWalletHandler()
            # case WalletType.ETHEREUM:
            #     pass
            case _:
                print("Current impl does not support wallet type {}".format(wallet_type))
        self.address = address or self.crypto_handler.create_wallet(name)
        self.observer = ConcreteCryptoObserver(on_update=self.update)

    def toJSON(self):
        """Wallet serialization"""
        return json.dumps({
            "name": self.name,
            "address": self.address,
            "type": self.wallet_type,
            "balance": self.balance,
            "holdings": {
                crypto_id: {"amount": data["amount"]} 
                for crypto_id, data in self.holdings.items()
            }
        }, indent=4)

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