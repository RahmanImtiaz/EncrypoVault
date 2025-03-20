from AccountsFileManager import AccountsFileManager
from AuthenticationManager import AuthenticationManager


class WebviewAPI:
    authentication_manager: AuthenticationManager
    accounts_manager: AccountsFileManager
    def __init__(self):
        self.authentication_manager = AuthenticationManager().get_instance()
        self.accounts_manager = AccountsFileManager().get_instance()

    def get_accounts(self):
        return self.accounts_manager.get_accounts()

    def create_account(self, account_name, account_password, account_type):
        return self.accounts_manager.create_account(account_name, account_type, account_password)