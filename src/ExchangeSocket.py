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
    COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=gbp&ids={crypto_ids}"
    
    def __init__(self, product_ids):
        super().__init__()
        self.product_ids = product_ids
        self.session = None
    
    def add_crypto(self, observer: CryptoObserver):
        """Implementation of abstract method from CryptoWatch"""
        if observer not in self.watchedCrypto:
            if isinstance(observer, Wallet):
                self.watchedCrypto.append(observer)
                print(f"Added {observer.name} to the watch list")
            elif isinstance(observer, Crypto):
                self.watchedCrypto.append(observer)
                print(f"Added {observer.crypto_id} to the watch list")
    
    def remove_crypto(self, observer: CryptoObserver):
        """Implementation of abstract method from CryptoWatch"""
        if observer in self.watchedCrypto:
            if isinstance(observer, Wallet):
                self.watchedCrypto.remove(observer)
                print(f"Removed {observer.name} from the watch list")
            elif isinstance(observer, Crypto):
                self.watchedCrypto.remove(observer)
                print(f"Removed {observer.crypto_id} from the watch list")
    
    def notifyObservers(self, crypto_id: str, crypto_data: dict):
        """Implementation of abstract method from CryptoWatch"""
        for observer in self.watchedCrypto:
            observer.update(crypto_id, crypto_data)
    
    async def connect_to_exchange(self):
        self.session = aiohttp.ClientSession()
        await self.fetch_prices()
    
    async def fetch_prices(self):
        if not self.session:
            return
            
        crypto_ids = ",".join(self.product_ids)
        url = self.COINGECKO_URL.format(crypto_ids=crypto_ids)
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    for crypto_data in data:
                        crypto_id = crypto_data.get("id")
                        if crypto_id:
                            self.notifyObservers(crypto_id, crypto_data)
                else:
                    print(f"Failed to fetch data: HTTP {response.status}")
        except Exception as e:
            print(f"Error fetching prices: {str(e)}")
    
    async def keep_updating_prices(self, interval=30):
        try:
            while True:
                await self.fetch_prices()
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            pass
    
    async def disconnect_from_exchange(self):
        if self.session:
            await self.session.close()
            self.session = None
        print("Disconnected from the exchange")