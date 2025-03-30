import json
from AccountType import AccountType, Beginner, Advanced, Tester

class Account:
    def __init__(self, save_data=None, account_type=None):
        """Initialize account
        
        Args:
            save_data (str, optional): JSON string with account data. Defaults to None.
            account_type (AccountType, optional): Type of account. Defaults to None.
        """
        # Initialize basic properties
        self._accountName = ""
        self._secretKey = ""
        self._contacts = {}
        self._encryption_key = ""
        
        # Set default account type if none is provided
        self._accountType = account_type if account_type is not None else Beginner()
        
        # If saveData is provided, deserialize and load data
        if save_data is not None:
            data = json.loads(save_data)
            self._accountName = data["accountName"]
            self._secretKey = data["secretKey"] 
            self._contacts = data["contacts"]
            # Convert encryption key from hex string back to bytes if it's a string
            if isinstance(data["encryptionKey"], str):
                self._encryption_key = bytes.fromhex(data["encryptionKey"])
            else:
                self._encryption_key = data["encryptionKey"]
            
            # If account type is in the saved data, instantiate the appropriate type
            if "accountType" in data:
                account_type_name = data["accountType"].lower()
                print(f"account type: {account_type_name}")
                if account_type_name == "advanced":
                    self._accountType = Advanced()
                elif account_type_name == "beginner":
                    self._accountType = Beginner()
                elif account_type_name == "tester":
                    self._accountType = Tester()
       
    def get_account_name(self):
        """Get account name"""
        return self._accountName
    
    def get_secret_key(self):
        """Get secret key"""
        return self._secretKey
    
    def get_contacts(self):
        """Get contacts"""
        if not hasattr(self, '_contacts'):
            self._contacts = {}
        return self._contacts
        
    def get_account_type(self):
        """Get the account type"""
        return self._accountType
    
    def get_encryption_key(self):
        """Get the encryption key"""
        return self._encryption_key
    
    def set_account_type(self, account_type):
        """Set the account type
        
        Args:
            account_type (AccountType): The new account type
        """
        if not isinstance(account_type, AccountType):
            raise TypeError("accountType must be an instance of AccountType")
        self._accountType = account_type
        
    def set_account_name(self, name):
        """Set account name"""
        self._accountName = name
        
    def set_secret_key(self, key):
        """Set secret key"""
        self._secretKey = key
    
    def set_encryption_key(self, key):
        """Set the encryption key"""
        self._encryption_key = key
        
    def add_contact(self, name, address):
        """Add a contact"""
        if not hasattr(self, '_contacts'):
            self._contacts = {}
        self._contacts[name] = address
        
    def to_json(self):
        """Convert account to JSON string for saving
        
        Returns:
            str: JSON string representation of account
        """
        encryption_key_str = self._encryption_key.hex() if isinstance(self._encryption_key, bytes) else self._encryption_key

        data = {
            "accountName": self._accountName,
            "secretKey": self._secretKey,
            "contacts": self._contacts,
            "accountType": self._accountType.get_type_name(),
            "encryptionKey": encryption_key_str
        }
        return json.dumps(data)

    def toJSON(self):
        return self.to_json()