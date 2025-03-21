from webauthn import options_to_json
from webauthn.helpers.structs import PublicKeyCredentialRequestOptions, UserVerificationRequirement

from AccountsFileManager import AccountsFileManager
from AuthenticationManager import AuthenticationManager
from crypto_impl.BitcoinWallet import BitcoinWallet
import webauthn

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
        return self.accounts_manager.get_loaded_account()

    def authenticate_account(self, account_name, password, biometrics):
        self.authentication_manager.authenticate_account(account_name, password, biometrics)

    def create_account(self, account_name, account_password, account_type):
        return self.accounts_manager.create_account(account_name, account_type, account_password)

    def create_bitcoin_wallet(self, wallet_name):
        btc_wallet = BitcoinWallet.create_wallet(wallet_name)
        return btc_wallet.toJSON()

    def create_webauthn_auth_options(self) -> str:
        return options_to_json(webauthn.generate_authentication_options(challenge=bytes.fromhex("c99a420cd739ff56632d3262582df92c43d50bd64e045374422ca3ed68826e5e"), rp_id="localhost", user_verification=UserVerificationRequirement.REQUIRED))

    def create_webauthn_reg_options(self, account_name) -> str:
        return options_to_json(webauthn.generate_registration_options(challenge=bytes.fromhex("c99a420cd739ff56632d3262582df92c43d50bd64e045374422ca3ed68826e5e"), rp_id="localhost", rp_name=account_name, user_name=account_name))
