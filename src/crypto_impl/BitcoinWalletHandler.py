import json

import bitcoinlib

import AccountsFileManager
from crypto_impl.HandlerInterface import HandlerInterface


class BitcoinWalletHandler(HandlerInterface):
    wallet: bitcoinlib.wallets.Wallet

    def __init__(self, name):
        account = AccountsFileManager.AccountsFileManager.get_instance().get_loaded_account()
        wallet = bitcoinlib.wallets.Wallet.create(name, keys=[account.get_secret_key()])
        self.wallet = wallet


    @staticmethod
    def create_wallet(name) -> bitcoinlib.wallets.Wallet:
        account = AccountsFileManager.AccountsFileManager.get_instance().get_loaded_account()
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

