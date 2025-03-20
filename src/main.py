import webview

from API import WebviewAPI

webview_api = WebviewAPI()

webview.create_window("Hallo","../src-frontend/dist/index.html", js_api=webview_api)
webview.start(debug=True)