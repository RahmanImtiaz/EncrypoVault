from abc import ABC, abstractmethod
import datetime
from typing import Optional
from Wallet import Wallet
from Crypto import Crypto

class CryptoTransactionStrategy(ABC):
    @abstractmethod
    async def buy(self, wallet_name: str, crypto_name: str, amount: float) -> bool:
        pass
    
    @abstractmethod
    async def sell(self, wallet_name: str, crypto_name: str, amount: float) -> bool:
        pass
    
    @abstractmethod
    async def send(self, wallet_name: str, recipient: str, crypto_name: str, amount: float) -> bool:
        pass

class RealTransaction(CryptoTransactionStrategy):
    def __init__(self, exchange, portfolio): 
        self.exchange = exchange
        self.portfolio = portfolio
        self.transaction_history = []

    async def buy(self, wallet_name: str, crypto_name: str, amount: float) -> bool:
        """Execute buy transaction for specified wallet"""
        wallet = self.portfolio.get_wallet(wallet_name)
        if not wallet:
            print(f"Wallet {wallet_name} not found")
            return False

        crypto = self._get_crypto(crypto_name)
        if not crypto:
            print(f"[{wallet.name}] {crypto_name} not available")
            return False

        if not crypto.current_price:
            print(f"[{wallet.name}] No current price for {crypto_name}")
            return False

        total_cost = amount * crypto.current_price

        if wallet.balance < total_cost:
            print(f"[{wallet.name}] Insufficient balance. Needed: £{total_cost:.2f}, Available: £{wallet.balance:.2f}")
            return False

        # Execute purchase
        wallet.balance -= total_cost
        self._add_to_holdings(wallet, crypto, crypto_name, amount)
        
        self._record_transaction(
            wallet_name=wallet.name,
            tx_type="BUY",
            crypto_name=crypto_name,
            amount=amount,
            price=crypto.current_price,
            total=total_cost
        )
        
        print(f"[{wallet.name}] Bought {amount} {crypto_name} for £{total_cost:.2f}")
        return True

    async def sell(self, wallet_name: str, crypto_name: str, amount: float) -> bool:
        """Execute sell transaction for specified wallet"""
        wallet = self.portfolio.get_wallet(wallet_name)
        if not wallet:
            print(f"Wallet {wallet_name} not found")
            return False

        crypto = self._get_crypto(crypto_name)
        if not crypto:
            print(f"[{wallet.name}] {crypto_name} not available")
            return False

        if not crypto.current_price:
            print(f"[{wallet.name}] No current price for {crypto_name}")
            return False

        current_holdings = wallet.holdings.get(crypto_name, {}).get("amount", 0)
        if current_holdings < amount:
            print(f"[{wallet.name}] Insufficient {crypto_name}. Needed: {amount}, Available: {current_holdings}")
            return False

        # Execute sale
        total_value = amount * crypto.current_price
        wallet.balance += total_value
        wallet.holdings[crypto_name]["amount"] -= amount

        # Clean up if empty
        if wallet.holdings[crypto_name]["amount"] <= 0:
            del wallet.holdings[crypto_name]

        self._record_transaction(
            wallet_name=wallet.name,
            tx_type="SELL",
            crypto_name=crypto_name,
            amount=amount,
            price=crypto.current_price,
            total=total_value
        )
        
        print(f"[{wallet.name}] Sold {amount} {crypto_name} for £{total_value:.2f}")
        return True

    async def send(self, wallet_name: str, recipient: str, crypto_name: str, amount: float) -> bool:
        """Execute send transaction from specified wallet"""
        wallet = self.portfolio.get_wallet(wallet_name)
        if not wallet:
            print(f"Wallet {wallet_name} not found")
            return False

        current_holdings = wallet.holdings.get(crypto_name, {}).get("amount", 0)
        if current_holdings < amount:
            print(f"[{wallet.name}] Insufficient {crypto_name}. Needed: {amount}, Available: {current_holdings}")
            return False

        # Execute transfer
        wallet.holdings[crypto_name]["amount"] -= amount
        if wallet.holdings[crypto_name]["amount"] <= 0:
            del wallet.holdings[crypto_name]

        self._record_transaction(
            wallet_name=wallet.name,
            tx_type="SEND",
            crypto_name=crypto_name,
            amount=amount,
            recipient=recipient
        )
        
        print(f"[{wallet.name}] Sent {amount} {crypto_name} to {recipient}")
        return True

    def _get_crypto(self, crypto_name: str) -> Optional[Crypto]:
        """Helper to get crypto from exchange"""
        for asset in self.exchange.watchedCrypto:
            if isinstance(asset, Crypto) and asset.crypto_id == crypto_name:
                return asset
        return None

    def _add_to_holdings(self, wallet: Wallet, crypto: Crypto, crypto_name: str, amount: float):
        """Add crypto to wallet's holdings"""
        if crypto_name in wallet.holdings:
            wallet.holdings[crypto_name]["amount"] += amount
        else:
            wallet.holdings[crypto_name] = {
                "crypto": crypto,
                "amount": amount
            }

    def _record_transaction(self, **kwargs):
        """Standard transaction recording"""
        tx = {
            "timestamp": datetime.datetime.now().isoformat(),
            **kwargs
        }
        self.transaction_history.append(tx)

    def get_transaction_history(self, wallet_name: str = None):
        """Get filtered transaction history"""
        if wallet_name:
            return [tx for tx in self.transaction_history if tx.get("wallet_name") == wallet_name]
        return self.transaction_history