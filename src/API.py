from webauthn import options_to_json
from webauthn.helpers.structs import PublicKeyCredentialRequestOptions, UserVerificationRequirement
import webauthn
import sys

from AccountsFileManager import AccountsFileManager
from AuthenticationManager import AuthenticationManager
from crypto_impl.BitcoinWallet import BitcoinWallet
from Portfolio import Portfolio

class WebviewAPI:
    authentication_manager: AuthenticationManager
    accounts_manager: AccountsFileManager
    def __init__(self):
        self.authentication_manager = AuthenticationManager().get_instance()
        self.accounts_manager = AccountsFileManager().get_instance()
        api_key = "fdade57267b549538799a94164f3db43"
        self.portfolio = Portfolio(api_key)

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
        
    def get_portfolio_balance(self):
        """Get the total balance of all wallets"""
        try:
            self.portfolio.update_all_balances()  # Refresh all balances before returning
            return self.portfolio.get_total_balance()
        except Exception as e:
            print(f"Error getting portfolio balance: {str(e)}")
            return 0
        

    def get_portfolio_wallets(self):
        """Get all wallets with their data"""
        try:
            self.portfolio.update_all_balances()
            
            wallets = self.portfolio.get_all_wallets()
            return [
                {
                    "name": wallet.name,
                    "balance": wallet.balance,
                    "address": wallet.address,
                    "coin_symbol": wallet.coin_symbol,
                    "holdings": self._format_holdings(wallet.holdings)
                }
                for wallet in wallets
            ]
        except Exception as e:
            print(f"Error getting wallets: {str(e)}")
            return []
        
    def _format_holdings(self, holdings):
        """Format holdings data for the frontend"""
        formatted = {}
        
        for crypto_id, data in holdings.items():
            # Get amount from the data
            amount = data.get("amount", 0)
            
            # Get crypto object if available
            crypto_obj = data.get("crypto", None)
            
            # Create default holding structure
            formatted[crypto_id] = {
                "amount": amount,
                "name": crypto_id.title(),  # Capitalize the ID as a fallback name
                "symbol": crypto_id.lower(),
                "value": 0  # Default value
            }
            
            # If we have a crypto object, use its data
            if crypto_obj:
                formatted[crypto_id]["name"] = crypto_obj.name
                formatted[crypto_id]["symbol"] = crypto_obj.symbol
                if hasattr(crypto_obj, 'current_price') and crypto_obj.current_price:
                    formatted[crypto_id]["value"] = amount * crypto_obj.current_price
                    
        return formatted
    
    def add_contact(self, contact_name, contact_address):
        """Add a contact to the wallet"""
        try:
            if self.accounts_manager.get_loaded_account() != None:
                self.accounts_manager.get_loaded_account().add_contact(contact_name, contact_address)
            return True
        except Exception as e:
            print(f"Error adding contact: {str(e)}")
            return False
        
    def get_contacts(self):
        """Get contacts for the current account"""
        try:
            if self.accounts_manager.get_loaded_account() != None:
                return self.accounts_manager.get_loaded_account().get_contacts()
            else:
                return []
        except Exception as e:
            print(f"Error getting contacts: {e}")
            return []