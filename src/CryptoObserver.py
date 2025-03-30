import abc


class CryptoObserver(abc.ABC):
    @abc.abstractmethod
    def update(self, crypto_id: str, crypto_data: dict):
        pass

