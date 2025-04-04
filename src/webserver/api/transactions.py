from flask import Blueprint, jsonify

from AccountsFileManager import AccountsFileManager


class TransactionsRoutes:
    def __init__(self, api_bp: Blueprint):
        tx_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

        @tx_bp.route("/", methods=['GET'])
        def get_all_transactions():
            return AccountsFileManager.get_instance().get_loaded_account().transactionLog.toJSON(), 200

        @tx_bp.route("/<txid>", methods=['GET'])
        def get_transaction(txid):
            return AccountsFileManager.get_instance().get_loaded_account().transactionLog.search(txid).toJSON(), 200

        api_bp.register_blueprint(tx_bp)