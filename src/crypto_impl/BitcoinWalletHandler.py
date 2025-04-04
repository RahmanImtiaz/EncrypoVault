import json

import bitcoinlib
import pycoin
from bitcoinlib.keys import HDKey
from bitcoinlib.networks import Network
from bitcoinlib.services.bitcoind import BitcoindClient
from pycoin.networks.bitcoinish import create_bitcoinish_network

#from pycoin.symbols.xtn import network

import AccountsFileManager
from crypto_impl.HandlerInterface import HandlerInterface
from crypto_impl.WalletType import WalletType


class BitcoinWalletHandler(HandlerInterface):

    _pycoin_key = None
    _name: str = ""

    def __init__(self, name):
        self._name = name

        self.localDev = False

        if self.localDev:
            REGTEST_PARAMS = dict(
                network_name="Bitcoin Regtest",
                # 'network' is an arbitrary label – later used when constructing transactions, etc.
                network="regtest",
                network_shortcut="RTEST",
                wif_prefix=239,
                symbol="QMU",
                subnet_name="regtest",
                address_prefix=111,
                pay_to_script_prefix=196,
                bip32_prv_prefix=0x04358394,
                bip32_pub_prefix=0x043587CF,
                # regtest genesis block hash from Bitcoin Core regtest
                genesis_hash="0f9188f13cb7b2c14f8d38f02b9c9ffc1da93d22",
                default_port=18443,
                dns_seeds=[],  # no seed nodes in regtest
                protocol_magic=0xdab5bffa
            )

            self.network = create_bitcoinish_network(**REGTEST_PARAMS)
        else:
            from pycoin.symbols.xtn import network
            self.network = network

        self._pycoin_key = self.network.keys.private(secret_exponent=self._get_secret_exponent())

    @staticmethod
    def create_wallet(name):
       return BitcoinWalletHandler(name)

    def get_service(self):
        if self.localDev:
            return BitcoindClient(base_url='http://testuser:testpass@localhost:18443')
            #return bitcoinlib.services.services.Service(network='regtest', rpc_url)
        else:
            return bitcoinlib.services.services.Service(network="testnet")

    def get_transaction_object(self):
        if self.localDev:
            return bitcoinlib.transactions.Transaction(network="regtest")
        else:
            return bitcoinlib.transactions.Transaction(network="testnet")

    def _get_secret_exponent(self):
        key = self._get_child_key()
        secret_exponent = int.from_bytes(key.PrivateKey().Raw().ToBytes(), byteorder="big")
        return secret_exponent

    def _get_child_key(self):
        ctx = AccountsFileManager.AccountsFileManager.get_instance().get_loaded_account().get_bip32_ctx()
        ind = self.account_name_to_index(self._name, self.get_wallet_type())
        return ctx.ChildKey(ind)

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

        # Verify and send
        print("Verifying transaction...")
        if tx.verify():
            print("Transaction verified successfully!")
            raw_tx = tx.as_hex()
            print(f"Sending raw transaction: {raw_tx}")

            txid = svc.sendrawtransaction(raw_tx)
            if txid:
                print(f"Transaction sent! TXID: {txid}")
                return txid
            else:
                print("Failed to send transaction")
                return False
        else:
            print("Transaction verification failed")
            return False

    def get_tx_info(self, tx_id):
        pass

    def get_tx(self):
        pass



    @staticmethod
    def load_wallet(data: dict):
        return BitcoinWalletHandler(data["name"])

    def get_address(self):
        return self._pycoin_key.address()

    def get_balance(self):
        svc = self.get_service()
        bal: int = svc.getbalance(addresslist=[self.get_address()])
        return bal

    def toJSON(self):
        return json.dumps({
            "name": self._name,
            "type": str(self.get_wallet_type()),
            "balance": self.get_balance()
        })

    @staticmethod
    def get_wallet_type() -> WalletType:
        return WalletType.BITCOIN