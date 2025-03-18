import unittest
import asyncio
import datetime
import json
from unittest.mock import patch, MagicMock, AsyncMock
import io
from contextlib import redirect_stdout

from Wallet import Wallet
from Crypto import Crypto
from ExchangeSocket import ExchangeSocket
from Portfolio import Portfolio  # new import for Portfolio tests


class TestWallet(unittest.TestCase):
    def setUp(self):
        """Create a new Wallet instance for each test."""
        self.wallet = Wallet(name="TestWallet")

    def test_initial_state(self):
        """Test that the wallet initializes with correct default values."""
        self.assertEqual(self.wallet.balance, 0.0)
        self.assertIsNone(self.wallet.address)
        self.assertEqual(self.wallet.name, "TestWallet")
        self.assertEqual(self.wallet.holdings, {})

    def test_update_existing_crypto(self):
        """
        If the crypto is already in holdings, updating it should recalculate 
        its value (quantity * new_price).
        """
        # Initialize holdings with the correct dictionary structure
        self.wallet.holdings["BTC-USD"] = {"quantity": 2.0, "value": 0.0}

        # Update with a new price; expecting value = 2 * 30000
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.wallet.update("BTC-USD", 30000.0)
        output = buf.getvalue()
        self.assertIn("Updated BTC-USD value to 60000.0", output)
        self.assertEqual(self.wallet.holdings["BTC-USD"]["value"], 60000.0)

    def test_update_non_existent_crypto(self):
        """
        If the crypto is not in holdings, the wallet should print an error message.
        """
        if "BTC-USD" in self.wallet.holdings:
            del self.wallet.holdings["BTC-USD"]

        buf = io.StringIO()
        with redirect_stdout(buf):
            self.wallet.update("BTC-USD", 30000.0)
        output = buf.getvalue()
        self.assertIn("Could not update BTC-USD value", output)

    def test_update_zero_price(self):
        """
        Updating a crypto with zero price should set the holding value to 0 if it exists.
        """
        self.wallet.holdings["BTC-USD"] = {"quantity": 2.0, "value": 50000.0}
        self.wallet.update("BTC-USD", 0.0)
        self.assertEqual(self.wallet.holdings["BTC-USD"]["value"], 0.0)

    def test_update_negative_price(self):
        """
        Even though it's unlikely in real scenarios, test how the wallet handles a negative price.
        """
        self.wallet.holdings["BTC-USD"] = {"quantity": 2.0, "value": 50000.0}
        self.wallet.update("BTC-USD", -100.0)
        self.assertEqual(self.wallet.holdings["BTC-USD"]["value"], -200.0)

    def test_add_to_holdings_and_update(self):
        """
        Add a new crypto to the wallet's holdings and check that update works correctly.
        """
        self.wallet.holdings["ETH-USD"] = {"quantity": 5.0, "value": 0.0}
        self.wallet.update("ETH-USD", 1800.0)
        self.assertEqual(self.wallet.holdings["ETH-USD"]["value"], 9000.0)


class TestCrypto(unittest.TestCase):
    def setUp(self):
        """Create a new Crypto instance for each test."""
        self.crypto = Crypto(name="BTC-USD")

    def test_initial_state(self):
        """Test that the crypto initializes with correct default values."""
        self.assertEqual(self.crypto.name, "BTC-USD")
        self.assertEqual(self.crypto.conversion_rate, 0.0)
        self.assertIsNone(self.crypto.last_updated)

    def test_update_correct_crypto(self):
        """
        If the updated crypto name matches self.crypto.name,
        last_updated should be set and the correct message printed.
        """
        self.crypto.name = "BTC-USD"
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.crypto.update("BTC-USD", 25000.0)
        output = buf.getvalue()
        self.assertIn("Updated BTC-USD price to 25000.0", output)
        self.assertIsNotNone(self.crypto.last_updated)

    def test_update_incorrect_crypto(self):
        """
        If the updated crypto name does not match self.crypto.name,
        nothing should happen (last_updated remains None).
        """
        self.crypto.update("ETH-USD", 1800.0)
        self.assertIsNone(self.crypto.last_updated)

    def test_update_same_name_multiple_times(self):
        """
        Check if multiple updates correctly overwrite last_updated each time.
        """
        self.crypto.name = "BTC-USD"
        self.crypto.update("BTC-USD", 20000.0)
        first_update_time = self.crypto.last_updated
        self.assertIsNotNone(first_update_time)

        # Ensure a slight delay so the timestamp changes
        import time
        time.sleep(0.001)

        self.crypto.update("BTC-USD", 21000.0)
        second_update_time = self.crypto.last_updated
        self.assertGreater(second_update_time, first_update_time)


