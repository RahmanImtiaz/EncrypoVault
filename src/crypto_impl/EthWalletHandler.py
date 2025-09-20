from crypto_impl.HandlerInterface import HandlerInterface
from crypto_impl.WalletType import WalletType


class EthWalletHandler(HandlerInterface):

    def __init__(self, name):
        pass

    @staticmethod
    def create_wallet(self):
        pass

    def get_address(self):
        pass

    def send_tx(self, amount, destination_address):
        pass

    def get_tx_info(self, tx_id):
        pass

    def get_tx(self):
        pass

    @staticmethod
    def load_wallet(data: dict):
        pass

    @staticmethod
    def get_wallet_type() -> WalletType:
        return WalletType.ETHEREUM

    def get_balance(self):
        pass