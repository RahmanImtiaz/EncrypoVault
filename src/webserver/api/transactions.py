from flask import Blueprint, jsonify

from AccountsFileManager import AccountsFileManager


class TransactionsRoutes:
    def __init__(self, api_bp: Blueprint):
        tx_bp = Blueprint('transactions', __name__, url_prefix='/transactions')



        api_bp.register_blueprint(tx_bp)