import asyncio
import os
import datetime
from Account import Account
from AccountType import Beginner, Advanced, Tester
from AuthenticationManager import AuthenticationManager
from AccountsFileManager import AccountsFileManager
from Wallet import Wallet
from CryptoWatch import CryptoWatch
from ExchangeSocket import ExchangeSocket
from CryptoTransactionStrategy import RealTransaction
from Transaction import Transaction
from TransactionLog import TransactionLog

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.total = 0
    
    def run_test(self, test_name, test_func):
        """Run a test and print the result"""
        self.total += 1
        print(f"\n{'=' * 80}")
        print(f"TEST {self.total}: {test_name}")
        print(f"{'-' * 80}")
        try:
            test_func()
            print(f"✅ PASSED: {test_name}")
            self.passed += 1
        except Exception as e:
            print(f"❌ FAILED: {test_name}")
            print(f"   Error: {str(e)}")
            self.failed += 1
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n{'=' * 80}")
        print(f"TEST SUMMARY: {self.passed}/{self.total} passed ({self.failed} failed)")
        print(f"{'=' * 80}")

class MockExchangeSocket(ExchangeSocket):
    """Mock implementation of ExchangeSocket for testing"""
    def __init__(self):
        super().__init__()
        self.prices = {
            "BTC-USD": 50000.0,
            "ETH-USD": 3000.0,
            "DOGE-USD": 0.25
        }
    
    async def connect_to_exchange_socket(self):
        print("Mock: Connected to exchange socket")
    
    async def disconnect_from_exchange_socket(self):
        print("Mock: Disconnected from exchange socket")
    
    async def get_crypto_price(self, crypto_name: str) -> float:
        if crypto_name in self.prices:
            print(f"Mock: Getting price for {crypto_name}: ${self.prices[crypto_name]}")
            return self.prices[crypto_name]
        print(f"Mock: Unknown crypto {crypto_name}, returning default price $100")
        return 100.0

