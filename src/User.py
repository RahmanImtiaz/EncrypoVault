from typing import List, Optional, Dict, Any
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
        self._session_start_time: Optional[datetime] = None
        self._last_activity_time: Optional[datetime] = None
    
    def login(self) -> Dict[str, Any]:
        """ Attempt to log into the selected account """
        try:
            account_name = self._select_account()
            if not account_name:
                return False
            auth_manager = AuthenticationManager.get_instance()
            self._current_account = auth_manager.authenticate_account(account_name)
            
            if self._current_account:
                self._auth_successful = True
                self._session_start_time = datetime.now()
                self._last_activity_time = datetime.now()
                # Create success response with account details
                return {
                    "success": True,
                    "account": {
                        "name": self._current_account.get_account_name(),
                        "type": self._current_account.get_account_type().get_type_name(),
                        "transaction_limit": self._current_account.get_account_type().get_transaction_limit(),
                        "uses_real_funds": self._current_account.get_account_type().uses_real_funds(),
                        "contacts": self._current_account.get_contacts()
                    }
                }
            AuditLog.get_instance().add_entry(
                account_name if account_name else "unknown", 
                datetime.now(), 
                "AUTHENTICATION_FAILED"
            )
            return {"success": False, "error": "Authentication failed"}
        except Exception as e:
            AuditLog.get_instance().add_entry(
                account_name if account_name else "unknown", 
                datetime.now(), 
                "LOGIN_ERROR"
            )
            return {"success": False, "error": str(e)}
    
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
        
    def get_available_account_types(self) -> List[Dict[str, Any]]:
        """ Get information about available account types """
        return [
            {
                "name": "Beginner",
                "description": "Limited features, suitable for new users, has beginner resources",
                "transaction_limit": Beginner().get_transaction_limit(),
                "uses_real_funds": Beginner().uses_real_funds()
            },
            {
                "name": "Advanced",
                "description": "Full features for experienced users, including candle stick graphs",
                "transaction_limit": Advanced().get_transaction_limit(),
                "uses_real_funds": Advanced().uses_real_funds()
            },
            {
                "name": "Tester",
                "description": "Test account with fake funds and access to dev tools",
                "transaction_limit": Tester().get_transaction_limit(),
                "uses_real_funds": Tester().uses_real_funds()
            }
        ]
    
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
        # Update last activity timestamp
        self._last_activity_time = datetime.now()
        return self._current_account if self._auth_successful else None
    
    def logout(self) -> Dict[str, Any]:
        """ Log out of the current account """
        if not self._current_account:
            return {"success": False, "error": "No active session"}
        
        try:
            account_name = self._current_account.get_account_name()
            session_duration = (datetime.now() - self._session_start_time).total_seconds() if self._session_start_time else 0
            
            # Log the logout action
            AuditLog.get_instance().add_entry(
                account_name, 
                datetime.now(), 
                "LOGOUT"
            )
            
            # Clear all session data
            self._current_account = None
            self._auth_successful = False
            self._session_start_time = None
            self._last_activity_time = None
            
            return {
                "success": True, 
                "session": {
                    "account": account_name,
                    "duration": session_duration
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_session(self) -> Dict[str, Any]:
        """ Check if the current session is still valid """
        if not self._auth_successful or not self._current_account:
            return {"valid": False, "error": "No active session"}
        
        # Check session timeout (30 minutes of inactivity)
        if self._last_activity_time and (datetime.now() - self._last_activity_time).total_seconds() > 1800:
            self.logout()
            return {"valid": False, "error": "Session expired"}
        
        # Update last activity time
        self._last_activity_time = datetime.now()
        
        return {
            "valid": True,
            "account": self._current_account.get_account_name(),
            "type": self._current_account.get_account_type().get_type_name(),
            "session_duration": (datetime.now() - self._session_start_time).total_seconds() if self._session_start_time else 0
        }