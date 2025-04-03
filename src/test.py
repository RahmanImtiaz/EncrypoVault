# import requests
#
# # url = 'https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=gbp&days=30'
#
# url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=gbp&days=30"
# response = requests.get(url)
#
# if response.status_code == 200:
#     data = response.json()
#     # Process the data as needed
#
#     print(data)
# else:
#     print(f'Error: {response.status_code}')
#
#
#
# # URL = "  https://api.coingecko.com/api/v3/coins/{id}/market_chart?vs_currency={vs_currency}&days={days} "
#
#
#
# # URL2 = " https://api.coingecko.com/api/v3/coins/{id}/ohlc?vs_currency={vs_currency}&days={days}"
#
import os.path

import bitcoinlib
from bitcoinlib.keys import HDKey
from pycoin.symbols.xtn import network

from bitcoinlib import wallets
from bip_utils import Bip39Mnemonic, Bip39MnemonicGenerator, Bip39WordsNum, Bip39SeedGenerator, Bip32Slip10Secp256k1

mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)

print(f"Mnemonic: {mnemonic}")

seed = Bip39SeedGenerator(mnemonic).Generate()

ctx = Bip32Slip10Secp256k1.FromSeed(seed)

pycoin_key = network.keys.private(secret_exponent=ctx.PrivateKey().Raw().ToInt())

#btlib_wallet = bitcoinlib.wallets.Wallet.create("abcdtest")
if os.path.exists("./tmp"):
    os.unlink("./tmp")

hdkey_mainnet = HDKey(import_key=ctx.PrivateKey().ToExtended())
hdkey_mainnet.network_change("testnet")

# wallet = bitcoinlib.wallets.Wallet.create( "TestNetWallet", keys=[testnet_xprv], network='testnet', witness_type='segwit', db_uri='sqlite:///./tmp')
wallet = bitcoinlib
print(f"btlib address : {hdkey_mainnet.address()}")
print(f"pycoin address: {pycoin_key.address()}")

