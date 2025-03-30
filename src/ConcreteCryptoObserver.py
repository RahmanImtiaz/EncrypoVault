from CryptoObserver import CryptoObserver
import ExchangeSocket


class ConcreteCryptoObserver(CryptoObserver):
    def __init__(self, on_update):
        self.on_update = on_update
        ExchangeSocket.ExchangeSocket().subscribe(self)

    def update(self, crypto_id: str, crypto_data: dict):
        self.on_update(crypto_id, crypto_data)