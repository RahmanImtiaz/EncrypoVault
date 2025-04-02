import bitcoinlib

import AccountsFileManager
from crypto_impl.HandlerInterface import HandlerInterface


class BitcoinWalletHandler(HandlerInterface):
    def get_address(self):
        return self.wallet.get_key().address

    wallet: bitcoinlib.wallets.Wallet

    def __init__(self, name):
        account = AccountsFileManager.AccountsFileManager.get_instance().get_loaded_account()
        wallet = bitcoinlib.wallets.Wallet.create(name)
        wallet.import_key(account.get_private_key())
        self.wallet = wallet


    @staticmethod
    def create_wallet(name) -> bitcoinlib.wallets.Wallet:
        account = AccountsFileManager.AccountsFileManager.get_instance().get_loaded_account()
        wallet = bitcoinlib.wallets.Wallet.create(name=name, keys=[account.get_private_key()])

        return wallet


    def toJSON(self):
        return self.wallet.as_json()

