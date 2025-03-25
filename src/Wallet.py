import blockcypher
import requests  # Add this import
from CryptoObserver import CryptoObserver
import json
import os
from typing import Optional

class Wallet(CryptoObserver):
    def __init__(self, 
                 name: str,
                 api_key: str,
                 coin_symbol: str = 'btc-testnet',
                 initial_balance: float = 10000.00,
                 address: Optional[str] = None):
        """
        Initialize wallet with proper address generation for different coin types
        
        Args:
            name: Wallet nickname
            api_key: BlockCypher API key
            coin_symbol: The cryptocurrency network (btc-testnet, beth/test, etc.)
            initial_balance: Starting balance
            address: Existing address to reuse
        """
        self.name = name
        self.api_key = api_key
        self.coin_symbol = coin_symbol
        self.balance = initial_balance
        self.holdings = {}
        self.address = address or self._generate_address()

    def _generate_address(self):
        """Generate new address using BlockCypher API for the specified coin type"""
        try:
            if self.coin_symbol.lower() == 'eth-testnet':
                # Ethereum testnet address generation using direct API call
                url = f"https://api.blockcypher.com/v1/beth/test/addrs?token={self.api_key}"
                response = requests.post(url)
                response.raise_for_status()  # Raises exception for 4XX/5XX errors
                address_data = response.json()
                print(f"Generated new {self.coin_symbol} address: {address_data['address']}")
                return address_data['address']
            else:
                # Default to Bitcoin address generation
                wallet_info = blockcypher.generate_new_address(
                    coin_symbol=self.coin_symbol,
                    api_key=self.api_key
                )
                print(f"Generated new {self.coin_symbol} address: {wallet_info['address']}")
                return wallet_info['address']
        except Exception as e:
            raise RuntimeError(f"Failed to generate {self.coin_symbol} address: {str(e)}")

    def toJSON(self):
        """Wallet serialization"""
        return json.dumps({
            "name": self.name,
            "address": self.address,
            "coin_symbol": self.coin_symbol,
            "balance": self.balance,
            "holdings": {
                crypto_id: {"amount": data["amount"]} 
                for crypto_id, data in self.holdings.items()
            }
        }, indent=4)

    def update(self, crypto_id: str, crypto_data: dict):
        if crypto_id in self.holdings:
            self.holdings[crypto_id]["crypto"].update(crypto_id, crypto_data)
            print(f"Updated {crypto_id} in wallet {self.name}")
        else:
            print(f"Crypto {crypto_id} not found in wallet {self.name}")

    def _calculate_total_balance(self):
        self.balance = sum(
            data["crypto"].current_price * data["amount"]
            for data in self.holdings.values()
            if data["crypto"].current_price is not None
        )

    def get_total_balance(self):
        self._calculate_total_balance()
        return self.balance