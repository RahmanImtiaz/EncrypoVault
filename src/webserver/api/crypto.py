import sys

from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO

from AccountsFileManager import AccountsFileManager
from AuthenticationManager import AuthenticationManager


class CryptoRoutes:
    def __init__(self, api_bp: Blueprint, app):
        crypto_bp = Blueprint('crypto', __name__, url_prefix='/crypto')

        socket = SocketIO(app, logger=False, engineio_logger=False)

        socket.init_app(app)

        app.socketio = socket

        ws_prefix = api_bp.url_prefix+crypto_bp.url_prefix

        @socket.on('connect', ws_prefix+'/ws')
        def handle_connect(ws):
            print('got client connection from {}'.format(ws))

        @socket.on('disconnect', ws_prefix+'/ws')
        def handle_disconnect(ws):
            print('got client disconnect from {}'.format(ws))

        @socket.on('message', ws_prefix+'/ws')
        def handle_message(ws, message):
            print('got message {} from {}'.format(message, ws))

        api_bp.register_blueprint(crypto_bp)
