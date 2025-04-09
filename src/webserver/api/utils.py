import sys

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from flask import Blueprint, request, jsonify

from AccountsFileManager import AccountsFileManager
from AuthenticationManager import AuthenticationManager


class UtilRoutes:
    def __init__(self, api_bp: Blueprint):
        utils_bp = Blueprint('utils', __name__, url_prefix='/utils')

        @utils_bp.route('/os', methods=['GET'])
        def login():
            return jsonify({"os": sys.platform}), 200

        @utils_bp.route('/shutdown', methods=['POST'])
        def shutdown():
            """Shutdown route for the Flask server."""
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                print("Not running with the Werkzeug Server. Attempting alternative shutdown.")
                import os
                os._exit(0)
            func()
            return jsonify({"message": "Server shutting down..."}), 200

        @utils_bp.route("/open_page", methods=["POST"])
        def open_page():
            data = request.get_json()
            if not data or "url" not in data:
                return jsonify({"message": "No url provided."}), 400
            url = data["url"]
            url = QUrl(url)
            QDesktopServices.openUrl(url)

            return jsonify({"url": url.toString()}), 200

        api_bp.register_blueprint(utils_bp)