class TestExchangeSocket(unittest.TestCase):
    def setUp(self):
        """Create a new ExchangeSocket instance for each test."""
        self.exchange = ExchangeSocket(product_ids=["BTC-USD", "ETH-USD"])

    def test_initial_state(self):
        """Test that the ExchangeSocket initializes with correct default values."""
        self.assertIsNone(self.exchange._connection)
        self.assertEqual(self.exchange.host, "localhost")
        self.assertEqual(self.exchange.port, 8765)
        self.assertEqual(self.exchange.product_ids, ["BTC-USD", "ETH-USD"])
        self.assertEqual(self.exchange.watchedCrypto, [])
        self.assertIsNone(self.exchange.server)
        self.assertIsNone(self.exchange.coinbase_task)

    def test_add_remove_crypto(self):
        """Test adding and removing CryptoObserver objects from the watch list."""
        mock_observer = MagicMock()
        mock_observer.name = "MockObserver"
        self.exchange.add_crypto(mock_observer)
        self.assertIn(mock_observer, self.exchange.watchedCrypto)
        self.exchange.remove_crypto(mock_observer)
        self.assertNotIn(mock_observer, self.exchange.watchedCrypto)

    def test_add_duplicate_crypto(self):
        """Ensure that adding the same observer twice does not duplicate entries."""
        mock_observer = MagicMock()
        mock_observer.name = "MockObserver"
        self.exchange.add_crypto(mock_observer)
        self.exchange.add_crypto(mock_observer)
        self.assertEqual(self.exchange.watchedCrypto.count(mock_observer), 1)

    def test_remove_nonexistent_crypto(self):
        """Removing a crypto observer that isn't in the list should do nothing."""
        mock_observer = MagicMock()
        mock_observer.name = "MockObserver"
        self.exchange.remove_crypto(mock_observer)
        self.assertNotIn(mock_observer, self.exchange.watchedCrypto)

    def test_notify_observers(self):
        """Test that notifyObservers calls update on all watchers."""
        mock_observer1 = MagicMock()
        mock_observer1.name = "MockObserver1"
        mock_observer2 = MagicMock()
        mock_observer2.name = "MockObserver2"
        self.exchange.add_crypto(mock_observer1)
        self.exchange.add_crypto(mock_observer2)
        self.exchange.notifyObservers("BTC-USD", 30000.0)
        mock_observer1.update.assert_called_with("BTC-USD", 30000.0)
        mock_observer2.update.assert_called_with("BTC-USD", 30000.0)

    @patch('websockets.connect')
    def test_connect_to_coinbase(self, mock_connect):
        """
        Test that connect_to_coinbase subscribes to the product_ids and 
        notifies observers upon receiving ticker data.
        """
        fake_ws = AsyncMock()
        fake_ws.__aenter__.return_value = fake_ws
        fake_ws.__aexit__.return_value = None

        async def fake_async_gen():
            yield '{"type": "ticker", "product_id": "BTC-USD", "price": "28000.00"}'
            yield '{"type": "ticker", "product_id": "ETH-USD", "price": "1800.00"}'
            raise asyncio.CancelledError()

        fake_ws.__aiter__ = lambda *args, **kwargs: fake_async_gen()
        mock_connect.return_value = fake_ws

        mock_observer = MagicMock()
        mock_observer.name = "MockObserver"
        self.exchange.add_crypto(mock_observer)

        async def run_test():
            try:
                await self.exchange.connect_to_coinbase()
            except asyncio.CancelledError:
                pass

        asyncio.run(run_test())
        mock_observer.update.assert_any_call("BTC-USD", 28000.0)
        mock_observer.update.assert_any_call("ETH-USD", 1800.0)

    @patch('websockets.connect')
    def test_connectToExchangeSocket_and_disconnect(self, mock_connect):
        """
        Test connectToExchangeSocket starts the coinbase task 
        and disconnectFromExchangeSocket cancels it.
        """
        fake_ws = AsyncMock()
        fake_ws.__aenter__.return_value = fake_ws
        fake_ws.__aexit__.return_value = None

        async def fake_async_gen():
            yield '{"type": "ticker", "product_id": "BTC-USD", "price": "29000.00"}'
            while True:
                await asyncio.sleep(0.1)

        fake_ws.__aiter__ = lambda *args, **kwargs: fake_async_gen()
        mock_connect.return_value = fake_ws

        async def run_test():
            task = asyncio.create_task(self.exchange.connectToExchangeSocket())
            await asyncio.sleep(0.1)  # Allow connection to establish
            await self.exchange.disconnectFromExchangeSocket()
            try:
                await task
            except asyncio.CancelledError:
                pass

        asyncio.run(run_test())
        self.assertIsNone(self.exchange.coinbase_task, "coinbase_task should be None after disconnect.")

    @patch('websockets.connect')
    def test_non_ticker_messages_ignored(self, mock_connect):
        """
        Test that messages not of type 'ticker' do not trigger notifyObservers.
        """
        fake_ws = AsyncMock()
        fake_ws.__aenter__.return_value = fake_ws
        fake_ws.__aexit__.return_value = None

        async def fake_async_gen():
            yield '{"type": "subscriptions", "channels": [{"name": "ticker","product_ids": ["BTC-USD"]}]}'
            yield '{"type": "ticker", "product_id": "BTC-USD", "price": "28000.00"}'
            yield '{"type": "ticker", "product_id": "BTC-USD"}'
            raise asyncio.CancelledError()

        fake_ws.__aiter__ = lambda *args, **kwargs: fake_async_gen()
        mock_connect.return_value = fake_ws

        mock_observer = MagicMock()
        mock_observer.name = "MockObserver"
        self.exchange.add_crypto(mock_observer)

        async def run_test():
            try:
                await self.exchange.connect_to_coinbase()
            except asyncio.CancelledError:
                pass

        asyncio.run(run_test())
        # Only one valid ticker message should trigger an update
        mock_observer.update.assert_called_once_with("BTC-USD", 28000.0)


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        """Create a new Portfolio instance for each test."""
        self.portfolio = Portfolio(name="MyPortfolio")

    def test_initial_state(self):
        """Test that the portfolio initializes with correct default values."""
        self.assertEqual(self.portfolio.name, "MyPortfolio")
        self.assertEqual(self.portfolio.wallets, [])
        self.assertEqual(self.portfolio.total_balance, 0.0)
        self.assertEqual(self.portfolio.get_total_balance(), 0.0)

    def test_add_wallet(self):
        """Test that a wallet is added to the portfolio."""
        wallet = Wallet(name="Wallet1")
        wallet.balance = 150.0
        self.portfolio.add_wallet(wallet)
        self.assertIn(wallet, self.portfolio.wallets)

    def test_remove_wallet(self):
        """Test that a wallet is removed from the portfolio."""
        wallet = Wallet(name="Wallet1")
        self.portfolio.add_wallet(wallet)
        self.portfolio.remove_wallet(wallet)
        self.assertNotIn(wallet, self.portfolio.wallets)

    def test_update_total_balance(self):
        """
        Test that update_total_balance sums up the balance of all wallets.
        With the updated implementation, repeated calls do not accumulate.
        """
        wallet1 = Wallet(name="Wallet1")
        wallet1.balance = 100.0
        wallet2 = Wallet(name="Wallet2")
        wallet2.balance = 200.0
        self.portfolio.add_wallet(wallet1)
        self.portfolio.add_wallet(wallet2)
        
        # After one update, total_balance should be 300.0
        self.portfolio.update_total_balance()
        self.assertEqual(self.portfolio.get_total_balance(), 300.0)

    def test_update_total_balance_multiple_calls(self):
        """
        Test that multiple calls to update_total_balance yield the same result,
        because the method resets the total_balance before summing.
        """
        wallet = Wallet(name="Wallet1")
        wallet.balance = 50.0
        self.portfolio.add_wallet(wallet)
        self.portfolio.update_total_balance()  # total_balance becomes 50.0
        first_total = self.portfolio.get_total_balance()
        self.assertEqual(first_total, 50.0)
        
        self.portfolio.update_total_balance()  # Should still be 50.0 after reset
        self.assertEqual(self.portfolio.get_total_balance(), 50.0)


if __name__ == '__main__':
    unittest.main()
