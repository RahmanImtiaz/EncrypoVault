import requests

# url = 'https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=gbp&days=30'

url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=gbp&days=30"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    # Process the data as needed
    
    print(data)
else:
    print(f'Error: {response.status_code}')



# URL = "  https://api.coingecko.com/api/v3/coins/{id}/market_chart?vs_currency={vs_currency}&days={days} "



# URL2 = " https://api.coingecko.com/api/v3/coins/{id}/ohlc?vs_currency={vs_currency}&days={days}"

