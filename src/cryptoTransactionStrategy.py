from abc import ABC, abstractmethod
import os
import csv
from transaction import Transaction

class CryptoTransactionStrategy(ABC):
    
    @abstractmethod
    def buyCrypto(self, cryptoName: str, amount: float):
        pass
    
    @abstractmethod
    def sellCrypto(self, cryptoName: str, amount: float):
        pass
    
    @abstractmethod
    def sendCrypto(self, sendTo: str, amount: float):
        pass
    
    @abstractmethod
    def recieveCrypto(self, walletAddress: str):
        pass
    
    
    @abstractmethod
    def generateQRCode(self, walletAddress: str):
        pass
    
    @abstractmethod
    def loadCryptoFile(filename = "cryptoFile.txt") -> dict:
        pass
    
    @abstractmethod
    def saveCryptoFile(self, holdings: dict, filename = "cryptoFile.txt"):
        pass
    
    @abstractmethod
    def updateCryptoFile(self, crypto_name: str, amount: float, filename = "cryptoFile.txt"):
        pass
    
class RealTransaction(CryptoTransactionStrategy):
    
    def __init__(self, exchange_socket):
        self.exchange_socket = exchange_socket
        
        
    def loadCryptoFile(filename="cryptoFile.txt"):
               
        holdings = {}
        if os.path.exists(filename):
            with open(filename, "r", newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 2:
                        name, amt_str = row
                        holdings[name] = float(amt_str)
        return holdings
    
    
    
    def saveCryptoFile(self, holdings, filename="cryptoFile.txt"):
        with open(filename, mode="w", newline="") as f:
            writer = csv.writer(f)
            for name, amt in holdings.items():
                writer.writerow([name, amt])
                
                
    def updateCryptoFile(self, crypto_name, amount, filename="cryptoFile.txt"):
        holdings = self.loadCryptoFile(filename)
        old = holdings.get(crypto_name, 0.0)
        new = old + amount
        
        if new <= 0:
            holdings.pop(crypto_name, None)
        else:
            holdings[crypto_name] = new
        self.saveCryptoFile(holdings, filename)
        
        
        
    async def buyCrypto(self, wallet, cryptoName: str, amount: float):
        price = await self.exchange_socket.get_crypto_price(cryptoName)
        
        wallet.balance += amount
        
        print(f"Buying {amount} of {cryptoName} at {price}")
        user_input = input("Confirm transaction? (y/n): ")
        
        if user_input.lower() != "y":
            print("Transaction cancelled.")
            return
        
        
        
        if wallet.watch:
            wallet.watch.addCrypto(cryptoName)
            
        
        
        self.updateCryptoFile(cryptoName, amount)
        
        
        
    async def sellCrypto(self, wallet, cryptoName: str, amount: float):
        price = await self.exchange_socket.get_crypto_price(cryptoName)
        
        
        print(f"Selling {amount} of {cryptoName} at {price}")
        user_input = input("Confirm transaction? (y/n): ")
        
        if user_input.lower() != "y":
            print("Transaction cancelled.")
            return
        
        
        
        
        wallet.balance -= amount
        
        self.updateCryptoFile(cryptoName, -amount)
    