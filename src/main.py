import webview

from src.API import WebviewAPI
from src.AccountsFileManager import AccountsFileManager
from src.AuthenticationManager import AuthenticationManager

webview_api = WebviewAPI()

webview.create_window("Hallo","../src-frontend/dist/index.html", js_api=webview_api)
webview.start()