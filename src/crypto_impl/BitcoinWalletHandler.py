import json
from datetime import datetime

import bitcoinlib
from bitcoinlib.keys import HDKey
from bitcoinlib.wallets import wallet_create_or_open

import AccountsFileManager
from Transaction import Transaction
from crypto_impl.HandlerInterface import HandlerInterface
from crypto_impl.WalletType import WalletType


# from pycoin.symbols.xtn import network


class BitcoinWalletHandler(HandlerInterface):

    wallet: bitcoinlib.wallets.Wallet

    def __init__(self, name):
        self._name = name
        acc_manager = AccountsFileManager.AccountsFileManager.get_instance()
        db_uri = f"{acc_manager.current_directory}/{acc_manager.get_loaded_account().get_account_name()}.db"
        db_cache_uri = f"{acc_manager.current_directory}/{acc_manager.get_loaded_account().get_account_name()}.cache.db"
        db_uri = db_uri.replace("\\", "/")
        db_cache_uri = db_cache_uri.replace("\\", "/")
        db_uri = f"sqlite:///{db_uri}"
        db_cache_uri = f"sqlite:///{db_cache_uri}"

        hdkey = HDKey(import_key=self._get_child_key().PrivateKey().ToExtended())
        hdkey.network_change("testnet")
        subkey = hdkey.subkey_for_path("m/44'/0'", "testnet")
        print(f"testnet wif priv wif: {hdkey.wif_private(witness_type='segwit')}")
        self.wallet = wallet_create_or_open(
            name,
            db_uri=str(db_uri),
            db_cache_uri=str(db_cache_uri),
            witness_type="segwit",
            keys=subkey.wif_private(witness_type="segwit"),
            network="testnet"
        )


    @staticmethod
    def create_wallet(name):
       return BitcoinWalletHandler(name)

    def _get_child_key(self):
        ctx = AccountsFileManager.AccountsFileManager.get_instance().get_loaded_account().get_bip32_ctx()
        ind = self.account_name_to_index(self._name, self.get_wallet_type())
        return ctx.ChildKey(ind)

    def send_tx(self, amount, destination_address):
        if amount < 1:
            amount = amount * 100000000
        tx = self.wallet.send_to(destination_address, amount, broadcast=True)
        acc = AccountsFileManager.AccountsFileManager.get_instance().get_loaded_account()
        if tx is not None and tx.txid is not None:
            transaction_entry = Transaction(
                timestamp=datetime.now().isoformat(),
                amount=amount/100000000,
                tx_hash=tx.txid,
                sender=self.wallet.get_key().address,
                receiver=destination_address,
                name=self._name
            )
            acc.transactionLog.add_to_transaction_log(transaction_entry)
        return tx.txid

    def get_tx_info(self, tx_id):
        self.wallet.transactions()
        pass

    def get_tx(self):
        pass



    @staticmethod
    def load_wallet(data: dict):
        return BitcoinWalletHandler(data["name"])

    def get_address(self):
        return self.wallet.get_key().address

    def get_balance(self):
        self.wallet.scan()
        return self.wallet.balance(network="testnet")/100000000

    def toJSON(self):
        return json.dumps({
            "name": self._name,
            "type": str(self.get_wallet_type()),
            "balance": self.get_balance()
        })

    @staticmethod
    def get_wallet_type() -> WalletType:
        return WalletType.BITCOIN