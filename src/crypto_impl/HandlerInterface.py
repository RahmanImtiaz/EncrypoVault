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

    @staticmethod
    def account_name_to_index(account_name: str, wallet_type: WalletType) -> int:  # Hash the account name using SHA-256
        h = hashlib.sha256(f"{account_name}-{str(wallet_type)}".encode(
            "utf-8")).hexdigest()  # Use the first 8 characters (4 bytes) of the hash to create an integer # Then take modulo 231 to ensure it fits in the range for hardened indices.
        return int(h[:8], 16) % (2**31)
