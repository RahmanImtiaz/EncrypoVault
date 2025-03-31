import logging
import os
import signal
import sys
import threading
import atexit

from flask import Flask, send_from_directory, request, jsonify

from AccountsFileManager import AccountsFileManager
from webserver.api.api import ApiRoutes
from API import WebviewAPI


class FlaskServer:


    server_running = True
    shutdown_event = threading.Event()  # Add this to coordinate shutdown

    def __init__(self):
        self.app = Flask(__name__)
        self.port = 9209
        self.api = WebviewAPI()


        # register api routes (the ones starting from /api)
        ApiRoutes(self.app)

        self.register_portfolio_routes()
        self.register_contacts_routes()

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

    def register_portfolio_routes(self):
        """Register the portfolio-related routes with the Flask app"""
        
        @self.app.route('/api/portfolio/balance', methods=['GET'])
        def get_portfolio_balance():
            try:
                # Call the API method to get the portfolio balance
                balance = self.api.get_portfolio_balance()
                return jsonify({"balance": balance})
            except Exception as e:
                print(f"Error getting portfolio balance: {str(e)}")
                return jsonify({"error": str(e)}), 500
                
        @self.app.route('/api/portfolio/wallets', methods=['GET'])
        def get_portfolio_wallets():
            try:
                # Call the API method to get all wallets
                wallets = self.api.get_portfolio_wallets()
                return jsonify({"wallets": wallets})
            except Exception as e:
                print(f"Error getting wallets: {str(e)}")
                return jsonify({"error": str(e)}), 500
            
    def register_contacts_routes(self):
        """Register contact-related routes with the Flask app"""
        
        @self.app.route('/api/contacts/list', methods=['GET'])
        def get_contacts():
            try:
                contacts = self.api.get_contacts()
                contact_list = [{"name": name, "address": address} for name, address in contacts.items()]
                return jsonify({"contacts": contact_list})
            except Exception as e:
                print(f"Error getting contacts: {str(e)}")
                return jsonify({"error": str(e)}), 500
                
        @self.app.route('/api/contacts/add', methods=['POST'])
        def add_contact():
            try:
                data = request.json
                if not data or 'name' not in data or 'address' not in data:
                    return jsonify({"error": "Missing name or address"}), 400
                    
                success = self.api.add_contact(data['name'], data['address'])
                if success:
                    return jsonify({"success": True, "message": "Contact added successfully"})
                else:
                    return jsonify({"error": "Failed to add contact"}), 500
            except Exception as e:
                print(f"Error adding contact: {str(e)}")
                return jsonify({"error": str(e)}), 500
        
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
