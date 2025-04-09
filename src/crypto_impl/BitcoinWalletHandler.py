import json
from datetime import datetime, time
import sqlite3

import bitcoinlib
from bitcoinlib.keys import HDKey
from bitcoinlib.wallets import wallet_create_or_open
import sqlalchemy

import AccountsFileManager
import threading
from Transaction import Transaction
from crypto_impl.HandlerInterface import HandlerInterface
from crypto_impl.WalletType import WalletType


# from pycoin.symbols.xtn import network


class BitcoinWalletHandler(HandlerInterface):

    wallet: bitcoinlib.wallets.Wallet
    fake_balance: float

    def __init__(self, name, balance, fake_balance):
        self._name = name
        self._db_lock = threading.Lock() 
        self._balance = balance
        self.fake_balance = fake_balance
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
        #self.update_loop()
        threading.Thread(target=self.update_loop, daemon=True).start()


    @staticmethod
    def create_wallet(name):
       return BitcoinWalletHandler(name, balance=0, fake_balance=0)

    def update_balance(self):
        with self._db_lock:  # Ensure thread-safe access to the database
            try:
                self.wallet.scan()
                account = AccountsFileManager.AccountsFileManager.get_instance().get_loaded_account()
                self._balance = self.wallet.balance()/100000000
                print("Balance: ", self._balance)
                transactions = self.wallet.transactions()

                # valid_transactions = transactions
                if transactions is not None:
                    valid_transactions = []
                    for transaction in transactions:
                        is_valid = False
                        for inp in transaction.inputs:
                            if inp.address == self.get_address():
                                is_valid = True

                        for output in transaction.outputs:
                            if output.address == self.get_address():
                                is_valid = True
                        if is_valid:
                            valid_transactions.append(transaction)
                    print(f"Found {len(valid_transactions)} transactions")
                    for tx in valid_transactions:
                        if account.transactionLog.search(tx_hash=tx.txid) is None:
                            incoming = tx.inputs[0].address != self.get_address()
                            print("Incoming:", incoming)
                            print("Found a transaction that is not in the local log:")
                            amount = 0
                            sender = ""
                            receiver = ""
                            if incoming:
                                pass
                                amount = tx.inputs[0].value
                                sender = tx.inputs[0].address
                                receiver = self.get_address()
                            else:
                                for output in tx.outputs: # tb1qgdq7j0ntsdzm8t42xmqa0yygh9t7pw4ynuk3td
                                    if output.address != self.get_address():
                                        amount = output.value
                                        receiver = output.address


                            t = Transaction(
                                timestamp=tx.date.isoformat(),
                                amount=amount / 100000000,
                                tx_hash=tx.txid,
                                sender=sender,
                                receiver=receiver,
                                name=self._name
                            )
                            print(f"tx: {t.__str__()}")

                else:
                    print("No incoming transactions found.")
            except Exception as e:
                print(f"Error updating balance: {e}")
                raise

    def update_loop(self):
        self.update_balance()
        threading.Timer(30, self.update_loop).start()

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
        pass

    def get_tx(self):
        pass



    @staticmethod
    def load_wallet(data: dict):
        return BitcoinWalletHandler(data["name"], data.get("balance", 0), data.get("fake_balance", 0))

    def get_address(self):
        return self.wallet.get_key().address

    def get_balance(self):
        return self._balance
    
    def get_fake_balance(self) :
        return self.fake_balance/100000000

    def toJSON(self):
        return json.dumps({
            "name": self._name,
            "type": str(self.get_wallet_type()),
            "balance": self.get_balance(),
            "fake_balance": self.get_fake_balance(),
        })

    @staticmethod
    def get_wallet_type() -> WalletType:
        return WalletType.BITCOIN