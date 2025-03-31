from CryptoCurrency import CryptoCurrency
from ExchangeSocket import ExchangeSocket
from Portfolio import Portfolio
from CryptoTransactionStrategy import RealTransaction
import asyncio

async def main():
    # Initialize with API key
    API_KEY = "fdade57267b549538799a94164f3db43"
    portfolio = Portfolio(API_KEY)
    
    # Wallet selection/creation
    print("\n=== Available Wallets ===")
    existing_wallets = portfolio.wallets.keys()
    if existing_wallets:
        print("Existing wallets:")
        for i, name in enumerate(existing_wallets, 1):
            wallet = portfolio.get_wallet(name)
            print(f"{i}. {name} ({wallet.coin_symbol}) - £{wallet.balance:.2f}")
        print(f"{len(existing_wallets)+1}. Create new wallet")
        
        choice = input("\nSelect wallet (number): ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(existing_wallets):
                wallet_name = list(existing_wallets)[choice-1]
                wallet = portfolio.get_wallet(wallet_name)
                print(f"\nUsing existing wallet: {wallet_name}")
            elif choice == len(existing_wallets)+1:
                wallet_name = input("Enter new wallet name: ")
                coin_symbol = input("Enter coin symbol (btc-testnet/eth-testnet): ") or 'btc-testnet'
                initial_balance = float(input("Enter initial balance: ") or 10000.00)
                wallet = portfolio.create_wallet(wallet_name, coin_symbol, initial_balance)
                print(f"\nCreated new wallet: {wallet_name}")
            else:
                raise ValueError("Invalid selection")
        except (ValueError, IndexError):
            print("Invalid input, using default wallet")
            wallet = portfolio.get_wallet("TestWallet") or portfolio.create_wallet("TestWallet", "btc-testnet")
    else:
        print("No existing wallets found, creating default TestWallet")
        wallet = portfolio.create_wallet("TestWallet", "btc-testnet")
    
    print(f"\n=== Wallet Selected ===")
    print(f"Name: {wallet.name}")
    print(f"Address: {wallet.address}")
    print(f"Type: {wallet.coin_symbol}")
    print(f"Balance: £{wallet.balance:.2f}")
    
    # Initialize exchange
    exchange = ExchangeSocket(["bitcoin", "ethereum"])
    await exchange.connect_to_exchange()
    
    # Create Crypto objects
    bitcoin = CryptoCurrency("bitcoin")
    ethereum = CryptoCurrency("ethereum")
    
    # Add to exchange
    exchange.add_crypto(bitcoin)
    exchange.add_crypto(ethereum)
    exchange.add_crypto(wallet)
    
    # Start price updates
    update_task = asyncio.create_task(exchange.keep_updating_prices())
    await asyncio.sleep(2)  # Wait for initial prices
    
    # Initialize trader
    trader = RealTransaction(exchange, portfolio)
    
    print("\n=== Current Prices ===")
    print(f"Bitcoin: £{bitcoin.current_price or 'Unavailable'}")
    print(f"Ethereum: £{ethereum.current_price or 'Unavailable'}")
    
    # Transaction menu
    while True:
        print("\n=== Transaction Menu ===")
        print("1. Buy Crypto")
        print("2. Sell Crypto")
        print("3. Send Crypto")
        print("4. View Wallet")
        print("5. Exit")
        
        choice = input("Select action: ")
        
        if choice == "1":  # Buy
            crypto = input("Enter crypto to buy (bitcoin/ethereum): ").lower()
            amount = float(input(f"Enter amount of {crypto} to buy: "))
            await trader.buy(wallet.name, crypto, amount)
            
        elif choice == "2":  # Sell
            if not wallet.holdings:
                print("No holdings to sell")
                continue
            print("Your holdings:")
            for i, (crypto, data) in enumerate(wallet.holdings.items(), 1):
                print(f"{i}. {crypto}: {data['amount']}")
            crypto = input("Enter crypto to sell: ").lower()
            amount = float(input(f"Enter amount of {crypto} to sell: "))
            await trader.sell(wallet.name, crypto, amount)
            
        elif choice == "3":  # Send
            if not wallet.holdings:
                print("No holdings to send")
                continue
            print("Your holdings:")
            for i, (crypto, data) in enumerate(wallet.holdings.items(), 1):
                print(f"{i}. {crypto}: {data['amount']}")
            crypto = input("Enter crypto to send: ").lower()
            amount = float(input(f"Enter amount of {crypto} to send: "))
            recipient = input("Enter recipient address: ")
            await trader.send(wallet.name, recipient, crypto, amount)
             
        elif choice == "4":  # View Wallet
            print(f"\n=== Wallet Status ===")
            print(f"Balance: £{wallet.balance:.2f}")
            print("Holdings:")
            for crypto, data in wallet.holdings.items():
                print(f"- {crypto}: {data['amount']}")
            print("Recent Transactions:")
            for tx in trader.get_transaction_history(wallet.name)[-3:]:
                print(f"- {tx['tx_type']} {tx['amount']} {tx['crypto_name']} at £{tx.get('price', 'N/A')}")
                
        elif choice == "5":  # Exit
            break
            
        else:
            print("Invalid choice")
    
    # Clean up
    update_task.cancel()
    await exchange.disconnect_from_exchange()
    print("\n=== Session Ended ===")

if __name__ == "__main__":
    asyncio.run(main())