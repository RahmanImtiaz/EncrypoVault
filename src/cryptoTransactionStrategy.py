import csv
import os
from abc import ABC, abstractmethod


class CryptoTransactionStrategy(ABC):
    
    @abstractmethod
    def buy_crypto(self, crypto_name: str, amount: float):
        pass
    
    @abstractmethod
    def sell_crypto(self, crypto_name: str, amount: float):
        pass
    
    @abstractmethod
    def send_crypto(self, send_to: str, amount: float):
        pass
    
    @abstractmethod
    def receive_crypto(self, wallet_address: str):
        pass
    
    
    @abstractmethod
    def generate_qr_code(self, wallet_address: str):
        pass
    
    @abstractmethod
    def load_crypto_file(self, filename ="cryptoFile.txt") -> dict:
        pass
    
    @abstractmethod
    def save_crypto_file(self, holdings: dict, filename ="cryptoFile.txt"):
        pass
    
    @abstractmethod
    def update_crypto_file(self, crypto_name: str, amount: float, filename ="cryptoFile.txt"):
        pass
    
class RealTransaction(CryptoTransactionStrategy):
    
    def buy_crypto(self, crypto_name: str, amount: float):
        pass

    def __init__(self, exchange_socket):
        self.exchange_socket = exchange_socket
        
        
    def load_crypto_file(self, filename="cryptoFile.txt"):
               
        holdings = {}
        if os.path.exists(filename):
            with open(filename, "r", newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 2:
                        name, amt_str = row
                        holdings[name] = float(amt_str)
        return holdings
    
    
    
    def save_crypto_file(self, holdings, filename="cryptoFile.txt"):
        with open(filename, mode="w", newline="") as f:
            writer = csv.writer(f)
            for name, amt in holdings.items():
                writer.writerow([name, amt])
                
                
    def update_crypto_file(self, crypto_name, amount, filename="cryptoFile.txt"):
        holdings = self.load_crypto_file(filename)
        old = holdings.get(crypto_name, 0.0)
        new = old + amount
        
        if new <= 0:
            holdings.pop(crypto_name, None)
        else:
            holdings[crypto_name] = new
        self.save_crypto_file(holdings, filename)
        
        
        
    # async def buyCrypto(self, wallet, cryptoName: str, amount: float):
    #     try:
    #         price = await self.exchange_socket.get_crypto_price(cryptoName)
    #     except Exception as e:
    #         print(f"Error getting price for {cryptoName}: {e}")
    #         return None
        
    #     cost = price * amount
        
        
    #     print(f"Buying {amount} of {cryptoName} at {price}")
    #     user_input = input("Confirm transaction? (y/n): ")
        
    #     if user_input.lower() != "y":
    #         print("Transaction cancelled.")
    #         return
        
        
        
        # if wallet.watch:
        #     wallet.watch.addCrypto(cryptoName)
            
        
        
        # self.updateCryptoFile(cryptoName, amount)
        

    async def prepare_buy_transaction(self, wallet, cryptoName: str, amount: float):
        """Prepare the transaction details without executing it"""
        try:
            price = await self.exchange_socket.get_crypto_price(cryptoName)
            cost = price * amount
            
            # Return transaction details for confirmation
            return {
                "type": "buy",
                "crypto_name": cryptoName,
                "amount": amount,
                "price": price,
                "cost": cost,
                "wallet": wallet
            }
        except Exception as e:
            print(f"Error getting price for {cryptoName}: {e}")
            return None

    async def execute_buy_transaction(self, transaction_details):
        """Execute a pre-prepared buy transaction after confirmation"""
        if not transaction_details:
            return False
            
        cryptoName = transaction_details["crypto_name"]
        amount = transaction_details["amount"]
        wallet = transaction_details["wallet"]
        
        # Update watchlist if needed
        if wallet.watch:
            wallet.watch.add_crypto(cryptoName)
        
        # Execute the transaction
        self.update_crypto_file(cryptoName, amount)
        return True


    async def prepare_sell_transaction(self, wallet, cryptoName: str, amount: float):
        """Prepare the sell transaction details without executing it"""
        try:
            price = await self.exchange_socket.get_crypto_price(cryptoName)
            proceeds = price * amount
            
            # Return transaction details for confirmation
            return {
                "type": "sell",
                "crypto_name": cryptoName,
                "amount": amount,
                "price": price,
                "proceeds": proceeds,
                "wallet": wallet
            }
        except Exception as e:
            print(f"Error getting price for {cryptoName}: {e}")
            return None

    async def execute_sell_transaction(self, transaction_details):
        """Execute a pre-prepared sell transaction after confirmation"""
        if not transaction_details:
            return False
            
        cryptoName = transaction_details["crypto_name"]
        amount = transaction_details["amount"]
        wallet = transaction_details["wallet"]
        
        # Update wallet balance
        wallet.balance -= amount
        
        # Execute the transaction
        self.update_crypto_file(cryptoName, -amount)
        return True
    
        
    # async def sellCrypto(self, wallet, cryptoName: str, amount: float):
    #     price = await self.exchange_socket.get_crypto_price(cryptoName)
        
        
    #     print(f"Selling {amount} of {cryptoName} at {price}")
    #     user_input = input("Confirm transaction? (y/n): ")
        
    #     if user_input.lower() != "y":
    #         print("Transaction cancelled.")
    #         return
        
        
        
        
    #     wallet.balance -= amount
        
    #     self.updateCryptoFile(cryptoName, -amount)
    