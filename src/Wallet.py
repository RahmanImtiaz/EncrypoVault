
import requests  # Add this import

from ConcreteCryptoObserver import ConcreteCryptoObserver
from CryptoObserver import CryptoObserver
import json
import os
from typing import Optional

from crypto_impl.BitcoinWalletHandler import BitcoinWalletHandler
from crypto_impl.HandlerInterface import HandlerInterface
from crypto_impl.WalletType import WalletType


class Wallet(CryptoObserver):
    def __init__(self, 
                 name: str,
                 wallet_type: WalletType,
                 address: Optional[str] = None,
                 last_balance: float = 0,
                 fake_balance: float = 0):
        self.name = name
        self.wallet_type = wallet_type
        self.crypto_handler: HandlerInterface
        self.holdings = {}
        match wallet_type:
            case WalletType.BITCOIN:
                self.crypto_handler = BitcoinWalletHandler(self.name, last_balance, fake_balance)
            # case WalletType.ETHEREUM:
            #     pass
            case _:
                print("Current impl does not support wallet type {}".format(wallet_type))
        self.address = address or self.crypto_handler.get_address()
        self.observer = ConcreteCryptoObserver(on_update=self.update)

    def toJSON(self):
        """Wallet serialization"""
        return json.dumps({
            "name": self.name,
            "address": self.address,
            "type": str(self.wallet_type),
            "balance": self.crypto_handler.get_balance(),
            "fake_balance": self.crypto_handler.fake_balance,
        }, indent=4)

    def update(self, crypto_id: str, crypto_data: dict):
        symbol = ""
        if crypto_id == "bitcoin":
            symbol = "BTC"
        elif crypto_id == "ethereum":
            symbol = "ETH"
        else:
            print(f"Unknown crypto ID: {crypto_id}")
            return
        pass
    
        # this as of right now does not need to be implemented as Wallet does not hold the price of the cryptocurrency
        # the current implementation holds the amount of BTC or ETH in balance then the frontend gets the price from
        # price_cache or the JSON file and displays that

    def _calculate_total_balance(self):
        self.balance = sum(
            data["crypto"].current_price * data["amount"]
            for data in self.holdings.values()
            if data["crypto"].current_price is not None
        )

    def get_total_balance(self):
        self._calculate_total_balance()
        return self.balance