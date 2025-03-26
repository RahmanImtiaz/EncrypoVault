from Crypto import Crypto
from ExchangeSocket import ExchangeSocket
from Wallet import Wallet
from CryptoTransactionStrategy import RealTransaction
import asyncio

async def main():
    # Setup components - now matches Wallet's __init__ parameters
    wallet = Wallet("My Wallet", 1000.0)  # Explicit float
    bitcoin = Crypto("bitcoin")
    ethereum = Crypto("ethereum")
    
    exchange = ExchangeSocket(["bitcoin", "ethereum"])
    exchange.add_crypto(bitcoin)
    exchange.add_crypto(ethereum)
    exchange.add_crypto(wallet)
    
    # Create transaction processor
    transaction_processor = RealTransaction(exchange, wallet)
    
    # Execute transactions
    await transaction_processor.buy_crypto("bitcoin", 0.01)
    await transaction_processor.sell_crypto("bitcoin", 0.005)
    await transaction_processor.send_crypto("other_wallet", 0.005, "bitcoin")
    
    # Print results
    print(f"\nWallet Balance: £{wallet.balance:.2f}")
    print("Holdings:", {crypto.crypto_id: amount for crypto, amount in wallet.holdings.items()})
    print("Transaction History:", transaction_processor.get_transaction_history())

asyncio.run(main())