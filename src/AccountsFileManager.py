from Account import Account
from AuthenticationManager import AuthenticationManager
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os
import json


class AccountsFileManager:
    """Singleton class for file management of accounts"""
    _AccountsFileManager = None

    def __new__(cls):
        if cls._AccountsFileManager is None:
            cls._AccountsFileManager = super(AccountsFileManager, cls).__new__(cls)
            cls._AccountsFileManager.__initialized = False
        return cls._AccountsFileManager
    
    def __init__(self):
        if getattr(self, '_initialized', False):
            return
        
        self.default_directory = os.path.expanduser("~/.EncryptoVault")
        self.current_directory = self.default_directory
        if not os.path.exists(self.default_directory):
            os.makedirs(self.default_directory)
        self._initialized = True
    
    @staticmethod
    def getInstance():
        """Get the singleton instance of AccountsFileManager"""
        if AccountsFileManager._AccountsFileManager is None:
            AccountsFileManager()
        return AccountsFileManager._AccountsFileManager
    
    def loadAccount(self, decryption_key, account_name):
        """Load account from file"""
        if self._verifyFileIntegrity(self.current_directory) == False:
            return None
        fileData = self._decryptFile(self.current_directory, decryption_key, account_name)
        account = Account(fileData)
        return account

    def saveAccount(self, account):
        """Save account object to file"""
        if self._verifyFileIntegrity(self.current_directory) == False:
            return False
        
        encryptionKey = AuthenticationManager.getInstance()._generateKey()
        self._encryptFile(self.current_directory, encryptionKey, account)
        return True
        

    def _decryptFile(self, filePath, decryptionKey, account_name):
        """Decrypt file"""
        file_path = os.path.join(filePath, f"{account_name}.enc")
    
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Account file for {account_name} not found")
    
        with open(file_path, "r") as f:
            encrypted_data = json.load(f)
    
        # Extract components
        salt = bytes.fromhex(encrypted_data["salt"])
        nonce = bytes.fromhex(encrypted_data["nonce"])
        ciphertext = bytes.fromhex(encrypted_data["ciphertext"])

        # Derive the same key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(decryptionKey)
    
        # Decrypt with AES-GCM
        aesgcm = AESGCM(key)
        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            return plaintext.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")

    # Update the _encryptFile method in AccountsFileManager.py to use toJSON
    def _encryptFile(self, fileDestinationPath, encryptionKey, account):
        """Encrypt file and write to file"""
        
        # Generate a random salt for this encryption
        salt = os.urandom(16)

        # Derive key using PBKDF2 with SHA-256
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 32 bytes = 256 bits for AES-256
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(encryptionKey)

        # Generate a random nonce for AES-GCM
        nonce = os.urandom(12)

        # Get account data as JSON string and encode
        plaintext = account.toJSON().encode('utf-8')

        # Encrypt with AES-GCM
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)

        # Combine salt, nonce, and ciphertext for storage
        encrypted_data = {
            "salt": salt.hex(),
            "nonce": nonce.hex(),
            "ciphertext": ciphertext.hex()
        }

        # Write to file using account name as filename
        file_path = os.path.join(fileDestinationPath, f"{account.getAccountName()}.enc")
        with open(file_path, "w") as f:
            json.dump(encrypted_data, f)

        

    def _verifyFileIntegrity(self, filePath):
        """Verify file integrity"""
        # Check if directory exists
        if not os.path.exists(filePath):
            try:
                os.makedirs(filePath)
            except Exception:
                return False
    
        # Directory exists, so it's valid for our purposes
        return os.path.isdir(filePath) and os.access(filePath, os.R_OK | os.W_OK)

    def exportAccount(self, account, filePath):
        """Export the account to a file"""
        pass

    def importAccount(self, filePath):
        """Import account from a file"""
        pass

    def importAccountFromPhrase(self, recoveryPhrase):
        """Import account using recovery phrase (list of strings)"""
        pass