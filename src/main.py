import os
import signal

from flask import Flask, send_from_directory
import webview
import threading
from API import WebviewAPI

app = Flask(__name__)
port = 9209

server_running = True

@app.route('/<path:path>')
def send_file(path):
    return send_from_directory('../src-frontend/dist', path)

def run_server():
    app.run(host='localhost', port=port)


def close_server():
    """Send a signal to stop the Flask server."""
    global server_running
    server_running = False

    os.kill(os.getpid(), signal.SIGINT)


def on_close(ww_window: webview.Window):
    close_server()
    ww_window.destroy()


thread = threading.Thread(target=run_server)
thread.start()

webview_api = WebviewAPI()
window = webview.create_window("Hallo", f"http://localhost:{port}/index.html", js_api=webview_api)

window.events.closed += on_close


# Start the webview
webview.start(debug=True)