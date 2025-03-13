from exchangeSocket import ExchangeSocket
from crypto import Crypto
from src.wallet import Wallet


class CryptoWatch:

    def __init__(self, name: str, exchange_socket: ExchangeSocket):
        self.exchange_socket = exchange_socket
        self.wallets = []         
        self.watchedCryptos = []  

    def add_wallet(self, wallet: Wallet):
        if wallet not in self.wallets:
            self.wallets.append(wallet)
            wallet.cryptowatch = self

    def remove_wallet(self, wallet: Wallet):
        if wallet in self.wallets:
            self.wallets.remove(wallet)
            wallet.cryptowatch = None

    def add_crypto(self, crypto_name: str):
        if not any(c.name == crypto_name for c in self.watchedCryptos):
            self.watchedCryptos.append(Crypto(crypto_name))

    def remove_crypto(self, crypto_name: str):
        self.watchedCryptos = [
            c for c in self.watchedCryptos if c.name != crypto_name
        ]

    def notify_observers(self):
        #unsure about this method and what its role is
        print("Notifying observers...")

    async def update_all_prices(self):
        for crypto_obj in self.watchedCryptos:
            price = await self.exchange_socket.get_crypto_price(crypto_obj.name)
            crypto_obj.update_price(price)
