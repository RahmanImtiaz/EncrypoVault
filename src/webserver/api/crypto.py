import json
from json import JSONDecodeError
import sys
import asyncio
import uuid

from datetime import datetime
from Transaction import Transaction 
from flask import Blueprint, request
from flask_socketio import SocketIO
from AccountsFileManager import AccountsFileManager
from ConcreteCryptoObserver import ConcreteCryptoObserver
from ExchangeSocket import ExchangeSocket
from ExchangeSocketCR import PriceSocket
from Wallet import Wallet
from crypto_impl.BitcoinWalletHandler import BitcoinWalletHandler
from crypto_impl.WalletType import WalletType


class CryptoRoutes:
    def __init__(self, api_bp: Blueprint, app):
        crypto_bp = Blueprint('crypto', __name__, url_prefix='/crypto')

        socket = SocketIO(app, logger=False, engineio_logger=False)

        def handle_update(crypto_id: str, crypto_data: dict):
            self.send_socket_message("cryptoUpdate", {"cryptoId": crypto_id, "cryptoData": crypto_data})

        self.crypto_observer = ConcreteCryptoObserver(on_update=handle_update)



        socket.init_app(app)

        app.socketio = socket

        ws_prefix = api_bp.url_prefix+crypto_bp.url_prefix

        @crypto_bp.route("/wallets/details", methods=["GET"])
        def get_wallets():
            acc = AccountsFileManager.get_instance().get_loaded_account()
            wallets = []
            for wallet in acc.get_wallets():

                wallets.append(
                    json.loads(acc.get_wallets()[wallet].toJSON())
                )
            return {"data": wallets}, 200

        @crypto_bp.route("/wallets/send_crypto", methods=["POST"])
        def send_crypto_from_wallet():
            data = json.loads(request.data)
            required_values = ["walletName", "amount", "destinationAddress"]

            for required_value in required_values:
                if required_value not in data:
                    return {"error": f"{required_value} not found"}, 400

            wallet_name = data["walletName"]
            amount = data["amount"]
            destination = data["destinationAddress"]
            account = AccountsFileManager.get_instance().get_loaded_account()
            wallet = account.get_wallets()[wallet_name]

            if wallet is None:
                return {"error": f"{wallet_name} not found"}, 404

            txid = wallet.crypto_handler.send_tx(amount, destination)
            print(f"Acc has transactions:")
            print(json.dumps(account.transactionLog.toJSON(), indent=4))
            AccountsFileManager.get_instance().save_account(account)
            return {"success": True, "txid": txid}, 200


        @crypto_bp.route("/wallets", methods=["POST"])
        def create_wallet():

            # Get current account
            account_manager = AccountsFileManager.get_instance()
            current_account = account_manager.get_loaded_account()

            if not current_account:
                return {"error": "No account is currently logged in"}, 401
            
            # Get request data
            data = request.get_json()
            if not data:
                return {"error": "No data provided"}, 400
            
            required_values = ["walletType", "walletName"]

            for required_value in required_values:
                if required_value not in data:
                    return {"error": f"{required_value} not found"}, 400

            wallet_type = data["walletType"]
            wallet_type = WalletType.from_str(wallet_type)
            wallet_name = data["walletName"]
            
            wallet = Wallet(wallet_name, wallet_type)
            try:
                AccountsFileManager.get_instance().get_loaded_account().add_wallet(wallet)
                print(f"at time of wallet saving, decryption key is {AccountsFileManager.get_instance().get_loaded_account().get_encryption_key().hex()}")
                AccountsFileManager.get_instance().save_account(AccountsFileManager.get_instance().get_loaded_account())
            except Exception as e:
                return {"error": str(e)}, 500
            
            return {"walletType": str(wallet_type), "walletName": wallet_name, "walletAddress": wallet.address}, 200



        @socket.on('connect', ws_prefix+'/ws')
        def handle_connect(auth):
            print('got client connection w/ auth: {}'.format(auth))

        @socket.on('disconnect', ws_prefix+'/ws')
        def handle_disconnect(reason):
            print('got client disconnect w/ reason: {}'.format(reason))

        @crypto_bp.route("/buy", methods=["POST"])
        def buy_crypto():
            data = request.get_json()
            required_values = ["walletName", "amount"]
            for required_value in required_values:
                if required_value not in data:
                    return {"error": f"{required_value} not found"}, 400
            wallet_name = data["walletName"]
            amount = data["amount"]
            account = AccountsFileManager.get_instance().get_loaded_account()
            wallet = account.get_wallets()[wallet_name]
            if wallet is None:
                return {"error": f"{wallet_name} not found"}, 404
            
            transaction = Transaction(
                timestamp=datetime.now().isoformat(),
                amount=amount/100000000,  # Convert back to BTC
                tx_hash=f"fake-buy-{uuid.uuid4()}",  # Generate fake TXID
                sender="exchange",
                receiver=wallet.address,
                name=wallet.name
            )
            account.transactionLog.add_to_transaction_log(transaction)

            wallet.crypto_handler.fake_balance+=amount
            AccountsFileManager.get_instance().save_account(account)
            return {"success": True}, 200

        @crypto_bp.route("/sell", methods=["POST"])
        def sell_crypto():
            data = request.get_json()
            required_values = ["walletName", "amount"]
            for required_value in required_values:
                if required_value not in data:
                    return {"error": f"{required_value} not found"}, 400
            wallet_name = data["walletName"]
            amount = data["amount"]
            account = AccountsFileManager.get_instance().get_loaded_account()
            wallet = account.get_wallets()[wallet_name]
            if wallet is None:
                return {"error": f"{wallet_name} not found"}, 404
            if wallet.crypto_handler.fake_balance < amount:
                return {"error": f"{wallet.crypto_handler.get_fake_balance()} < {amount/100000000}"}, 400
            
            transaction = Transaction(
                timestamp=datetime.now().isoformat(),
                amount=amount/100000000,
                tx_hash=f"fake-sell-{uuid.uuid4()}",
                sender=wallet.address,
                receiver="exchange",
                name=wallet.name
            )
            account.transactionLog.add_to_transaction_log(transaction)

            wallet.crypto_handler.fake_balance -= amount
            AccountsFileManager.get_instance().save_account(account)
            return {"success": True}, 200

        @crypto_bp.route("/verify_biometrics", methods=["POST"])
        def verify_biometrics():
            try:
                data = json.loads(request.data)
                account_name = data.get("accountName")
                password = data.get("password")  # Optional fallback
                platform = sys.platform

                if platform == "darwin":
                    # macOS: Use Touch ID
                    from macos_touch_id import authenticate_with_touch_id
                    if not authenticate_with_touch_id():
                        return {"error": "Biometric authentication failed"}, 403
                elif platform == "win32":
                    return {"success": True}, 200
                else:
                    return {"error": "Biometric authentication not supported on this platform"}, 400

                return {"success": True}, 200
            except Exception as e:
                print(f"Error verifying biometrics: {e}")
                return {"error": str(e)}, 500

        @socket.on('message', ws_prefix+'/ws')
        def handle_message(message=None):
            if message is None:
                self.send_socket_message("server_error", {"error": "got nothing in socket, bruh??"})
                return
            if type(message) is not dict:
                try:
                    data = json.loads(message)
                except JSONDecodeError:
                    self.send_socket_message("server_error", {"error": "Malformed message"})
                    return
            else:
                print("message is dict, no need to parse")
                data = message
            if 'command' not in data:
                self.send_socket_message("server_error", {"error": "invalid socket message! missing command"})
                return

            cmd = data['command']

            match cmd:
                case 'add_crypto':
                    if 'crypto_id' not in data:
                        self.send_socket_message("server_error", {"error": "missing crypto_id"})
                    else:
                        crypto_id = data['crypto_id']
                        ExchangeSocket().add_crypto(crypto_id)
                        self.send_socket_message("message", {"message": "added crypto: {}".format(crypto_id)})
                case 'proxy_data':
                    type_sent = data.get("type")
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    # Checks what the client wants and returns the data avoiding the CORS issue
                    try:
                        if type_sent == "coins_list": 
                            result = loop.run_until_complete(ExchangeSocket().coins_list())
                            response_event = "coins_list_response"
                            
                        elif type_sent == "coin_data":
                            coin_id = data.get("coin_id")
                            if not coin_id:
                                result = {"error": "Missing coin_id for coin_data"}
                            else:
                                result = loop.run_until_complete(ExchangeSocket().coin_data(coin_id))
                            response_event = "coin_data_response"
                            
                        elif type_sent == "candlestick":
                            coin_id = data.get("coin_id")
                            time_range = data.get("days", 1)
                            if not coin_id:
                                result = {"error": "Missing coin_id for candlestick"}
                            else:
                                result = loop.run_until_complete(ExchangeSocket().candlestick_data(coin_id, time_range))
                            response_event = "candlestick_response"
                            
                        elif type_sent == "linegraph":
                            coin_id = data.get("coin_id")
                            time_range = data.get("days", 1)
                            if not coin_id:
                                result = {"error": "Missing coin_id for price_graph"}
                            else:
                                result = loop.run_until_complete(ExchangeSocket().linegraph_data(coin_id, time_range))
                            response_event = "linegraph_response"
                            
                        else:
                            result = {"error": "Unknown request type"}
                            response_event = "proxy_response"
                            
                    except Exception as e:
                        result = {"error": str(e)}
                        response_event = "proxy_response"
                        
                    finally:
                        loop.close()
                    self.send_socket_message(response_event, result)
                    
                case 'get_price':
                    price_socket = PriceSocket()
                    # if the price socket is not connected then pull from the price.json else if it is connected then pull from 
                    # pricesocket.price_cache
                    
                    if not price_socket.is_connected():
                        # load the price cache from the file
                        with open(price_socket.price_file, 'r') as f:
                            price_socket.price_cache = json.load(f)
                    
                    
                    # send the whole price cache front end can deal with it
                    
                    self.send_socket_message("price_cache", price_socket.price_cache)
                    

        self.socket = socket
        self.ws_prefix = ws_prefix
        api_bp.register_blueprint(crypto_bp)
        
        
        
        
        


    def send_socket_message(self, channel: str, message: dict):
        self.socket.emit(channel, message, namespace=self.ws_prefix+"/ws")







