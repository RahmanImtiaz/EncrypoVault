import logging
import os
import signal
import sys
import threading
import atexit
import asyncio
from flask import Flask, send_from_directory, request, jsonify

from webserver.api.api import ApiRoutes
from API import WebviewAPI
from ExchangeSocketCR import PriceSocket

class FlaskServer:


    server_running = True
    shutdown_event = threading.Event()  # Add this to coordinate shutdown

    def __init__(self):
        self.app = Flask(__name__)
        self.port = 9209
        self.api = WebviewAPI()
        self.price_socket = PriceSocket()
        self.start_price_socket()


        # register api routes (the ones starting from /api)
        ApiRoutes(self.app)

        @self.app.route('/<path:path>')
        @self.app.route("/", defaults={'path': 'index.html'})
        def send_file(path):
            # If the path starts with "api", let Flask return a 404 so API routes handle it
            if path.startswith("api"):
                return "Not Found", 404
            return send_from_directory('../../src-frontend/dist', path)

        self.server_thread = threading.Thread(target=self.run_server)

        atexit.register(self.close_server)

        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.daemon = True  # Make it a daemon thread so it doesn't block program exit
        self.server_thread.start()
            
    def start_price_socket(self):
        def run_socket():
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.price_socket.connect_to_exchange())
            loop.run_forever()
        threading.Thread(target=run_socket, daemon=True).start()
        
    def run_server(self):
        if self.app.socketio:
            self.app.logger.setLevel(logging.INFO)
            self.app.logger.propagate = True
            logging.getLogger('werkzeug').setLevel(logging.INFO)
            self.app.socketio.run(self.app, host='localhost', port=self.port)
            #self.app.run(host="localhost", port=self.port)
        else:
            print("Socket io not registered!!")

    def close_server(self):
        """Send a signal to stop the Flask server."""

        self.server_running = False

        self.shutdown_event.set()

        try:
            import requests

            shutdown_thread = threading.Thread(
                target=lambda: requests.post(f'http://localhost:{self.port}/api/utils/shutdown', timeout=1.0)
            )
            shutdown_thread.daemon = True  # Make it a daemon so it doesn't block program exit
            shutdown_thread.start()
        except Exception as e:
            print(f"Error shutting down server: {e}")

    def on_close(self):
        self.close_server()


    # Create API and window
