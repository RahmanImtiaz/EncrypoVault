import csv
import os
from abc import ABC, abstractmethod
from Wallet import Wallet
from Crypto import Crypto
from ExchangeSocket import ExchangeSocket
import datetime


# THE API I RECOMMED IS THE CRYPTO API, IT PROVIDES ACCESS TO THE BLOCKCHAIN BUT ALSO LETS US HANDLE THE PRIVATE KEYS, COINBASE API
# DOES NOT LET US DO THIS!!! 
# ALSO HAS A SANDBOX FEATURE TO ALLOW US TO TEST WHETHER OUR CODE WORKS OR NOT


class CryptoTransactionStrategy(ABC):
    
    @abstractmethod
    def buy_crypto(self, crypto_name: str, amount: float):
        pass

    # EACH TIME WE BUY WE MUST ENCRYPT AND DECRYPT THE FILE THAT STORES OUR PRIVATE KEYS
    
    @abstractmethod
    def sell_crypto(self, crypto_name: str, amount: float):
        pass

    # EACH TIME WE SELL WE MUST ENCRYPT AND DECRYPT THE FILE THAT STORES OUR PRIVATE KEYS
    
    @abstractmethod
    def send_crypto(self, send_to: str, amount: float):
        pass
    
    
class RealTransaction(CryptoTransactionStrategy):
    def __init__(self, exchange: ExchangeSocket, wallet: Wallet = None):
        self.exchange = exchange
        self.wallet = wallet
        self.transaction_history = []

    async def buy_crypto(self, crypto_name: str, amount: float):
        """
        Simulates buying cryptocurrency using real funds
        - Checks if crypto is available on exchange
        - Gets current price
        - Deducts funds from wallet
        - Adds crypto to holdings
        """
        # Get current price data
        await self.exchange.connect_to_exchange()
        
        # Find the crypto in watched list
        crypto = next((c for c in self.exchange.watchedCrypto 
                      if isinstance(c, Crypto) and c.crypto_id == crypto_name), None)
        
        if not crypto:
            print(f"Error: {crypto_name} not found in tracked cryptocurrencies")
            return False
        
        if not crypto.current_price:
            print(f"Error: Current price not available for {crypto_name}")
            return False
        
        total_cost = amount * crypto.current_price
        
        if self.wallet.balance >= total_cost:
            self.wallet.balance -= total_cost
            
            # Add to holdings with proper structure
            if crypto_name in self.wallet.holdings:
                self.wallet.holdings[crypto_name]["amount"] += amount
            else:
                self.wallet.holdings[crypto_name] = {
                    "crypto": crypto,
                    "amount": amount
                }
            
            # Record transaction
            transaction = {
                'type': 'BUY',
                'crypto': crypto_name,
                'amount': amount,
                'price_per_unit': crypto.current_price,
                'total_cost': total_cost,
                'timestamp': datetime.datetime.now().isoformat()
            }
            self.transaction_history.append(transaction)
            
            print(f"Successfully bought {amount} {crypto_name} for £{total_cost:.2f}")
            return True
        else:
            print(f"Insufficient funds. Needed: £{total_cost:.2f}")
            return False

    async def sell_crypto(self, crypto_name: str, amount: float):
        """
        Simulates selling cryptocurrency for real funds
        - Checks if crypto is in holdings
        - Gets current price
        - Adds funds to wallet
        - Removes crypto from holdings
        """
        await self.exchange.connect_to_exchange()
    
        # Find the crypto in watched list
        crypto = next((c for c in self.exchange.watchedCrypto 
                    if isinstance(c, Crypto) and c.crypto_id == crypto_name), None)
    
        if not crypto:
            print(f"Error: {crypto_name} not found in tracked cryptocurrencies")
            return False
    
        if not crypto.current_price:
            print(f"Error: Current price not available for {crypto_name}")
            return False
    
        # Check holdings - now properly accessing the amount from the dictionary
        if not self.wallet or self.wallet.holdings.get(crypto_name, {}).get("amount", 0) < amount:
            print(f"Insufficient {crypto_name} holdings")
            return False
    
        # Calculate proceeds
        total_value = amount * crypto.current_price
    
        # Update wallet
        self.wallet.balance += total_value
        self.wallet.holdings[crypto_name]["amount"] -= amount
    
        # Clean up if amount reaches zero
        if self.wallet.holdings[crypto_name]["amount"] <= 0:
            del self.wallet.holdings[crypto_name]
    
        # Record transaction
        transaction = {
            'type': 'SELL',
            'crypto': crypto_name,
            'amount': amount,
            'price_per_unit': crypto.current_price,
            'total_value': total_value,
            'timestamp': datetime.datetime.now().isoformat()
        }      
        self.transaction_history.append(transaction)
    
        print(f"Successfully sold {amount} {crypto_name} for £{total_value:.2f}")
        return True

    async def send_crypto(self, send_to: str, amount: float, crypto_name: str):
        """
        Simulates sending cryptocurrency to another wallet
        - Checks if crypto is in holdings
        - Deducts from sender's wallet
        - Records transaction
        """
        # Check holdings - properly access the amount from the nested dictionary
        if not self.wallet or self.wallet.holdings.get(crypto_name, {}).get("amount", 0) < amount:
            print(f"Insufficient {crypto_name} holdings")
            return False
    
        # Deduct from sender
        self.wallet.holdings[crypto_name]["amount"] -= amount
    
        # Clean up if amount reaches zero
        if self.wallet.holdings[crypto_name]["amount"] <= 0:
            del self.wallet.holdings[crypto_name]
    
        # Record transaction
        transaction = {
            'type': 'SEND',
            'crypto': crypto_name,
            'amount': amount,
            'recipient': send_to,
            'timestamp': datetime.datetime.now().isoformat()
        }
        self.transaction_history.append(transaction)
    
        print(f"Sent {amount} {crypto_name} to {send_to}")
        return True

    def get_transaction_history(self):
        """Returns list of all transactions"""
        return self.transaction_history
    
    
    
class MockTransaction(CryptoTransactionStrategy):
    
    def buy_crypto(self, crypto_name: str, amount: float):
        pass
    
    def sell_crypto(self, crypto_name: str, amount: float):
        pass
    
    def send_crypto(self, send_to: str, amount: float):
        pass
    
    def receive_crypto(self, wallet_address: str):
        pass
    
    def generate_qr_code(self, wallet_address: str):
        pass
