import os
import json
import asyncio
import aiofiles
import websockets
from gevent import threading


class PriceSocket:
    COINBASE_WS_URL = "wss://ws-feed.exchange.coinbase.com"
    
    _PriceSocket = None

    def __new__(cls):
        if cls._PriceSocket is None:
            cls._PriceSocket = super(PriceSocket, cls).__new__(cls)
            cls._PriceSocket._initialized = False
        return cls._PriceSocket

    def __init__(self):
        if getattr(self, '_initialized', False):
            return

        self.product_ids = ["BTC-GBP", "ETH-GBP"]
        self.ws = None
        self.session = False
        self.observers = []

        self.default_directory = os.path.expanduser("~/.EncryptoVault")
        self.current_directory = self.default_directory
        self.price_file = os.path.join(self.current_directory, "prices.json")
        self.price_cache = {}

        if os.path.exists(self.price_file):
            try:
                with open(self.price_file, 'r') as f:
                    self.price_cache = json.load(f)
            except json.JSONDecodeError:
                print("Failed to load price cache. Starting fresh.")
                self.price_cache = {}
        else:
            with open(self.price_file, 'w') as f:
                json.dump(self.price_cache, f)

        self.cache_task = None
        self._initialized = True

    def subcribe(self, observer):
        self.observers.append(observer)

    async def connect_to_exchange(self):
        try:
            self.ws = await websockets.connect(self.COINBASE_WS_URL)
            self.session = True
            print("Connected to Coinbase WebSocket")
            subscribe_message = {
                "type": "subscribe",
                "product_ids": self.product_ids,
                "channels": ["ticker"]
            }
            await self.ws.send(json.dumps(subscribe_message))
            print("Subscribed to channels")
            asyncio.create_task(self.listen_to_messages())

            self.cache_task = asyncio.create_task(self.update_price_cache_periodically())

        except Exception as e:
            print(f"Error connecting to exchange: {e}")
            self.session = False

    async def listen_to_messages(self):
        print("Listening for messages...")
        try:
            while self.session:
                message = await self.ws.recv()
                data = json.loads(message)
                if data.get("type") == "ticker":
                    crypto_id = data.get("product_id")
                    price = data.get("price")
                    if crypto_id and price:
                        self.price_cache[crypto_id] = price
        except websockets.exceptions.ConnectionClosed as e:
            print(f"WebSocket connection closed: {e}")
            self.session = False
        except Exception as e:
            print(f"Error listening to messages: {e}")
            self.session = False

    async def update_price_cache_periodically(self):
        if self.session:
            try:
                asyncio.create_task(self.save_price_cache())
                threading.Timer(10, self.update_price_cache_periodically).start()
            except asyncio.CancelledError:
                print("Cancelled")
            except Exception as e:
                print(f"Error updating price cache: {e}")

    async def save_price_cache(self):
        try:
            async with aiofiles.open(self.price_file, 'w') as f:
                await f.write(json.dumps(self.price_cache))
        except Exception as e:
            print(f"Error saving price cache: {e}")

    async def disconnect(self):
        self.session = False

        if self.cache_task and not self.cache_task.done():
            self.cache_task.cancel()
            try:
                await self.cache_task
            except asyncio.CancelledError:
                print("Cache task successfully cancelled.")

        if self.ws:
            try:
                await self.ws.close()
                print("WebSocket closed.")
            except Exception as e:
                print(f"Error closing WebSocket: {e}")

    def is_connected(self):
        return self.session
