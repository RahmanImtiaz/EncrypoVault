import base64
import json

#import slip39

from TransactionLog import TransactionLog
from bip_utils.bip.bip32 import Bip32Slip10Secp256k1

from AccountType import AccountType, Beginner, Advanced, Tester
from Wallet import Wallet

class Account:
    def __init__(self, save_data=None, account_type=None):
        """Initialize account
        
        Args:
            save_data (str, optional): JSON string with account data. Defaults to None.
            account_type (AccountType, optional): Type of account. Defaults to None.
        """
        # Initialize basic properties
        self._accountName = ""
        self._bip_seed: bytes = b""
        self._mnemonic = ""
        self._contacts = {}
        self._wallets = {}
        self._encryption_key = ""
        self.portfolio = None
        self.transactionLog = TransactionLog()
        
        # Set default account type if none is provided
        self._accountType = account_type if account_type is not None else Beginner()
        
        # If saveData is provided, deserialize and load data
        if save_data is not None:
            data = json.loads(save_data)
            self._accountName = data["accountName"]
            self._bip_seed = data["bipSeed"]
            self._contacts = data.get("contacts", {})
            self._mnemonic = data["mnemonic"]

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

            
            # Initialize portfolio if needed 
            from Portfolio import Portfolio
            api_key = "fdade57267b549538799a94164f3db43"  
            self.portfolio = Portfolio(api_key, f"{self._accountName}'s Portfolio")
            
            # Restore transaction log if it exists
            if "transactions" in data and data["transactions"]:
                from Transaction import Transaction
                import datetime

                if isinstance(data["transactions"], str):
                    data["transactions"] = json.loads(data["transactions"])
                
                for tx_data in data["transactions"]:
                    if isinstance(tx_data, str):
                        tx_data = json.loads(tx_data)
                    required_fields = ["timestamp", "amount", "hash", "receiver", "sender", "name"]
                    for required_field in required_fields:
                        if required_field not in tx_data:
                            break
                    else:
                        # Parse timestamp (handle both string and datetime formats)
                        try:
                            if isinstance(tx_data['timestamp'], str):
                                timestamp = datetime.datetime.fromisoformat(tx_data['timestamp'])
                            else:
                                timestamp = tx_data['timestamp']
                        except (ValueError, TypeError):
                            timestamp = datetime.datetime.now()  # Fallback

                        # Create transaction object with saved data
                        tx = Transaction(
                            timestamp=timestamp,
                            amount=tx_data.get('amount', 0),
                            tx_hash=tx_data.get('hash', ''),
                            receiver=tx_data.get('receiver', ''),
                            sender=tx_data.get('sender', ''),
                            name=tx_data.get('name', 'unknown')
                        )

                        # Add to transaction log
                        self.transactionLog.add_to_transaction_log(tx)


    def recover_wallets_from_save_data(self, save_data):

        if isinstance(save_data, str):
            data = json.loads(save_data)
        else:
            data = save_data

        if "wallets" in data and data["wallets"]:
            from crypto_impl.WalletType import WalletType
            from crypto_impl.BitcoinWalletHandler import BitcoinWalletHandler  # Import wallet handler

            serialized_wallets = data["wallets"]
            for name, wallet_data in serialized_wallets.items():
                # Skip if already loaded from portfolio
                if name in self._wallets:
                    continue

                print("Wallet data:")
                print(wallet_data)

                # Create wallet with saved properties
                wallet_type_str = wallet_data.get('type', 'BTC')
                wallet_type = WalletType.from_str(wallet_type_str)

                wallet = Wallet(
                    name=wallet_data.get('name', name),
                    wallet_type=wallet_type,
                    address=wallet_data.get('address'),
                    last_balance=wallet_data.get('balance', 0),
                    fake_balance=wallet_data.get('fake_balance', 0)
                )

                # Restore wallet balance
                wallet.balance = wallet_data.get('balance', 0.0)

                # Restore wallet holdings if they exist
                if 'holdings' in wallet_data:
                    for crypto_id, holding_data in wallet_data['holdings'].items():
                        wallet.holdings[crypto_id] = {
                            "amount": holding_data.get("amount", 0)
                        }

                # Add wallet to account's wallets dict
                self._wallets[name] = wallet

                # Recreate wallet file (if needed)
                try:
                    BitcoinWalletHandler.create_wallet(name)  # Recreate wallet file
                except Exception as e:
                    print(f"Error recreating wallet file for {name}: {e}")

    def get_recovery_phrases(self):
        """Get recovery phrases for the account"""
        return self._mnemonic
        # Bip39SeedGenerator(a).Generate()

        # return slip39.create(self._accountName, master_secret=self._secretKey, using_bip39=True)


    def get_bip32_ctx(self):
        """Get BIP32 context for wallet derivation"""
        if isinstance(self._bip_seed, str):
            # If the seed is stored as a base64 string, decode it
            base = base64.b64decode(self._bip_seed)
        else:
            # If it's already bytes, use it directly
            base = self._bip_seed
        # Create and return the BIP32 context
        return Bip32Slip10Secp256k1.FromSeed(base)
       
    def get_account_name(self):
        """Get account name"""
        return self._accountName

    def get_wallets(self):
        """Get wallets"""
        return self._wallets

    def add_wallet(self, wallet: Wallet):
        self._wallets[wallet.name] = wallet
    
    def get_private_key(self):
        """Get secret key"""
        print(f"get priv key seed: {self._bip_seed}")
        base = base64.b64decode(self._bip_seed)
        ctx = Bip32Slip10Secp256k1.FromSeed(base)
        print("CTX:")
        print(ctx)
        return Bip32Slip10Secp256k1.FromSeed(base).PrivateKey().ToExtended()
    
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

    # we shouldnt allow any function to overwrite the key or else the user will loose their funds
    # def set_secret_key(self, key):
    #     """Set secret key"""
    #     self._bip_seed = key

    # same as above
    # def set_encryption_key(self, key):
    #     """Set the encryption key"""
    #     self._encryption_key = key
        
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

        # Convert transaction log to dictionary if it exists
        if self.transactionLog is not None:
            transactions_data = json.loads(self.transactionLog.toJSON())
        else:
            transactions_data = []

        # Convert wallets to dictionaries
        wallets_data = {}
        for name, wallet in self._wallets.items():
            wallets_data[name] = {
                'name': wallet.name,
                'type': str(wallet.wallet_type),
                'address': wallet.address,
                'balance': wallet.crypto_handler.get_balance(),
                'fake_balance': getattr(wallet.crypto_handler, 'fake_balance', 0.0),
                'holdings': {
                    crypto_id: {"amount": data.get("amount", 0)} 
                    for crypto_id, data in wallet.holdings.items()
                }
            }

        data = {
            "accountName": self._accountName,
            "bipSeed": self._bip_seed,
            "mnemonic": self._mnemonic,
            "contacts": self._contacts,
            "accountType": self._accountType.get_type_name(),
            "encryptionKey": encryption_key_str,
            "transactions": transactions_data,
            "wallets": wallets_data
            
        }
        return json.dumps(data)

    def toJSON(self):
        return self.to_json()