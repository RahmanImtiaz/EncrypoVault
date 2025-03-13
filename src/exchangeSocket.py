class ExchangeSocket:
    def __init__(self):
        self.websocket_url = "wss://ws-feed.exchange.coinbase.com"
        self._connection = None

    async def connectToExchangeSocket(self):
        if not self._connection:
            self._connection = await websockets.connect(self.websocket_url)
            print("Connected to exchange socket.")

    async def disconnectFromExchangeSocket(self):
        if self._connection:
            await self._connection.close()
            self._connection = None
            print("Disconnected from exchange socket.")

    async def get_crypto_price(self, crypto_name: str) -> float:
        if not self._connection:
            await self.connectToExchangeSocket()

        subscribe_message = {
            "type": "subscribe",
            "product_ids": [crypto_name],
            "channels": ["ticker"]
        }
        await self._connection.send(json.dumps(subscribe_message))

        async for message in self._connection:
            data = json.loads(message)
            if data.get("type") == "ticker":
                price = float(data["price"])
                print(f"Received price for {crypto_name}: {price}")
                # Unsubscribe
                unsubscribe_message = {
                    "type": "unsubscribe",
                    "product_ids": [crypto_name],
                    "channels": ["ticker"]
                }
                await self._connection.send(json.dumps(unsubscribe_message))
                return price