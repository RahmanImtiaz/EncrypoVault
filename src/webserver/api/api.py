from flask import Blueprint, Flask

from .accounts import AccountRoutes
from .auth import AuthRoutes
from .utils import UtilRoutes


class ApiRoutes:
    def __init__(self, app: Flask):
        api_bp = Blueprint('accounts', __name__, url_prefix='/api')
        AccountRoutes(api_bp)
        AuthRoutes(api_bp)
        UtilRoutes(api_bp)
        app.register_blueprint(api_bp)
