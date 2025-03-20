from AccountsFileManager import AccountsFileManager
from AuthenticationManager import AuthenticationManager


class WebviewAPI:
    def __init__(self):
        self.authentication_manager = AuthenticationManager().get_instance()
        self.accounts_manager = AccountsFileManager().get_instance()

    def get_accounts(self):
        return self.accounts_manager.get_accounts()