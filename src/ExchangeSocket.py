import abc
import asyncio
from abc import abstractmethod
import aiohttp
import requests

class CryptoWatch(abc.ABC):
    def __init__(self):
        self.watchedCrypto = []
        self.observers = []

    def subscribe(self, observer):
        self.observers.append(observer)
    
    
    @abstractmethod
    def add_crypto(self, crypto_name: str):
        pass
    
    @abstractmethod
    def remove_crypto(self, crypto_name: str):
        pass
    
    @abstractmethod
    def notify_observers(self, crypto_id, crypto_data):
        pass


class ExchangeSocket(CryptoWatch):
    COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=gbp&ids={crypto_ids}"
    API_KEY = "CG-DkGqhTNQFPWTVnNub51H8q6t\t"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key":  API_KEY,
        "Connection": "close" 
    }
    _ExchangeSocket = None

    def __new__(cls):
        if cls._ExchangeSocket is None:
            cls._ExchangeSocket = super(ExchangeSocket, cls).__new__(cls)
            cls._ExchangeSocket._initialized = False
        return cls._ExchangeSocket

    def __init__(self):
        if getattr(self, '_initialized'):
            return
        super().__init__()
        self.product_ids = []
        self.session = None
        self._initialized = True
    
    def add_crypto(self, crypto_name: str):
        """Implementation of abstract method from CryptoWatch"""
        self.watchedCrypto.append(crypto_name)

    def remove_crypto(self, crypto_name: str):
        """Implementation of abstract method from CryptoWatch"""
        self.watchedCrypto.remove(crypto_name)
        print(f"Removed {crypto_name} from the watch list")
    
    def notify_observers(self, crypto_id: str, crypto_data: dict):
        """Implementation of abstract method from CryptoWatch"""
        for observer in self.observers:
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
                            self.notify_observers(crypto_id, crypto_data)
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
        
        
                
    async def coins_list(self):

        
        url = "https://api.coingecko.com/api/v3/coins/list"
        
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

        else:
            print(f"Error fetching coins list: {response.status_code}")
            return None

    async def coin_data(self, coin_id: str):
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            self.notify_observers(coin_id, data)
            return data
        else:
            print(f"Error fetching coin data: {response.status_code}")
            return None
        
        
    async def linegraph_data(self, coin_id: str, time_range: int):
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=gbp&days={time_range}"
        

        
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()

            return data
        else:
            print(f"Error fetching line graph data: {response.status_code}")
            return None
        
    async def candlestick_data(self, coin_id:str, time_range: int):
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc?vs_currency=gbp&days={time_range}"
 
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error fetching candlestick data: {response.status_code}")
            return None