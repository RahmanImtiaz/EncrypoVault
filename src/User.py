from typing import List, Optional
import os
from datetime import datetime

from AccountType import AccountType, Beginner, Advanced, Tester
from Account import Account
from AuthenticationManager import AuthenticationManager
from AccountsFileManager import AccountsFileManager
from AuditLog import AuditLog

class User:
    """
    User class for the EncryptoVault system.
    Represents the person using the system, providing authentication and account management.
    """
    
    def __init__(self):
        # User does not have explicit knowledge of AuthenticationManager (one-way association)
        self._accounts: List[Account] = []  # Aggregation with Account ("has-a" relationship)
        self._current_account: Optional[Account] = None
        self._auth_successful = False
    
    def login(self) -> bool:
        """ Attempt to log into the selected account """
        try:
            account_name = self._select_account()
            if not account_name:
                return False
            auth_manager = AuthenticationManager.get_instance()
            self._current_account = auth_manager.authenticate_account(account_name)
            
            if self._current_account:
                self._auth_successful = True
                return True
            return False
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False
    
    def register(self, account_name: str, account_type: AccountType) -> bool:
        """ Register a new account """
        try:
            # Create new account
            account = Account(account_type=account_type)
            account.set_account_name(account_name)
            
            # Prompt for authentication information
            auth_manager = AuthenticationManager.get_instance()
            password = auth_manager.prompt_for_password()
            biometrics = auth_manager.prompt_for_biometrics()
            
            # Generate encryption key
            encryption_key = auth_manager._generate_key(password, biometrics)

            account.set_encryption_key(encryption_key)
            
            # Save the account
            file_manager = AccountsFileManager.get_instance()
            file_manager.save_account(account)
            
            # Add to our accounts list
            self._accounts.append(account)
            
            AuditLog.get_instance().add_entry(account_name, datetime.now(), "ACCOUNT_CREATED")
            
            return True
        except Exception as e:
            print(f"Registration failed: {str(e)}")
            return False
    
    def _select_account(self) -> str:
        """ Select an account from available accounts """
        # In a real implementation, this would display UI for account selection and For now, its just to list available accounts and simulate selection
        file_manager = AccountsFileManager.get_instance()
        available_accounts = []
        
        try:
            for file in os.listdir(file_manager.current_directory):
                if file.endswith(".enc"):
                    account_name = os.path.splitext(file)[0]
                    available_accounts.append(account_name)
        except Exception as e:
            print(f"Error listing accounts: {str(e)}")
            return ""
            
        if not available_accounts:
            print("No accounts available")
            return ""
            
        # In a real implementation, this would show a UI for selection and For now is just returns the first account (if any)
        if available_accounts:
            return available_accounts[0]
        return ""
    
    def _select_account_type(self) -> AccountType:
        """ Select an account type """
        # UI for account type selection
        return Beginner() # default
    
    def get_current_account(self) -> Optional[Account]:
        """ Get the current authenticated account """
        return self._current_account if self._auth_successful else None
    
    def logout(self) -> None:
        """Log out of the current account"""
        if self._current_account:
            AuditLog.get_instance().add_entry(
                self._current_account.get_account_name(), 
                datetime.now(), 
                "LOGOUT"
            )
            
        self._current_account = None
        self._auth_successful = False