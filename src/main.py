import webview

from src.AccountsFileManager import AccountsFileManager
from src.AuthenticationManager import AuthenticationManager

webview.create_window("Hallo","../src-frontend/dist/index.html", js_api={"AccountsFileManager": AccountsFileManager.get_instance(), "AuthenticationManager": AuthenticationManager.get_instance()})
webview.start()