import json
import sys
from json import JSONDecodeError

from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO

from AccountsFileManager import AccountsFileManager
from AuthenticationManager import AuthenticationManager
from CryptoObserver import CryptoObserver, ConcreteCryptoObserver
from ExchangeSocket import CryptoWatch, ExchangeSocket


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


        @socket.on('connect', ws_prefix+'/ws')
        def handle_connect(auth):
            print('got client connection w/ auth: {}'.format(auth))

        @socket.on('disconnect', ws_prefix+'/ws')
        def handle_disconnect(reason):
            print('got client disconnect w/ reason: {}'.format(reason))




        @socket.on('message', ws_prefix+'/ws')
        def handle_message(message=None):
            if message is None:
                self.send_socket_message("error", {"error": "got nothing in socket, bruh??"})
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
            print('got command {}'.format(data))

            cmd = data['command']

            match cmd:
                case 'add_crypto':
                    if 'crypto_id' not in data:
                        self.send_socket_message("server_error", {"error": "missing crypto_id"})
                    else:
                        crypto_id = data['crypto_id']
                        ExchangeSocket().add_crypto(crypto_id)
                        self.send_socket_message("message", {"crypto_id": crypto_id})

        self.socket = socket
        self.ws_prefix = ws_prefix
        api_bp.register_blueprint(crypto_bp)


    def send_socket_message(self, channel: str, message: dict):
        self.socket.emit(channel, message, namespace=self.ws_prefix+"/ws")







