import json
import os
from typing import List

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator
import base64

from bip_utils.bip.bip32 import Bip32Base

from Account import Account


class AccountsFileManager:
    """Singleton class for file management of accounts"""
    _AccountsFileManager = None

    def __new__(cls):
        if cls._AccountsFileManager is None:
            cls._AccountsFileManager = super(AccountsFileManager, cls).__new__(cls)
            cls._AccountsFileManager._initialized = False
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
        account._encryption_key = decryption_key
        self.loaded_account = account
        return account

    def get_loaded_account(self) -> Account:
        return self.loaded_account

    def create_account(self, account_name, account_type, password, biometrics=None):
        if account_name in self.get_accounts():
            raise Exception('Account already exists')
        else:
            # Get the authentication manager
            from AuthenticationManager import AuthenticationManager
            auth_manager = AuthenticationManager.get_instance()

            # Use the provided password and biometrics to generate the encryption key
            if isinstance(password, str):
                password = password.encode('utf-8')

            # If biometrics not provided, prompt for them
            if biometrics is None:
                biometrics = auth_manager.prompt_for_biometrics()

            # Generate the encryption key
            encryption_key = auth_manager._generate_key(password, biometrics)

            mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)

            seed = Bip39SeedGenerator(mnemonic).Generate()

            print(f"acc creation time seed: {base64.b64encode(seed).decode('utf-8')}")



            # Create the account with proper initialization
            account = Account(save_data=json.dumps({
                "accountName": account_name,
                "encryptionKey": encryption_key.hex(),
                "bipSeed": base64.b64encode(seed).decode('utf-8'),
                "mnemonic": str(mnemonic),
                "contacts": {},
                "accountType": account_type
            }), account_type=account_type)

            # Save using the generated key
            self.save_account(account)
            return account

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

        with open(file_path, "rb") as f:
            encrypted_bytes = f.read()

        iv = encrypted_bytes[:AES.block_size]
        print(f"decrypt iv is: {iv} and length is {len(iv)}")
        print(f"decryption key is {decryption_key.hex()}")
        ciphertext = encrypted_bytes[AES.block_size:]

        cipher = AES.new(decryption_key, AES.MODE_CBC, iv)
        try:
            decrypted_bytes = cipher.decrypt(ciphertext)
            return unpad(decrypted_bytes, AES.block_size).decode("utf-8")
        except (UnicodeDecodeError, ValueError) as e:
            print(f"Decryption failed with key length: {len(decryption_key)} bytes")
            print(f"Ex: {e}")
            raise ValueError(f"Decryption failed: {e}")

    @staticmethod
    def _encrypt_file(file_destination_path, encryption_key, account):
        """Encrypt file and write to file"""
        if not isinstance(account, str):
            data = account.toJSON()
        else:
            data = account
        file_path = os.path.join(file_destination_path, f"{account.get_account_name()}.enc")
        print(f"Encrypting file: {file_path}")

        padded_data = pad(data.encode("utf-8"), AES.block_size)
        cipher = AES.new(encryption_key, AES.MODE_CBC)
        iv = cipher.iv
        print(f"encrypted iv is: {iv}")
        print(f"encryption key is {encryption_key.hex()}")
        ciphertext = cipher.encrypt(padded_data)
        encrypted_bytes = iv + ciphertext
        print(f"Writing file: {file_path}")
        with open(file_path, "wb") as f:
            f.write(encrypted_bytes)

    def get_accounts(self) -> List[str]:
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
