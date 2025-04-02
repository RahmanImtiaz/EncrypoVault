import json
from json import JSONDecodeError

from flask import Blueprint, request
from flask_socketio import SocketIO
import asyncio
from AccountsFileManager import AccountsFileManager
from ConcreteCryptoObserver import ConcreteCryptoObserver
from ExchangeSocket import ExchangeSocket
from Wallet import Wallet
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

        @crypto_bp.route("/wallets", methods=["POST"])
        def create_wallet():
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
            AccountsFileManager.get_instance().get_loaded_account().add_wallet(wallet)
            return {"walletType": str(wallet_type), "walletName": wallet_name, "walletAddress": wallet.address}, 200


        @socket.on('connect', ws_prefix+'/ws')
        def handle_connect(auth):
            print('got client connection w/ auth: {}'.format(auth))

        @socket.on('disconnect', ws_prefix+'/ws')
        def handle_disconnect(reason):
            print('got client disconnect w/ reason: {}'.format(reason))




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

        self.socket = socket
        self.ws_prefix = ws_prefix
        api_bp.register_blueprint(crypto_bp)
        
        
        
        
        


    def send_socket_message(self, channel: str, message: dict):
        self.socket.emit(channel, message, namespace=self.ws_prefix+"/ws")







