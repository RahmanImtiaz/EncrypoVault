import base64
import json

#import slip39

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
        self.transactionLog = None
        
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

            # Restore portfolio if it exists
            if "portfolio" in data and data["portfolio"]:
                from Portfolio import Portfolio
                portfolio_data = data["portfolio"]
                
                # Create portfolio with saved name
                self.portfolio = Portfolio(api_key="", name=portfolio_data.get('name', 'MainPortfolio'))
                
                # Restore wallets to portfolio
                if 'wallets' in portfolio_data:
                    from crypto_impl.WalletType import WalletType
                    
                    for name, wallet_data in portfolio_data['wallets'].items():
                        # Create wallet with saved properties
                        wallet = Wallet(
                            name=wallet_data.get('name', name),
                            wallet_type=WalletType.BITCOIN,  # Default to Bitcoin
                            address=wallet_data.get('address')
                        )
                        
                        # Restore wallet balance
                        wallet.balance = wallet_data.get('balance', 0.0)
                        
                        # Restore wallet holdings if they exist
                        if 'holdings' in wallet_data:
                            for crypto_id, holding_data in wallet_data['holdings'].items():
                                wallet.holdings[crypto_id] = {
                                    "amount": holding_data.get("amount", 0)
                                }
                        
                        # Add wallet to both the portfolio and the account's wallets dict
                        self.portfolio.wallets[name] = wallet
                        self._wallets[name] = wallet
            
            # Restore transaction log if it exists
            if "transactions" in data and data["transactions"]:
                from TransactionLog import TransactionLog
                from Transaction import Transaction
                import datetime
                
                self.transactionLog = TransactionLog()
                
                for tx_data in data["transactions"]:
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
                        tx_type=tx_data.get('type', 'unknown')
                    )
                    
                    # Add to transaction log
                    self.transactionLog.add_to_transaction_log(tx)

    def get_recovery_phrases(self):
        return self._mnemonic
        # Bip39SeedGenerator(a).Generate()

        # return slip39.create(self._accountName, master_secret=self._secretKey, using_bip39=True)
       
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
        return self.get_bip32_ctx().PrivateKey()

    def get_bip32_ctx(self) -> Bip32Slip10Secp256k1:
        return Bip32Slip10Secp256k1.FromSeed(base64.b64decode(self._bip_seed))
    
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

        # Convert portfolio to dictionary if it exists
        portfolio_data = None
        if self.portfolio:
            portfolio_data = {
                'name': self.portfolio.name,
                'wallets': {
                    name: {
                        'name': wallet.name,
                        'address': wallet.address,
                        'coin_symbol': wallet.coin_symbol,
                        'balance': wallet.balance,
                        'holdings': {
                            crypto_id: {"amount": data["amount"]} 
                            for crypto_id, data in wallet.holdings.items()
                        }
                    }
                    for name, wallet in self.portfolio.wallets.items()
                }
            }

        # Convert transaction log to dictionary if it exists
        transactions_data = None
        if self.transactionLog:
            transactions_data = [
                {
                    'timestamp': tx.timestamp.isoformat() if hasattr(tx.timestamp, 'isoformat') else str(tx.timestamp),
                    'amount': tx.amount,
                    'hash': tx.hash,
                    'receiver': tx.receiver,
                    'sender': tx.sender,
                    'type': tx.type
                }
                for tx in self.transactionLog._log
            ]

        data = {
            "accountName": self._accountName,
            "bipSeed": self._bip_seed,
            "mnemonic": self._mnemonic,
            "contacts": self._contacts,
            "accountType": self._accountType.get_type_name(),
            "encryptionKey": encryption_key_str,
            "portfolio": portfolio_data,
            "transactions": transactions_data
            
        }
        return json.dumps(data)

    def toJSON(self):
        return self.to_json()