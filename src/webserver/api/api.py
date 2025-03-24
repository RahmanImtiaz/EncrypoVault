from flask import Blueprint, Flask

from .accounts import AccountRoutes


class ApiRoutes:
    def __init__(self, app: Flask):
        api_bp = Blueprint('accounts', __name__, url_prefix='/api')
        AccountRoutes(api_bp)
        app.register_blueprint(api_bp)
