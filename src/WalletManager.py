import json
import os
from typing import Dict, Optional
from Wallet import Wallet

class WalletManager:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.wallets: Dict[str, Wallet] = {}
        self.load_wallets()
    
    def load_wallets(self, filepath: str = 'wallets.json'):
        try:
            with open(filepath) as f:
                wallets = json.load(f)
                for name, data in wallets.items():
                    self.wallets[name] = Wallet(
                        name=name,
                        api_key=self.api_key,
                        coin_symbol=data.get('coin_symbol', 'btc-testnet'),
                        initial_balance=data.get('balance', 10000.00),  # Added default balance
                        address=data['address']
                    )
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Note: Couldn't load wallets - {str(e)}")
        except KeyError as e:
            print(f"Error: Missing required field in wallet data - {str(e)}")
            # Initialize with empty wallets if data is corrupt
            self.wallets = {}
            
    def create_wallet(self, 
                    name: str, 
                    coin_symbol: str = 'btc-testnet',
                    initial_balance: float = 10000.00):
        """Create new wallet with required API key"""
        if name in self.wallets:
            raise ValueError(f"Wallet {name} already exists")
            
        wallet = Wallet(
            name=name,
            api_key=self.api_key,
            coin_symbol=coin_symbol,
            initial_balance=initial_balance
        )
        self.wallets[name] = wallet
        self._save_wallets()
        return wallet
        
    def _save_wallets(self):
        data = {
            name: {
                'address': wallet.address,
                'coin_symbol': wallet.coin_symbol,
                'balance': wallet.balance  # Ensure balance is saved
            }
            for name, wallet in self.wallets.items()
        }
        with open('wallets.json', 'w') as f:
            json.dump(data, f, indent=4)

    def remove_wallet(self, name: str):
        """Remove wallet from manager and delete its data"""
        if name in self.wallets:
            del self.wallets[name]
            if os.path.exists('wallets.json'):
                try:
                    with open('wallets.json', 'r') as f:
                        wallets = json.load(f)
                    if name in wallets:
                        del wallets[name]
                        with open('wallets.json', 'w') as f:
                            json.dump(wallets, f, indent=4)
                except (json.JSONDecodeError, IOError):
                    pass
            return True
        return False
    
    def get_wallet(self, name: str):
        return self.wallets.get(name)