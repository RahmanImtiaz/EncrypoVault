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
    def get_instance():
        """Get the singleton instance of AccountsFileManager"""
        if AccountsFileManager._AccountsFileManager is None:
            AccountsFileManager()
        return AccountsFileManager._AccountsFileManager
    
    def load_account(self, decryption_key, account_name):
        """Load account from file"""
        if not self._verify_file_integrity(self.current_directory):
            return None
        fileData = self._decrypt_file(self.current_directory, decryption_key, account_name)
        account = Account(fileData)
        return account

    def save_account(self, account):
        """Save account object to file"""
        if not self._verify_file_integrity(self.current_directory):
            return False
        # TODO: discuss this
        encryptionKey = AuthenticationManager.getInstance()._generateKey()
        self._encrypt_file(self.current_directory, encryptionKey, account)
        return True
        

    @staticmethod
    def _decrypt_file(file_path, decryption_key, account_name):
        """Decrypt file"""
        file_path = os.path.join(file_path, f"{account_name}.enc")
    
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
        key = kdf.derive(decryption_key)
    
        # Decrypt with AES-GCM
        aesgcm = AESGCM(key)
        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            return plaintext.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")

    # Update the _encryptFile method in AccountsFileManager.py to use toJSON
    @staticmethod
    def _encrypt_file(file_destination_path, encryption_key, account):
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
        key = kdf.derive(encryption_key)

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
        file_path = os.path.join(file_destination_path, f"{account.getAccountName()}.enc")
        with open(file_path, "w") as f:
            json.dump(encrypted_data, f)

        

    @staticmethod
    def _verify_file_integrity(file_path):
        """Verify file integrity"""
        # Check if directory exists
        if not os.path.exists(file_path):
            try:
                os.makedirs(file_path)
            except OSError:
                return False
    
        # Directory exists, so it's valid for our purposes
        return os.path.isdir(file_path) and os.access(file_path, os.R_OK | os.W_OK)

    def export_account(self, account, file_path):
        """Export the account to a file"""
        pass

    def import_account(self, file_path):
        """Import account from a file"""
        pass

    def import_account_from_phrase(self, recovery_phrase):
        """Import account using recovery phrase (list of strings)"""
        pass