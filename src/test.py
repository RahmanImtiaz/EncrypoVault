import asyncio
import os
import json
import time
import datetime
import shutil
from colorama import init, Fore, Style

# Import application components
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
from Crypto import Crypto

# Initialize colorama for colored output
init(autoreset=True)

class TestResult:
    """Constants for test result formatting"""
    PASS = f"{Fore.GREEN}✓ PASS{Style.RESET_ALL}"
    FAIL = f"{Fore.RED}✗ FAIL{Style.RESET_ALL}"
    INFO = f"{Fore.BLUE}ℹ INFO{Style.RESET_ALL}"
    WARNING = f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL}"

class MockExchangeSocket(ExchangeSocket):
    """Mock implementation of ExchangeSocket for testing"""
    def __init__(self):
        super().__init__()
        # Define some mock crypto prices
        self.mock_prices = {
            "BTC-USD": 65000.0,
            "ETH-USD": 3500.0,
            "SOL-USD": 150.0,
            "DOGE-USD": 0.12,
            "XRP-USD": 0.50
        }
        self.connected = False
    
    async def connect_to_exchange_socket(self):
        self.connected = True
        print(f"{TestResult.INFO} Mock exchange socket connected")
        return True
        
    async def disconnect_from_exchange_socket(self):
        self.connected = False
        print(f"{TestResult.INFO} Mock exchange socket disconnected")
        return True
        
    async def get_crypto_price(self, crypto_name: str) -> float:
        if not self.connected:
            await self.connect_to_exchange_socket()
            
        price = self.mock_prices.get(crypto_name, 100.0)  # Default price for unknown tokens
        print(f"{TestResult.INFO} Mock price for {crypto_name}: ${price}")
        return price

class TestAuthenticationManager(AuthenticationManager):
    """Test version of AuthenticationManager that bypasses actual authentication"""
    
    def prompt_for_password(self):
        return "test_password123"
    
    def prompt_for_biometrics(self):
        return "test_biometric_data"
    
    def _generate_key(self, password=None, biometrics=None):
        # For testing: return a deterministic key
        return b'test_key_for_encryption_purposes_1234'
    
    def ensure_secure_boot(self):
        return True

def section_header(title):
    """Print a section header"""
    print(f"\n{Fore.CYAN}{'=' * 80}")
    print(f"{Fore.CYAN}[ {title} ]")
    print(f"{Fore.CYAN}{'-' * 80}")

def subsection_header(title):
    """Print a subsection header"""
    print(f"\n{Fore.CYAN}[ {title} ]")
    print(f"{Fore.CYAN}{'-' * 40}")

