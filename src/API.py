from src.AccountsFileManager import AccountsFileManager
from src.AuthenticationManager import AuthenticationManager


class WebviewAPI:
    def __init__(self):

    def authenticate_account(self, account_name, password, biometrics):
        AuthenticationManager.authenticate_account(account_name, password, biometrics)

    def get_accounts(self):
        return AccountsFileManager.get_accounts()