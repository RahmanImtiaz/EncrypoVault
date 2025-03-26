import os
import signal
import sys
import threading
import atexit

from flask import Flask, send_from_directory, request

from AccountsFileManager import AccountsFileManager
from webserver.api.api import ApiRoutes


class FlaskServer:


    server_running = True
    shutdown_event = threading.Event()  # Add this to coordinate shutdown

    def __init__(self):
        self.app = Flask(__name__)
        self.port = 9209

        @self.app.route('/<path:path>')
        @self.app.route("/", defaults={'path': 'index.html'})
        def send_file(path):
            return send_from_directory('../../src-frontend/dist', path)


        # register api routes (the ones starting from /api)
        ApiRoutes(self.app)

        self.server_thread = threading.Thread(target=self.run_server)

        atexit.register(self.close_server)

        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.daemon = True  # Make it a daemon thread so it doesn't block program exit
        self.server_thread.start()

    def run_server(self):
        self.app.run(host='localhost', port=self.port)

    def close_server(self):
        """Send a signal to stop the Flask server."""

        self.server_running = False

        self.shutdown_event.set()

        try:
            import requests

            shutdown_thread = threading.Thread(
                target=lambda: requests.get(f'http://localhost:{self.port}/api/utils/shutdown', timeout=1.0)
            )
            shutdown_thread.daemon = True  # Make it a daemon so it doesn't block program exit
            shutdown_thread.start()
        except Exception as e:
            print(f"Error shutting down server: {e}")

    def on_close(self):
        self.close_server()



    # Create API and window
