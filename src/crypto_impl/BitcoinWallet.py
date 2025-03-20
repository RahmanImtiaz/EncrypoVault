import json

import bitcoinlib

from src.AccountsFileManager import AccountsFileManager
from src.Wallet import Wallet


class BitcoinWallet(Wallet):
    wallet: bitcoinlib.wallets.Wallet

    @staticmethod
    def create_wallet(name) -> 'BitcoinWallet':
        account = AccountsFileManager.get_instance().get_loaded_account()
        wallet = bitcoinlib.wallets.Wallet.create(name=name, keys=[account.get_secret_key()])

        return wallet


    def toJSON(self):
        return json.dumps({
            "name": self.name,
            "holdings": self.holdings,
            "balance": self.balance,
            "address": self.address,
            "transactions": self.wallet.transactions()
        })

