import abc


class CryptoObserver(abc.ABC):
    @abc.abstractmethod
    def update(self, crypto_id: str, crypto_data: dict):
        pass

class ConcreteCryptoObserver(CryptoObserver):
    def __init__(self, on_update):
        self.on_update = on_update

    def update(self, crypto_id: str, crypto_data: dict):
        self.on_update(crypto_id, crypto_data)