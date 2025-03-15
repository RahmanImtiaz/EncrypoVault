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
    

    
class RealTransaction(CryptoTransactionStrategy):
    
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