async def run_tests():
    runner = TestRunner()
    
    # Test file setup
    test_file = "test_account.enc"
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Create mocks
    exchange_socket = MockExchangeSocket()
    
    # Test 1: Account Type Creation and Conversion
    def test_account_types():
        beginner = Beginner()
        advanced = Advanced()
        tester = Tester()
        
        assert beginner.get_type_name() == "Beginner"
        assert advanced.get_type_name() == "Advanced"
        assert tester.get_type_name() == "Tester"
        
        assert beginner.get_transaction_limit() == 1000.0
        assert advanced.get_transaction_limit() == float('inf')
        assert tester.get_transaction_limit() == 100.0
        
        # Test conversion
        new_advanced = beginner.switch_to_advanced()
        assert new_advanced.get_type_name() == "Advanced"
        
        new_beginner = advanced.switch_to_beginner()
        assert new_beginner.get_type_name() == "Beginner"
        
        print("Successfully tested account types and conversions")
    
    runner.run_test("Account Type Management", test_account_types)
    
    # Test 2: Account Creation and Serialization
    def test_account_creation():
        account = Account(account_type=Beginner())
        account.set_account_name("TestUser")
        account.set_secret_key("abc123")
        account.add_contact("Friend1", "0x123456789")
        
        # Verify account properties
        assert account.get_account_name() == "TestUser"
        assert account.get_secret_key() == "abc123"
        assert "Friend1" in account.get_contacts()
        
        # Test serialization
        json_data = account.to_json()
        print(f"Serialized account: {json_data}")
        
        # Test deserialization
        restored_account = Account(save_data=json_data)
        assert restored_account.get_account_name() == "TestUser"
        assert restored_account.get_secret_key() == "abc123"
        assert restored_account.get_contacts()["Friend1"] == "0x123456789"
        
        print("Successfully created, serialized and deserialized account")
    
    runner.run_test("Account Creation and Serialization", test_account_creation)
    
    # Test 3: Wallet and CryptoWatch Integration
    async def test_wallet_cryptowatch():
        # Create wallet
        wallet = Wallet("MyWallet")
        assert wallet.name == "MyWallet"
        
        # Create CryptoWatch
        crypto_watch = CryptoWatch("MainWatch", exchange_socket)
        
        # Link wallet to CryptoWatch
        wallet.link_to_watch(crypto_watch)
        assert wallet.watch == crypto_watch
        assert wallet in crypto_watch.wallets
        
        # Add cryptocurrencies to watch
        crypto_watch.add_crypto("BTC-USD")
        crypto_watch.add_crypto("ETH-USD")
        
        # Check crypto list
        assert len(crypto_watch.watchedCryptos) == 2
        crypto_names = [c.name for c in crypto_watch.watchedCryptos]
        assert "BTC-USD" in crypto_names
        assert "ETH-USD" in crypto_names
        
        # Update prices
        await crypto_watch.update_all_prices()
        
        # Check updated prices
        for crypto in crypto_watch.watchedCryptos:
            print(f"{crypto.name} price: ${crypto.conversion_rate}")
            assert crypto.conversion_rate > 0
            assert crypto.last_updated is not None
        
        print("Successfully tested Wallet and CryptoWatch integration")
    
    runner.run_test("Wallet and CryptoWatch Integration", 
                   lambda: asyncio.run(test_wallet_cryptowatch()))
    
    # Test 4: Transaction Strategy
    async def test_transactions():
        wallet = Wallet("TransactionWallet")
        transaction_strategy = RealTransaction(exchange_socket)
        
        # Test file operations
        test_holdings = {"BTC": 1.5, "ETH": 10.0}
        transaction_strategy.save_crypto_file(test_holdings, "test_crypto.csv")
        
        loaded_holdings = transaction_strategy.load_crypto_file("test_crypto.csv")
        assert loaded_holdings["BTC"] == 1.5
        assert loaded_holdings["ETH"] == 10.0
        
        # Test update operation
        transaction_strategy.update_crypto_file("BTC", 0.5, "test_crypto.csv")
        updated_holdings = transaction_strategy.load_crypto_file("test_crypto.csv")
        assert updated_holdings["BTC"] == 2.0
        
        # Test buy transaction
        buy_details = await transaction_strategy.prepare_buy_transaction(wallet, "DOGE-USD", 100)
        assert buy_details["type"] == "buy"
        assert buy_details["crypto_name"] == "DOGE-USD"
        assert buy_details["amount"] == 100
        assert buy_details["price"] == 0.25  # From our mock
        
        # Execute buy transaction
        success = await transaction_strategy.execute_buy_transaction(buy_details)
        assert success == True
        
        # Test sell transaction
        sell_details = await transaction_strategy.prepare_sell_transaction(wallet, "DOGE-USD", 50)
        assert sell_details["type"] == "sell"
        assert sell_details["crypto_name"] == "DOGE-USD"
        assert sell_details["amount"] == 50
        
        # Execute sell transaction
        success = await transaction_strategy.execute_sell_transaction(sell_details)
        assert success == True
        
        # Clean up test file
        if os.path.exists("test_crypto.csv"):
            os.remove("test_crypto.csv")
        
        print("Successfully tested transaction strategies")
    
    runner.run_test("Transaction Strategy", 
                   lambda: asyncio.run(test_transactions()))
    
    # Test 5: Transaction Log
    def test_transaction_log():
        log = TransactionLog()
        
        # Create a transaction
        timestamp = datetime.datetime.now()
        tx = Transaction(timestamp, 1.0, "0xabc123", "sender", "receiver", "BTC")
        
        # Add to log
        log.add_to_transaction_log(tx)
        
        # Search for transaction
        found_tx = log.search(timestamp, 1.0, "0xabc123", "receiver", "sender")
        
        # This should return None because receiver and sender are in wrong order
        assert found_tx is None
        
        # Correct search
        found_tx = log.search(timestamp, 1.0, "0xabc123", None, None)
        assert found_tx is not None
        
        print("Successfully tested transaction log")
    
    runner.run_test("Transaction Log", test_transaction_log)
    
    # Test 6: File Encryption and Decryption
    def test_file_encryption_decryption():
        # Setup test directory
        test_dir = "./test_files"
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
        
        # Create an account
        account = Account(account_type=Advanced())
        account.set_account_name("EncryptionTest")
        account.set_secret_key("secure123")
        
        # Get encryption key
        auth_manager = AuthenticationManager.get_instance()
        encryption_key = auth_manager._generate_key()
        
        # Encrypt and save
        file_manager = AccountsFileManager.get_instance()
        AccountsFileManager._encrypt_file(test_dir, encryption_key, account)
        
        # Verify file exists
        encrypted_file_path = os.path.join(test_dir, "EncryptionTest.enc")
        assert os.path.exists(encrypted_file_path)
        
        # Decrypt file
        decrypted_data = AccountsFileManager._decrypt_file(test_dir, encryption_key, "EncryptionTest")
        
        # Create new account from decrypted data
        restored_account = Account(save_data=decrypted_data)
        
        # Verify data integrity
        assert restored_account.get_account_name() == "EncryptionTest"
        assert restored_account.get_secret_key() == "secure123"
        assert restored_account.get_account_type().get_type_name() == "Advanced"
        
        # Clean up test files
        if os.path.exists(encrypted_file_path):
            os.remove(encrypted_file_path)
        if os.path.exists(test_dir):
            os.rmdir(test_dir)
        
        print("Successfully tested file encryption and decryption")
    
    runner.run_test("File Encryption and Decryption", test_file_encryption_decryption)
    
    # Print test summary
    runner.print_summary()

if __name__ == "__main__":
    asyncio.run(run_tests())