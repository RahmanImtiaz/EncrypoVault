import abc, json
from abc import abstractmethod
import asyncio
from Crypto import Crypto
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
    
    coinbase_URL = "wss://ws-feed.exchange.coinbase.com"
    def __init__(self, product_ids = None, hosts = "localhost", port = 8765):
        super().__init__()
        self._connection = None
        self.host = hosts
        self.port = port
        self.product_ids = product_ids
        self.server = None
        self.coinbase_task = None
        
    def add_crypto(self, observer: CryptoObserver):
        if observer not in self.watchedCrypto:
            self.watchedCrypto.append(observer)
            print("Added " + observer.name + " to the watchlist")
    
    def remove_crypto(self, observer: CryptoObserver):
        if observer in self.watchedCrypto:
            self.watchedCrypto.remove(observer)
            print("Removed " + observer.name + " from the watch list")
    
    def notifyObservers(self, crypto_name: str, new_price: float):
        for observer in self.watchedCrypto:
            observer.update(crypto_name, new_price)

    
    async def connect_to_coinbase(self):
        async with websockets.connect(self.coinbase_URL) as websocket:
            subscribe_message = {
                "type": "subscribe",
                "product_ids": self.product_ids,
                "channels": ["ticker"]
            }
            await websocket.send(json.dumps(subscribe_message))
            
            print("Subscribed to " + str(self.product_ids))
            
            async for message in websocket:
                data = json.loads(message)
                if data.get("type") == "ticker":
                    product_id = data.get("product_id")                        
                    price = (data.get("price"))
                    if not price:
                        return
                    price = float(price)
                    if price and product_id:
                        print("Received " + product_id + " price: " + str(price))
                        self.notifyObservers(product_id, price)
    
    async def connectToExchangeSocket(self):
        self.coinbase_task = asyncio.create_task(self.connect_to_coinbase())
        await self.coinbase_task
    
    async def disconnectFromExchangeSocket(self):
        if self.coinbase_task:
            self.coinbase_task.cancel()
            try:
                await self.coinbase_task
            except asyncio.CancelledError:
                print("Task was cancelled")
            self.coinbase_task = None
            print("Disconnected from the exchange")
