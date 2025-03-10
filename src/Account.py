import json

class Account:
    def __init__(self, saveData=None):
        """Initialize account
        
        Args:
            saveData (str, optional): JSON string with account data. Defaults to None.
        """
        if saveData is None:
            self._accountName = ""
            self._secretKey = ""
            self._contacts = {}
        else:
            data = json.loads(saveData)  # Parse the JSON string into a dictionary
            self._accountName = data["accountName"]
            self._secretKey = data["secretKey"] 
            self._contacts = data["contacts"]

    #def __init__(self, accountType):
       # self._accountType = accountType
       
    def getAccountName(self):
        """Get account name"""
        return self._accountName
    
    def getSecretKey(self):
        """Get secret key"""
        return self._secretKey
    
    def getContacts(self):
        """Get contacts"""
        return self._contacts
        
    def setAccountName(self, name):
        """Set account name"""
        self._accountName = name
        
    def setSecretKey(self, key):
        """Set secret key"""
        self._secretKey = key
        
    def addContact(self, name, address):
        """Add a contact"""
        self._contacts[name] = address