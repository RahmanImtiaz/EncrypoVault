from flask import Blueprint, jsonify

from AccountsFileManager import AccountsFileManager
from AccountType import AccountType


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

        @acc_bp.route('/current/switch-type', methods=['POST'])
        def switch_account_type():
            try:
                account = AccountsFileManager.get_instance().get_loaded_account()
                current_type = account.get_account_type()
                
                if current_type.get_type_name() == "Advanced":
                    account.set_account_type(current_type.switch_to_beginner())
                    new_type = "Beginner"
                elif current_type.get_type_name() == "Beginner": 
                    account.set_account_type(current_type.switch_to_advanced()) 
                    new_type = "Advanced"
                else:
                    return jsonify({"error": "Cannot switch type for this account"}), 400
                    
                AccountsFileManager.get_instance().save_account(account)
                
                return jsonify({
                    "success": True, 
                    "accountType": new_type,
                    "message": f"Successfully switched to {new_type} mode"
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500
    

        api_bp.register_blueprint(acc_bp)