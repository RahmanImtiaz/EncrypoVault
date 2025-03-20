from AccountsFileManager import AccountsFileManager
from AuthenticationManager import AuthenticationManager
from src.crypto_impl.BitcoinWallet import BitcoinWallet


class WebviewAPI:
    authentication_manager: AuthenticationManager
    accounts_manager: AccountsFileManager
    def __init__(self):
        self.authentication_manager = AuthenticationManager().get_instance()
        self.accounts_manager = AccountsFileManager().get_instance()

    def get_accounts(self):
        accounts = self.accounts_manager.get_accounts()
        print(f"Returning accounts: {accounts}")
        return accounts

    def get_loaded_account(self):
        return self.accounts_manager.get_loaded_account().toJSON()

    def create_account(self, account_name, account_password, account_type):
        return self.accounts_manager.create_account(account_name, account_type, account_password)

    def create_bitcoin_wallet(self, wallet_name):
        btc_wallet = BitcoinWallet.create_wallet(wallet_name)
        return btc_wallet.toJSON()