from flask import Blueprint

from AccountsFileManager import AccountsFileManager


class AccountRoutes:
    def __init__(self, api_bp: Blueprint):
        acc_bp = Blueprint('accounts', __name__, url_prefix='/accounts')

        @acc_bp.route('/current', methods=['GET'])
        def get_current_account():
            return AccountsFileManager.get_instance().get_loaded_account().toJSON()

        @acc_bp.route('/names', methods=['GET'])
        def get_account_names():
            return AccountsFileManager.get_instance().get_accounts()


        api_bp.register_blueprint(acc_bp)