async def run_tests():
    """Run all tests"""
    # Track test statistics
    tests_run = 0
    tests_passed = 0
    tests_failed = 0
    
    # Set up test environment
    test_dir = "./test_data"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    # Replace singletons with test versions
    AuthenticationManager._AuthenticationManager = TestAuthenticationManager()
    auth_manager = AuthenticationManager.get_instance()
    
    file_manager = AccountsFileManager.get_instance()
    file_manager.current_directory = test_dir
    
    # Create mock exchange socket
    exchange_socket = MockExchangeSocket()
    
    # Test helper function
    def run_test(name, test_function):
        nonlocal tests_run, tests_passed, tests_failed
        tests_run += 1
        
        subsection_header(name)
        start_time = time.time()
        
        try:
            test_function()
            end_time = time.time()
            print(f"{TestResult.PASS} {name} ({(end_time - start_time):.2f}s)")
            tests_passed += 1
        except Exception as e:
            print(f"{TestResult.FAIL} {name}")
            print(f"  Error: {e}")
            tests_failed += 1
            
    # Test helper function for async tests
    async def run_async_test(name, test_function):
        nonlocal tests_run, tests_passed, tests_failed
        tests_run += 1
        
        subsection_header(name)
        start_time = time.time()
        
        try:
            await test_function()
            end_time = time.time()
            print(f"{TestResult.PASS} {name} ({(end_time - start_time):.2f}s)")
            tests_passed += 1
        except Exception as e:
            print(f"{TestResult.FAIL} {name}")
            print(f"  Error: {e}")
            tests_failed += 1
    
    # ===== 1. ACCOUNT MANAGEMENT TESTS =====
    section_header("ACCOUNT MANAGEMENT TESTS")
    
    def test_create_account():
        """Test creating accounts with different types"""
        # Create accounts with different types
        beginner = Account(account_type=Beginner())
        advanced = Account(account_type=Advanced())
        tester = Account(account_type=Tester())
        
        # Set account details
        beginner.set_account_name("TestBeginner")
        advanced.set_account_name("TestAdvanced")
        tester.set_account_name("TestTester")
        
        beginner.set_secret_key("BeginnerSecret123")
        advanced.set_secret_key("AdvancedSecret456")
        tester.set_secret_key("TesterSecret789")
        
        # Add contacts
        beginner.add_contact("Bob", "0x123456789abcdef")
        advanced.add_contact("Alice", "0xfedcba987654321")
        
        # Verify account properties
        assert beginner.get_account_name() == "TestBeginner"
        assert advanced.get_account_name() == "TestAdvanced"
        assert tester.get_account_name() == "TestTester"
        
        assert beginner.get_account_type().get_type_name() == "Beginner"
        assert advanced.get_account_type().get_type_name() == "Advanced"
        assert tester.get_account_type().get_type_name() == "Tester"
        
        assert beginner.get_contacts()["Bob"] == "0x123456789abcdef"
        assert advanced.get_contacts()["Alice"] == "0xfedcba987654321"
        
        print(f"{TestResult.INFO} Created 3 accounts: Beginner, Advanced, and Tester")
    
    def test_account_serialization():
        """Test account serialization to JSON and back"""
        # Create an account and set its properties
        account = Account(account_type=Advanced())
        account.set_account_name("SerializeTest")
        account.set_secret_key("SerializeSecret123")
        account.add_contact("Contact1", "0xabcd1234")
        
        # Serialize to JSON
        json_data = account.to_json()
        print(f"{TestResult.INFO} Serialized account: {json_data}")
        
        # Deserialize from JSON
        new_account = Account(save_data=json_data)
        
        # Verify properties were preserved
        assert new_account.get_account_name() == "SerializeTest"
        assert new_account.get_secret_key() == "SerializeSecret123"
        assert new_account.get_contacts()["Contact1"] == "0xabcd1234"
        assert new_account.get_account_type().get_type_name() == "Advanced"
        
        print(f"{TestResult.INFO} Successfully deserialized account")
    
    def test_account_type_switching():
        """Test switching between account types"""
        # Create an account with Beginner type
        account = Account(account_type=Beginner())
        
        # Test initial type
        assert account.get_account_type().get_type_name() == "Beginner"
        assert account.get_account_type().get_transaction_limit() == 1000.0
        assert account.get_account_type().uses_real_funds() == True
        
        # Switch to Advanced
        account.set_account_type(account.get_account_type().switch_to_advanced())
        
        # Test new type
        assert account.get_account_type().get_type_name() == "Advanced" 
        assert account.get_account_type().get_transaction_limit() == float('inf')
        assert account.get_account_type().uses_real_funds() == True
        
        # Switch back to Beginner
        account.set_account_type(account.get_account_type().switch_to_beginner())
        
        # Test switched back type
        assert account.get_account_type().get_type_name() == "Beginner"
        assert account.get_account_type().get_transaction_limit() == 1000.0
        
        print(f"{TestResult.INFO} Successfully switched account types")
    
    # Run account management tests
    run_test("Create Account", test_create_account)
    run_test("Account Serialization", test_account_serialization)
    run_test("Account Type Switching", test_account_type_switching)
    
    # ===== 2. AUTHENTICATION AND FILE OPERATIONS TESTS =====
    section_header("AUTHENTICATION AND FILE OPERATIONS TESTS")
    
    def test_encrypt_decrypt_file():
        """Test encrypting and decrypting files"""
        # Create an account
        account = Account(account_type=Beginner())
        account.set_account_name("FileTestAccount")
        account.set_secret_key("SecureKey123")
        account.add_contact("FileContact", "0x67890abcdef")
        
        # Get encryption key from authentication manager
        encryption_key = auth_manager._generate_key()
        
        # Encrypt and save the account
        AccountsFileManager._encrypt_file(test_dir, encryption_key, account)
        
        # Verify the file exists
        encrypted_file = os.path.join(test_dir, "FileTestAccount.enc")
        assert os.path.exists(encrypted_file)
        print(f"{TestResult.INFO} Encrypted file created at {encrypted_file}")
        
        # Now decrypt it
        decrypted_data = AccountsFileManager._decrypt_file(test_dir, encryption_key, "FileTestAccount")
        
        # Create a new account from decrypted data
        restored_account = Account(save_data=decrypted_data)
        
        # Verify properties match original
        assert restored_account.get_account_name() == "FileTestAccount"
        assert restored_account.get_secret_key() == "SecureKey123"
        assert restored_account.get_contacts()["FileContact"] == "0x67890abcdef"
        
        print(f"{TestResult.INFO} Successfully decrypted and restored account data")
    
    async def test_authentication():
        """Test the authentication process"""
        # Create an account
        account = Account(account_type=Advanced())
        account.set_account_name("AuthTest")
        account.set_secret_key("AuthSecret")
        
        # Save the account with our test key
        encryption_key = auth_manager._generate_key()
        AccountsFileManager._encrypt_file(test_dir, encryption_key, account)
        
        # Now try to authenticate
        try:
            # This will use the mock authentication manager
            authenticated_account = auth_manager.authenticate_account("AuthTest")
            print(f"{TestResult.INFO} Authentication successful")
            
            # Verify the account details
            assert authenticated_account.get_account_name() == "AuthTest"
            assert authenticated_account.get_secret_key() == "AuthSecret"
            
        except Exception as e:
            # Note: Our mock authentication should succeed, so if we get here
            # it's due to an implementation issue in our test
            print(f"{TestResult.FAIL} Authentication failed: {e}")
            raise e
    
    # Run authentication and file tests
    run_test("Encrypt and Decrypt Files", test_encrypt_decrypt_file)
    await run_async_test("Authentication Process", test_authentication)
    
    # ===== 3. WALLET TESTS =====
    section_header("WALLET TESTS")
    
    def test_create_wallet():
        """Test creating wallets"""
        # Create multiple wallets
        wallet1 = Wallet("Main Wallet")
        wallet2 = Wallet("Savings Wallet")
        wallet3 = Wallet("Trading Wallet")
        
        # Set properties
        wallet1.address = "0xwallet1address"
        wallet2.address = "0xwallet2address"
        wallet3.address = "0xwallet3address"
        
        wallet1.balance = 1.5
        wallet2.balance = 3.0
        wallet3.balance = 0.5
        
        # Verify properties
        assert wallet1.name == "Main Wallet"
        assert wallet1.address == "0xwallet1address"
        assert wallet1.balance == 1.5
        
        assert wallet2.name == "Savings Wallet"
        assert wallet3.name == "Trading Wallet"
        
        print(f"{TestResult.INFO} Created wallets with the following balances:")
        print(f"  - {wallet1.name}: {wallet1.balance} BTC")
        print(f"  - {wallet2.name}: {wallet2.balance} BTC")
        print(f"  - {wallet3.name}: {wallet3.balance} BTC")
    
    async def test_cryptowatch_integration():
        """Test linking wallets with CryptoWatch"""
        # Create wallets and crypto watch
        wallet = Wallet("Watch Test Wallet")
        watch = CryptoWatch("Test Watch", exchange_socket)
        
        # Link wallet to watch
        wallet.link_to_watch(watch)
        
        # Verify linkage
        assert wallet.watch == watch
        assert wallet in watch.wallets
        
        # Add cryptocurrencies to watch
        watch.add_crypto("BTC-USD")
        watch.add_crypto("ETH-USD")
        watch.add_crypto("SOL-USD")
        
        # Update prices
        await watch.update_all_prices()
        
        # Check cryptocurrencies and their prices
        for crypto in watch.watchedCryptos:
            assert crypto.conversion_rate > 0
            assert crypto.last_updated is not None
            print(f"{TestResult.INFO} {crypto.name} price: ${crypto.conversion_rate}")
        
        # Test removing crypto from watch
        watch.remove_crypto("SOL-USD")
        crypto_names = [c.name for c in watch.watchedCryptos]
        assert "SOL-USD" not in crypto_names
        assert len(crypto_names) == 2
        
        print(f"{TestResult.INFO} Successfully linked wallet with CryptoWatch")
    
    # Run wallet tests
    run_test("Create Wallet", test_create_wallet)
    await run_async_test("CryptoWatch Integration", test_cryptowatch_integration)
    
    # ===== 4. TRANSACTION TESTS =====
    section_header("TRANSACTION TESTS")
    
    async def test_transaction_buy_sell():
        """Test buying and selling crypto"""
        wallet = Wallet("Transaction Test Wallet")
        transaction_strategy = RealTransaction(exchange_socket)
        
        # Set up a test file
        test_file = os.path.join(test_dir, "crypto_holdings.csv")
        
        # Test saving crypto file
        initial_holdings = {"BTC": 1.0, "ETH": 5.0}
        transaction_strategy.save_crypto_file(initial_holdings, test_file)
        print(f"{TestResult.INFO} Created initial holdings file")
        
        # Test loading crypto file
        loaded_holdings = transaction_strategy.load_crypto_file(test_file)
        assert loaded_holdings["BTC"] == 1.0
        assert loaded_holdings["ETH"] == 5.0
        print(f"{TestResult.INFO} Successfully loaded holdings: {loaded_holdings}")
        
        # Test preparing buy transaction
        buy_details = await transaction_strategy.prepare_buy_transaction(wallet, "BTC-USD", 0.5)
        assert buy_details["type"] == "buy"
        assert buy_details["crypto_name"] == "BTC-USD"
        assert buy_details["amount"] == 0.5
        assert buy_details["price"] == 65000.0  # From our mock
        
        print(f"{TestResult.INFO} Prepared buy transaction:")
        print(f"  - Crypto: {buy_details['crypto_name']}")
        print(f"  - Amount: {buy_details['amount']} BTC")
        print(f"  - Price: ${buy_details['price']}/BTC")
        print(f"  - Total Cost: ${buy_details['cost']}")
        
        # Execute buy transaction
        success = await transaction_strategy.execute_buy_transaction(buy_details)
        assert success == True
        
        # Update holdings file for testing
        transaction_strategy.update_crypto_file("BTC", 0.5, test_file)
        updated_holdings = transaction_strategy.load_crypto_file(test_file)
        assert updated_holdings["BTC"] == 1.5  # 1.0 + 0.5
        print(f"{TestResult.INFO} Holdings after buy: {updated_holdings}")
        
        # Test preparing sell transaction
        sell_details = await transaction_strategy.prepare_sell_transaction(wallet, "BTC-USD", 0.2)
        assert sell_details["type"] == "sell"
        assert sell_details["crypto_name"] == "BTC-USD"
        assert sell_details["amount"] == 0.2
        assert sell_details["price"] == 65000.0
        
        print(f"{TestResult.INFO} Prepared sell transaction:")
        print(f"  - Crypto: {sell_details['crypto_name']}")
        print(f"  - Amount: {sell_details['amount']} BTC")
        print(f"  - Price: ${sell_details['price']}/BTC")
        print(f"  - Total Proceeds: ${sell_details['proceeds']}")
        
        # Execute sell transaction
        success = await transaction_strategy.execute_sell_transaction(sell_details)
        assert success == True
        
        # Update holdings file for testing
        transaction_strategy.update_crypto_file("BTC", -0.2, test_file)
        final_holdings = transaction_strategy.load_crypto_file(test_file)
        assert final_holdings["BTC"] == 1.3  # 1.5 - 0.2
        print(f"{TestResult.INFO} Holdings after sell: {final_holdings}")
    
    def test_transaction_logging():
        """Test transaction logging functionality"""
        # Create a transaction log
        log = TransactionLog()
        
        # Create some test transactions
        tx1_time = datetime.datetime.now()
        tx1 = Transaction(tx1_time, 0.5, "0xtx1hash", "Alice", "Bob", "BTC")
        
        tx2_time = datetime.datetime.now()
        tx2 = Transaction(tx2_time, 1.0, "0xtx2hash", "Bob", "Charlie", "ETH")
        
        # Add transactions to log
        log.add_to_transaction_log(tx1)
        log.add_to_transaction_log(tx2)
        
        # Check log contents
        assert len(log._log) == 2
        
        # Print log contents
        print(f"{TestResult.INFO} Transaction log contains {len(log._log)} entries:")
        for tx in log._log:
            print(f"  - {tx}")
            
        # Note: The current TransactionLog.search() implementation looks for sentTo and sentBy
        # fields, but the Transaction class uses sender and receiver fields.
        # This is a bug in the application code.
        print(f"{TestResult.WARNING} TransactionLog.search() has a field mismatch with Transaction class")
        print(f"  - TransactionLog.search looks for: sentTo, sentBy")
        print(f"  - Transaction class uses: sender, receiver")
    
    # Run transaction tests
    await run_async_test("Buy and Sell Transactions", test_transaction_buy_sell)
    run_test("Transaction Logging", test_transaction_logging)
    
    # ===== 5. COMPREHENSIVE INTEGRATION TEST =====
    section_header("INTEGRATION TEST")
    
    async def test_full_workflow():
        """Test a full user workflow"""
        print(f"{TestResult.INFO} Starting full workflow test")
        
        # 1. Create an account
        account = Account(account_type=Advanced())
        account.set_account_name("IntegrationTest")
        account.set_secret_key("IntegrationKey123")
        
        # 2. Save account to encrypted file
        encryption_key = auth_manager._generate_key()
        AccountsFileManager._encrypt_file(test_dir, encryption_key, account)
        print(f"{TestResult.INFO} Created and saved account")
        
        # 3. Create a wallet for the account
        wallet = Wallet("Integration Wallet")
        wallet.address = "0xintegrationwallet"
        wallet.balance = 2.0
        print(f"{TestResult.INFO} Created wallet with 2.0 BTC")
        
        # 4. Set up crypto watch
        watch = CryptoWatch("Integration Watch", exchange_socket)
        wallet.link_to_watch(watch)
        watch.add_crypto("BTC-USD")
        watch.add_crypto("ETH-USD")
        
        # 5. Update crypto prices
        await watch.update_all_prices()
        crypto_prices = {c.name: c.conversion_rate for c in watch.watchedCryptos}
        print(f"{TestResult.INFO} Current crypto prices: {crypto_prices}")
        
        # 6. Perform transactions
        transaction_strategy = RealTransaction(exchange_socket)
        holdings_file = os.path.join(test_dir, "integration_holdings.csv")
        
        # Initial holdings
        initial_holdings = {"BTC": 2.0, "ETH": 10.0}
        transaction_strategy.save_crypto_file(initial_holdings, holdings_file)
        
        # Buy some BTC
        buy_tx = await transaction_strategy.prepare_buy_transaction(wallet, "BTC-USD", 0.5)
        await transaction_strategy.execute_buy_transaction(buy_tx)
        transaction_strategy.update_crypto_file("BTC", 0.5, holdings_file)
        
        # Sell some ETH
        sell_tx = await transaction_strategy.prepare_sell_transaction(wallet, "ETH-USD", 2.0)
        await transaction_strategy.execute_sell_transaction(sell_tx)
        transaction_strategy.update_crypto_file("ETH", -2.0, holdings_file)
        
        # Check final holdings
        final_holdings = transaction_strategy.load_crypto_file(holdings_file)
        print(f"{TestResult.INFO} Final holdings after transactions: {final_holdings}")
        assert final_holdings["BTC"] == 2.5
        assert final_holdings["ETH"] == 8.0
        
        # 7. Create transaction log entries
        log = TransactionLog()
        tx1 = Transaction(datetime.datetime.now(), 0.5, "0xbuytx", "Exchange", wallet.name, "BTC")
        tx2 = Transaction(datetime.datetime.now(), 2.0, "0xselltx", wallet.name, "Exchange", "ETH")
        
        log.add_to_transaction_log(tx1)
        log.add_to_transaction_log(tx2)
        print(f"{TestResult.INFO} Added 2 transactions to the log")
        
        print(f"{TestResult.PASS} Full workflow test completed successfully")
    
    # Run integration test
    await run_async_test("Full User Workflow", test_full_workflow)
    
    # ===== PRINT FINAL SUMMARY =====
    section_header("TEST SUMMARY")
    print(f"Total Tests Run: {tests_run}")
    print(f"Tests Passed: {Fore.GREEN}{tests_passed}{Style.RESET_ALL}")
    print(f"Tests Failed: {Fore.RED if tests_failed > 0 else ''}{tests_failed}{Style.RESET_ALL}")
    
    if tests_failed == 0:
        print(f"\n{Fore.GREEN}All tests passed!{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}Some tests failed. Please review the output.{Style.RESET_ALL}")
    
    # Clean up test directory
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
        print(f"\n{TestResult.INFO} Cleaned up test directory")

if __name__ == "__main__":
    print(f"{Fore.CYAN}{'=' * 80}")
    print(f"{Fore.CYAN}EncryptoVault Test Suite")
    print(f"{Fore.CYAN}{'=' * 80}")
    
    # Run all tests
    asyncio.run(run_tests())