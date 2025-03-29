from flask import Blueprint, Flask

from .accounts import AccountRoutes
from .auth import AuthRoutes
from .crypto import CryptoRoutes
from .utils import UtilRoutes


class ApiRoutes:
    def __init__(self, app: Flask):
        api_bp = Blueprint('api', __name__, url_prefix='/api')
        AccountRoutes(api_bp)
        AuthRoutes(api_bp)
        UtilRoutes(api_bp)
        CryptoRoutes(api_bp, app)
        app.register_blueprint(api_bp)
