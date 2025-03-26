from webauthn import options_to_json
from webauthn.helpers.structs import PublicKeyCredentialRequestOptions, UserVerificationRequirement

from AccountsFileManager import AccountsFileManager
from AuthenticationManager import AuthenticationManager
from crypto_impl.BitcoinWallet import BitcoinWallet
import webauthn
import sys

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
        if sys.platform == "darwin":
            from macos_touch_id import authenticate_with_touch_id
            if not authenticate_with_touch_id():
                print("Touch ID authentication failed")
                return False
        return self.authentication_manager.authenticate_account(account_name, password, biometrics)

    def create_account(self, account_name, account_password, account_type):
        return self.accounts_manager.create_account(account_name, account_type, account_password)

    def create_bitcoin_wallet(self, wallet_name):
        btc_wallet = BitcoinWallet.create_wallet(wallet_name)
        return btc_wallet.toJSON()

    def create_webauthn_auth_options(self) -> str:
        return options_to_json(webauthn.generate_authentication_options(challenge=bytes.fromhex("c99a420cd739ff56632d3262582df92c43d50bd64e045374422ca3ed68826e5e"), rp_id="localhost", user_verification=UserVerificationRequirement.REQUIRED))

    def create_webauthn_reg_options(self, account_name) -> str:
        return options_to_json(webauthn.generate_registration_options(challenge=bytes.fromhex("c99a420cd739ff56632d3262582df92c43d50bd64e045374422ca3ed68826e5e"), rp_id="localhost", rp_name=account_name, user_name=account_name))
    
    def get_platform(self):
        """Return the current platform: 'windows', 'macos', or 'other'"""
        if sys.platform == 'darwin':
            return 'macos'
        elif sys.platform == 'win32':
            return 'windows'
        else:
            return 'other'

    def authenticate_with_touch_id(self, account_name, password):
        """Authenticate specifically using Touch ID for macOS"""
        if sys.platform != 'darwin':
            return False
            
        from macos_touch_id import authenticate_with_touch_id
        biometric_result = authenticate_with_touch_id()
        
        if biometric_result == b'PASSWORD_FALLBACK':
            print("Touch ID unavailable, falling back to password authentication")
            try:
                account = self.authentication_manager.authenticate_account(
                    account_name, 
                    password
                )
                return bool(account)
            except Exception as e:
                print(f"Password authentication failed: {str(e)}")
                return False
        elif not biometric_result:
            print("Touch ID authentication failed")
            return False
            
        try:
            # Still need to verify the account/password
            account = self.authentication_manager.authenticate_account(
                account_name, 
                password, 
                b"touch_id_verified"  # Special marker for Touch ID
            )
            return bool(account)
        except Exception as e:
            print(f"Account authentication failed after Touch ID: {str(e)}")
            return False

        if biometric_result == b'PASSWORD_FALLBACK':
            print("Touch ID unavailable, falling back to password authentication")
            try:
                account = self.authentication_manager.authenticate_account(
                    account_name, 
                    password
                )
                return bool(account)
            except Exception as e:
                print(f"Password authentication failed: {str(e)}")
                return False