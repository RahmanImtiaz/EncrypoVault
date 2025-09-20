from flask import Blueprint, Flask

from .accounts import AccountRoutes
from .auth import AuthRoutes
from .contacts import ContactRoutes
from .crypto import CryptoRoutes
from .transactions import TransactionsRoutes
from .utils import UtilRoutes
from .portfolio import PortfolioRoutes


class ApiRoutes:
    def __init__(self, app: Flask):
        api_bp = Blueprint('api', __name__, url_prefix='/api')
        AccountRoutes(api_bp)
        AuthRoutes(api_bp)
        UtilRoutes(api_bp)
        ContactRoutes(api_bp)
        CryptoRoutes(api_bp, app)
        TransactionsRoutes(api_bp)
        PortfolioRoutes(api_bp)
        app.register_blueprint(api_bp)
