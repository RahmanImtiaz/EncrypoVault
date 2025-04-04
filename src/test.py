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

# mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
mnemonic = "guitar jelly evidence candy business sound scheme buddy congress exclude pioneer vast"


print(f"Mnemonic: {mnemonic}")

seed = Bip39SeedGenerator(mnemonic).Generate()

ctx = Bip32Slip10Secp256k1.FromSeed(seed)

pycoin_key = network.keys.private(secret_exponent=ctx.PrivateKey().Raw().ToInt())

#btlib_wallet = bitcoinlib.wallets.Wallet.create("abcdtest")
if os.path.exists("./tmp"):
    os.unlink("./tmp")

hdkey_mainnet = HDKey(import_key=ctx.PrivateKey().ToExtended())
print("hdkey priv wif: {}".format(hdkey_mainnet.wif_private()))
hdkey_mainnet.network_change("testnet")

# wallet = bitcoinlib.wallets.Wallet.create( "TestNetWallet", keys=[testnet_xprv], network='testnet', witness_type='segwit', db_uri='sqlite:///./tmp')

print(f"btlib address : {hdkey_mainnet.address()}")
print(f"pycoin address: {pycoin_key.address()}")

"""
    def send_tx(self, amount, destination_address):
        svc = self.get_service()
        tx = self.get_transaction_object()

        child_priv_hex = self._get_child_key().PrivateKey().Raw().ToHex()  # 32-byte hex string
        child_pub_hex = self._get_child_key().PublicKey().RawCompressed().ToHex()  # Compressed public key hex

        uxtos = svc.getutxos(self.get_address())
        #
        # for uxto in uxtos:
        #     print(uxto)

        uxto: dict = uxtos[0]
        print(uxto)
        tx.add_input(uxto["txid"], uxto["output_n"], keys=[child_pub_hex], strict=True)
        # Calculate fee and change
        input_amount = uxto["value"]
        fee = 1000  # Set reasonable fee in satoshis

        if input_amount <= amount + fee:
            print(f"Insufficient funds. UTXO: {input_amount} satoshis, Needed: {amount + fee} satoshis")
            return False

        # Add payment output
        tx.add_output(value=amount, address=destination_address, strict=True)

        # Add change output if needed
        change = input_amount - amount - fee
        if change > 546:  # Bitcoin dust threshold
            print(f"Adding change output: {change} satoshis back to {self.get_address()}")
            tx.add_output(value=change, address=self.get_address(), strict=True)

        # Sign the transaction
        print("Signing transaction...")
        tx.sign([child_priv_hex])
"""


from bitcoinlib.services.bitcoind import BitcoindClient

base_url = 'http://testuser:testpass@localhost:18443'
bdc = BitcoindClient(base_url=base_url)
balance = bdc.getbalance(addresslist=["bcrt1ql2xha266e5g7v07vrqw6xlvxmdladhhlca8sxn"])
print(balance)
