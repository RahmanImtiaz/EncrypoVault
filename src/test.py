import asyncio
from Crypto import Crypto
from ExchangeSocket import ExchangeSocket

# Main function to test the connection and observer updates
async def main():
    # Create the ExchangeSocket instance and add product IDs (for testing)
    exchange_socket = ExchangeSocket(product_ids=['bitcoin', 'ethereum', 'dogecoin'])

    # Create some Crypto observers for different cryptocurrencies
    bitcoin_observer = Crypto('bitcoin')
    ethereum_observer = Crypto('ethereum')
    dogecoin_observer = Crypto('dogecoin')

    # Add the observers to the ExchangeSocket's watchlist
    exchange_socket.add_crypto(bitcoin_observer)
    exchange_socket.add_crypto(ethereum_observer)
    exchange_socket.add_crypto(dogecoin_observer)

    # Simulate connecting to the exchange and updating observers
    await exchange_socket.connect_to_exchange()
    
    for observer in exchange_socket.watchedCrypto:
        print(f"{observer.crypto_id} data:")
        print(observer.__dict__)
        # print()

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
