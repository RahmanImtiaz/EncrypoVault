import json
from AccountType import AccountType, Beginner, Advanced, Tester

class Account:
    def __init__(self, saveData=None, accountType=None):
        """Initialize account
        
        Args:
            saveData (str, optional): JSON string with account data. Defaults to None.
            accountType (AccountType, optional): Type of account. Defaults to None.
        """
        # Initialize basic properties
        self._accountName = ""
        self._secretKey = ""
        self._contacts = {}
        
        # Set default account type if none is provided
        self._accountType = accountType if accountType is not None else Beginner()
        
        # If saveData is provided, deserialize and load data
        if saveData is not None:
            data = json.loads(saveData)
            self._accountName = data["accountName"]
            self._secretKey = data["secretKey"] 
            self._contacts = data["contacts"]
            
            # If account type is in the saved data, instantiate the appropriate type
            if "accountType" in data:
                account_type_name = data["accountType"]
                if account_type_name == "Advanced":
                    self._accountType = Advanced()
                elif account_type_name == "Beginner":
                    self._accountType = Beginner()
                elif account_type_name == "Tester":
                    self._accountType = Tester()
       
    def getAccountName(self):
        """Get account name"""
        return self._accountName
    
    def getSecretKey(self):
        """Get secret key"""
        return self._secretKey
    
    def getContacts(self):
        """Get contacts"""
        return self._contacts
        
    def getAccountType(self):
        """Get the account type"""
        return self._accountType
    
    def setAccountType(self, accountType):
        """Set the account type
        
        Args:
            accountType (AccountType): The new account type
        """
        if not isinstance(accountType, AccountType):
            raise TypeError("accountType must be an instance of AccountType")
        self._accountType = accountType
        
    def setAccountName(self, name):
        """Set account name"""
        self._accountName = name
        
    def setSecretKey(self, key):
        """Set secret key"""
        self._secretKey = key
        
    def addContact(self, name, address):
        """Add a contact"""
        self._contacts[name] = address
        
    def toJSON(self):
        """Convert account to JSON string for saving
        
        Returns:
            str: JSON string representation of account
        """
        data = {
            "accountName": self._accountName,
            "secretKey": self._secretKey,
            "contacts": self._contacts,
            "accountType": self._accountType.get_type_name()
        }
        return json.dumps(data)