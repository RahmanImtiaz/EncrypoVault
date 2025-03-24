# import os
# import signal
# import sys
# import threading
# import atexit
#
# from webserver import Flask, send_from_directory, request
# import webview
# from API import WebviewAPI
#
# app = Flask(__name__)
# live_mode = True
# if sys.platform == 'darwin':  # Check if running on macOS
#     live_mode = False
# port = 9209
#
# server_running = True
# shutdown_event = threading.Event()  # Add this to coordinate shutdown
#
# @app.route('/<path:path>')
# def send_file(path):
#     return send_from_directory('../src-frontend/dist', path)
#
# @app.route('/shutdown')
# def shutdown_server():
#     """Shutdown route for macOS."""
#     func = request.environ.get('werkzeug.server.shutdown')
#     if func is None:
#         raise RuntimeError('Not running with the Werkzeug Server')
#     func()
#     return 'Server shutting down...'
#
# def run_server():
#     app.run(host='localhost', port=port)
#
# def close_server():
#     """Send a signal to stop the Flask server."""
#     global server_running
#     server_running = False
#
#     shutdown_event.set()
#
#     try:
#         import requests
#
#         shutdown_thread = threading.Thread(
#             target=lambda: requests.get(f'http://localhost:{port}/shutdown', timeout=1.0)
#         )
#         shutdown_thread.daemon = True  # Make it a daemon so it doesn't block program exit
#         shutdown_thread.start()
#     except Exception as e:
#         print(f"Error shutting down server: {e}")
#
# def on_close(window):
#     close_server()
#     window.destroy()  # Close the window
#
# atexit.register(close_server)
#
# server_thread = threading.Thread(target=run_server)
# server_thread.daemon = True  # Make it a daemon thread so it doesn't block program exit
# server_thread.start()
#
# # Create API and window
# webview_api = WebviewAPI()
# url = f"http://localhost:{port}/index.html"
# if live_mode:
#     url = f"http://localhost:3928/index.html"
#
# window = webview.create_window("EncryptoVault", url, js_api=webview_api)
#
# window.events.closed += on_close
#
# # Start the webview
# webview.start(debug=True)

import os
import sys
from PySide6.QtCore import QUrl
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView

from webserver.server import FlaskServer


class MainWindow(QMainWindow):

    def closeEvent(self, event):
        self.webserver.on_close()
        event.accept()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("React with PySide6")
        # Create a QWebEngineView widget
        self.webserver = FlaskServer()
        self.browser = QWebEngineView(self)
        self.setCentralWidget(self.browser)

        # Build path to your React app's index.html.
        # For example, if your React build folder is in the same directory:
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src-frontend", "dist", "index.html"))
        print(f"file path: {file_path}")
        # local_url = QUrl.fromLocalFile(file_path)
        local_url= QUrl("http://localhost:9209/index.html")
        self.browser.setUrl(local_url)


        # Create a QShortcut for F12 to toggle/open the dev tools.
        self.dev_tools_shortcut = QShortcut(QKeySequence("F12"), self)
        self.dev_tools_shortcut.activated.connect(self.open_dev_tools)

        # Prepare the dev tools QWebEngineView but don't show it yet.
        self.dev_tools_view = QWebEngineView()
        self.dev_tools_view.resize(800, 600)
        self.dev_tools_view.setWindowTitle("Developer Tools")


    def open_dev_tools(self):
        # Connect the dev tools page to the main browser page
        self.browser.page().setDevToolsPage(self.dev_tools_view.page())
        # Show the dev tools window
        self.dev_tools_view.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1024, 768)
    window.show()
    sys.exit(app.exec())
