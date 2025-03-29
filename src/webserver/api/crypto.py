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
        def handle_connect(auth):
            print('got client connection w/ auth: {}'.format(auth))

        @socket.on('disconnect', ws_prefix+'/ws')
        def handle_disconnect(reason):
            print('got client disconnect w/ reason: {}'.format(reason))

        @socket.on('message', ws_prefix+'/ws')
        def handle_message(message):
            print('got message {}'.format(message))

        api_bp.register_blueprint(crypto_bp)
