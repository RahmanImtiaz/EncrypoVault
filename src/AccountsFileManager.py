from Account import Account
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from typing import List
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
        self.loaded_account = None
        self.default_directory = os.path.expanduser("~/.EncryptoVault")
        self.current_directory = self.default_directory
        if not os.path.exists(self.default_directory):
            os.makedirs(self.default_directory)
        self._initialized = True
    
    @staticmethod
    def get_instance() -> 'AccountsFileManager':
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
        self.loaded_account = account
        return account

    def get_loaded_account(self) -> Account:
        return self.loaded_account

    def create_account(self, account_name, account_type, account_password):
        if account_name in self.get_accounts():
            raise Exception('Account already exists')
        else:

            account = Account(save_data=json.dumps({"accountName": account_name, "encryptionKey": "00 00", "secretKey": "123", "contacts": [], "accountType": account_type}), account_type=account_type)
            self.save_account(account)

    def save_account(self, account):
        """Save account object to file"""
        if not self._verify_file_integrity(self.current_directory):
            return False
        # TODO: make this read from the account object
        encryptionKey = account.get_encryption_key()
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
            # Print more information for debugging
            print(f"Decryption failed with key length: {len(key)} bytes")
            print(f"Salt: {salt.hex()[:10]}..., Nonce: {nonce.hex()[:10]}...")
            raise ValueError(f"Decryption failed: {e}")

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
        plaintext = account.to_json().encode('utf-8')

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
        file_path = os.path.join(file_destination_path, f"{account.get_account_name()}.enc")
        with open(file_path, "w") as f:
            json.dump(encrypted_data, f)

    def get_accounts(self) -> List[str] :
        """ Select an account from available accounts """

        available_accounts = []

        try:
            for file in os.listdir(self.current_directory):
                if file.endswith(".enc"):
                    account_name = os.path.splitext(file)[0]
                    available_accounts.append(account_name)
        except Exception as e:
            print(f"Error listing accounts: {str(e)}")
            return ""

        if not available_accounts:
            print("No accounts available")
            return []

        # In a real implementation, this would show a UI for selection and For now is just returns the first account (if any)
        return available_accounts
        

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