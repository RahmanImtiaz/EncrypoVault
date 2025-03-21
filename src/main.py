import os
import signal
import sys
import threading
import atexit

from flask import Flask, send_from_directory, request
import webview
from API import WebviewAPI

app = Flask(__name__)
live_mode = True
if sys.platform == 'darwin':  # Check if running on macOS
    live_mode = False  
port = 9209

server_running = True
shutdown_event = threading.Event()  # Add this to coordinate shutdown

@app.route('/<path:path>')
def send_file(path):
    return send_from_directory('../src-frontend/dist', path)

@app.route('/shutdown')
def shutdown_server():
    """Shutdown route for macOS."""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

def run_server():
    app.run(host='localhost', port=port)

def close_server():
    """Send a signal to stop the Flask server."""
    global server_running
    server_running = False
    
    shutdown_event.set()
    
    try:
        import requests
        
        shutdown_thread = threading.Thread(
            target=lambda: requests.get(f'http://localhost:{port}/shutdown', timeout=1.0)
        )
        shutdown_thread.daemon = True  # Make it a daemon so it doesn't block program exit
        shutdown_thread.start()
    except Exception as e:
        print(f"Error shutting down server: {e}")

def on_close(window):
    close_server()
    window.destroy()  # Close the window

atexit.register(close_server)

server_thread = threading.Thread(target=run_server)
server_thread.daemon = True  # Make it a daemon thread so it doesn't block program exit
server_thread.start()

# Create API and window
webview_api = WebviewAPI()
url = f"http://localhost:{port}/index.html"
if live_mode:
    url = f"http://localhost:3928/index.html"

window = webview.create_window("EncryptoVault", url, js_api=webview_api)

window.events.closed += on_close

# Start the webview
webview.start(debug=True)