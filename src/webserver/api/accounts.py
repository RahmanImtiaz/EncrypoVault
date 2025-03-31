from flask import Blueprint, jsonify

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

        @acc_bp.route('/current/recovery', methods=['GET'])
        def get_account_recovery():
            # TODO: biometrics protect this
            return jsonify(AccountsFileManager.get_instance().get_loaded_account().get_recovery_phrases())


        api_bp.register_blueprint(acc_bp)