import json

from pycoin.symbols.xtn import network

import AccountsFileManager
from crypto_impl.HandlerInterface import HandlerInterface
from crypto_impl.WalletType import WalletType


class BitcoinWalletHandler(HandlerInterface):

    _pycoin_key = None
    _name: str = ""

    def __init__(self, name):
        self._name = name
        self._pycoin_key = network.keys.private(secret_exponent=self._get_secret_exponent())

    @staticmethod
    def create_wallet(name):
       return BitcoinWalletHandler(name)

    def _get_secret_exponent(self):
        key = self._get_child_key()
        secret_exponent = int.from_bytes(key.PrivateKey().Raw().ToBytes(), byteorder="big")
        return secret_exponent

    def _get_child_key(self):
        ctx = AccountsFileManager.AccountsFileManager.get_instance().get_loaded_account().get_bip32_ctx()
        ind = self.account_name_to_index(self._name, self.get_wallet_type())
        return ctx.ChildKey(ind)

    def send_tx(self, amount, destination_address):
        self._pycoin_key

    def get_tx_info(self, tx_id):
        pass

    def get_tx(self):
        pass

    @staticmethod
    def load_wallet(data: dict):
        return BitcoinWalletHandler(data["name"])

    def get_address(self):
        return self._pycoin_key.address()

    def get_balance(self):


    def toJSON(self):
        return json.dumps({
            "name": self._name,
            "type": str(self.get_wallet_type()),
            "balance": self.get_balance()
        })

    @staticmethod
    def get_wallet_type() -> WalletType:
        return WalletType.BITCOIN

