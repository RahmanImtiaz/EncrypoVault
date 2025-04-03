import abc
import hashlib

from crypto_impl.WalletType import WalletType


class HandlerInterface(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def create_wallet(self):
        pass

    @abc.abstractmethod
    def get_address(self):
        pass

    @abc.abstractmethod
    def send_tx(self, amount, destination_address):
        pass

    @abc.abstractmethod
    def get_tx_info(self, tx_id):
        pass

    @abc.abstractmethod
    def get_tx(self):
        pass

    @staticmethod
    @abc.abstractmethod
    def load_wallet(data: dict):
        pass

    @staticmethod
    @abc.abstractmethod
    def get_wallet_type() -> WalletType:
        pass

    @abc.abstractmethod
    def get_balance(self):
        pass

    @staticmethod
    def account_name_to_index(account_name: str, wallet_type: WalletType) -> int:
        """
        account_name-wallet_type -> sha256 sum, take first 8 bytes, parse from the hex and then modulo it by 2^31
        """
        h = hashlib.sha256(f"{account_name}-{str(wallet_type)}".encode(
            "utf-8")).hexdigest()
        return int(h[:8], 16) % (2**31)
