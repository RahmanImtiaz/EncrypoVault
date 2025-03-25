import json
import os
from typing import Dict, Optional, List
from Wallet import Wallet

class Portfolio:
    def __init__(self, api_key: str, name: str = "MainPortfolio"):
        self.api_key = api_key
        self.name = name
        self.wallets: Dict[str, Wallet] = {}  # Dictionary of wallet_name: Wallet
        self.load_wallets()
    
    def load_wallets(self, filepath: str = 'wallets.json'):
        """Load wallets from JSON file"""
        try:
            with open(filepath) as f:
                wallets = json.load(f)
                for name, data in wallets.items():
                    self.wallets[name] = Wallet(
                        name=name,
                        api_key=self.api_key,
                        coin_symbol=data.get('coin_symbol', 'btc-testnet'),
                        initial_balance=data.get('balance', 10000.00),
                        address=data['address']
                    )
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Note: Couldn't load wallets - {str(e)}")
        except KeyError as e:
            print(f"Error: Missing required field in wallet data - {str(e)}")
            self.wallets = {}
    
    def create_wallet(self, 
                     name: str, 
                     coin_symbol: str = 'btc-testnet',
                     initial_balance: float = 10000.00,
                     overwrite: bool = False) -> Wallet:
        """Create new wallet in the portfolio"""
        if name in self.wallets and not overwrite:
            raise ValueError(f"Wallet {name} already exists (use overwrite=True to replace)")
            
        wallet = Wallet(
            name=name,
            api_key=self.api_key,
            coin_symbol=coin_symbol,
            initial_balance=initial_balance
        )
        self.wallets[name] = wallet
        self._save_wallets()
        return wallet
    
    def remove_wallet(self, name: str) -> bool:
        """Remove wallet from portfolio"""
        if name in self.wallets:
            del self.wallets[name]
            self._save_wallets()
            return True
        return False
    
    def get_wallet(self, name: str) -> Optional[Wallet]:
        """Get wallet by name"""
        return self.wallets.get(name)
    
    def get_all_wallets(self) -> List[Wallet]:
        """Get list of all wallets in portfolio"""
        return list(self.wallets.values())
    
    def get_total_balance(self) -> float:
        """Calculate total balance across all wallets"""
        return sum(wallet.balance for wallet in self.wallets.values())
    
    def update_all_balances(self):
        """Update balances for all wallets in portfolio"""
        for wallet in self.wallets.values():
            wallet._calculate_total_balance()
    
    def _save_wallets(self):
        """Save wallets to JSON file"""
        data = {
            name: {
                'address': wallet.address,
                'coin_symbol': wallet.coin_symbol,
                'balance': wallet.balance,
                'holdings': {
                    crypto_id: {"amount": data["amount"]} 
                    for crypto_id, data in wallet.holdings.items()
                }
            }
            for name, wallet in self.wallets.items()
        }
        with open('wallets.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    def add_wallet(self, wallet: Wallet):
        """Add an existing wallet to the portfolio"""
        if wallet.name in self.wallets:
            raise ValueError(f"Wallet {wallet.name} already exists in portfolio")
        self.wallets[wallet.name] = wallet
        self._save_wallets()
    
    def to_dict(self) -> dict:
        """Convert portfolio to dictionary"""
        return {
            'name': self.name,
            'wallets': [wallet.toJSON() for wallet in self.wallets.values()],
            'total_balance': self.get_total_balance()
        }
    
    def __str__(self):
        return (f"Portfolio '{self.name}': {len(self.wallets)} wallets, "
                f"Total Balance: £{self.get_total_balance():.2f}")

        
    
    