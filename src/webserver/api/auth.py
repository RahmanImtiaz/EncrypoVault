import sys
from flask import Blueprint, request, jsonify
import webauthn
from webauthn import options_to_json
from webauthn.helpers.structs import UserVerificationRequirement

from AuthenticationManager import AuthenticationManager
from AccountsFileManager import AccountsFileManager


class AuthRoutes:
    def __init__(self, api_bp: Blueprint):
        auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

        @auth_bp.route('/login', methods=['POST'])
        def login():
            data = request.get_json()
            if data is None or 'account_name' not in data or 'password' not in data:
                return jsonify({"error": "No data"}), 400
            try:
                # Platform-specific authentication handling
                if sys.platform == 'darwin':
                    # For macOS: Use Touch ID
                    from macos_touch_id import authenticate_with_touch_id
                    
                    if authenticate_with_touch_id():
                        # Touch ID successful, now authenticate account with password
                        AuthenticationManager.get_instance().authenticate_account(
                            data['account_name'], 
                            data['password'],
                            None  # No WebAuthn for macOS
                        )
                        return jsonify({"success": True}), 200
                    else:
                        return jsonify({"error": "Touch ID authentication failed"}), 401
                else:
                    # For Windows: Use WebAuthn
                    biometrics = data.get('biometrics')  # Use .get() method instead of direct access
                    
                    # Authenticate with both password and biometrics
                    AuthenticationManager.get_instance().authenticate_account(
                        data['account_name'], 
                        data['password'],
                        biometrics
                    )
                    return jsonify({"success": True}), 200
                    
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @auth_bp.route('/webauthn_auth', methods=['GET'])
        def create_auth_options():
            # Only used for Windows, not macOS
            return options_to_json(webauthn.generate_authentication_options(
                challenge=bytes.fromhex("c99a420cd739ff56632d3262582df92c43d50bd64e045374422ca3ed68826e5e"), 
                rp_id="localhost", 
                user_verification=UserVerificationRequirement.REQUIRED
            ))
            
        @auth_bp.route('/register', methods=['POST'])
        def register():
            data = request.get_json()
            if data is None or 'account_name' not in data or 'password' not in data or 'account_type' not in data:
                return jsonify({"error": "Missing required registration data"}), 400
                
            try:
                # Platform-specific registration handling
                if sys.platform == 'darwin' and data.get('use_touch_id', False):
                    # For macOS: Use Touch ID
                    from macos_touch_id import authenticate_with_touch_id
                    
                    if authenticate_with_touch_id("Verify your identity to create a new account"):
                        # Touch ID successful, now create the account
                        account = AccountsFileManager.get_instance().create_account(
                            data['account_name'], 
                            data['account_type'],
                            data['password']
                        )
                        return jsonify({"success": True, "account": account}), 200
                    else:
                        return jsonify({"error": "Touch ID verification failed"}), 401
                else:
                    # For Windows: Use WebAuthn
                    biometrics = data.get('biometrics')
                    
                    # Create account with biometrics data
                    account = AccountsFileManager.get_instance().create_account(
                        data['account_name'], 
                        data['account_type'],
                        data['password'],
                        biometrics
                    )
                    return jsonify({"success": True, "account": account}), 200
                    
            except Exception as e:
                return jsonify({"error": str(e)}), 500
                
        @auth_bp.route('/webauthn_reg/<account_name>', methods=['GET'])
        def create_reg_options(account_name):
            # Only generate WebAuthn registration options for non-macOS platforms
            if sys.platform != 'darwin':
                try:
                    options = webauthn.generate_registration_options(
                        challenge=bytes.fromhex("c99a420cd739ff56632d3262582df92c43d50bd64e045374422ca3ed68826e5e"),
                        rp_id="localhost",
                        rp_name=account_name,
                        user_name=account_name
                    )
                    return options_to_json(options), 200
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            else:
                # For macOS, return a specific response indicating Touch ID should be used
                return jsonify({"useTouchID": True}), 200
            
        api_bp.register_blueprint(auth_bp)