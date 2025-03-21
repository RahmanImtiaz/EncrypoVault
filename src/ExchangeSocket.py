import abc, json
from abc import abstractmethod
import asyncio
import aiohttp
from Crypto import Crypto
from Wallet import Wallet
import websockets
from CryptoObserver import CryptoObserver

class CryptoWatch(abc.ABC):
    def __init__(self):
        self.watchedCrypto = []
    
    
    @abstractmethod
    def add_crypto(self, crypto_name: str):
        pass
    
    @abstractmethod
    def remove_crypto(self, crypto_name: str):
        pass
    
    @abstractmethod
    def notifyObservers(self):
        pass


class ExchangeSocket(CryptoWatch):
    
    COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=gbp"
    def __init__(self, product_ids):
        super().__init__()
        self.product_ids = product_ids 
        # this product_ids is used for testing the code
        
    def add_crypto(self, observer: CryptoObserver):
        if observer not in self.watchedCrypto:
            if isinstance(observer, Wallet):
                self.watchedCrypto.append(observer)
                print("Added " + observer.name + " to the watch list")
            elif isinstance(observer, Crypto):
                self.watchedCrypto.append(observer)
                print("Added " + observer.crypto_id + " to the watch list")
    
    def remove_crypto(self, observer: CryptoObserver):
        if observer in self.watchedCrypto:
            if isinstance(observer, Wallet):
                self.watchedCrypto.remove(observer)
                print("Removed " + observer.name + " from the watch list")
            elif isinstance(observer, Crypto):
                self.watchedCrypto.remove(observer)
                print("Removed " + observer.crypto_id + " from the watch list")
    
    def notifyObservers(self, crypto_id: str, crypto_data: dict):
        for observer in self.watchedCrypto:
            observer.update(crypto_id, crypto_data)

    async def connect_to_exchange(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.COINGECKO_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    for crypto_data in data:
                        crypto_id = crypto_data.get("id")
                        if crypto_id:
                            self.notifyObservers(crypto_id, crypto_data)
                            # print("Received " + crypto_id + " data")
                else:
                    print("Failed to fetch data")
                    
        await self.disconnect_from_exchange()
                    

    async def disconnect_from_exchange(self):
        print("Disconnected from the exchange")
