import sys

import webauthn
from flask import Blueprint, request, jsonify
from webauthn import options_to_json
from webauthn.helpers.structs import UserVerificationRequirement

from AccountsFileManager import AccountsFileManager
from AuthenticationManager import AuthenticationManager


class AuthRoutes:
    def __init__(self, api_bp: Blueprint):
        auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

        @auth_bp.route('/login', methods=['POST'])
        def login():
            data = request.get_json()
            if data is None or 'account_name' not in data or 'password' not in data:
                return jsonify({"error": "No data"}), 400
            try:
                if data.biometrics is None:
                    if sys.platform == 'darwin':
                        data.biometrics = AuthenticationManager.get_instance().prompt_for_biometrics()
                AuthenticationManager.get_instance().authenticate_account(data['account_name'], data['password'],
                                                                          data['biometrics'])
                return jsonify({"success": True}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @auth_bp.route('/webauthn_auth', methods=['GET'])
        def create_auth_options():
            return options_to_json(webauthn.generate_authentication_options(challenge=bytes.fromhex("c99a420cd739ff56632d3262582df92c43d50bd64e045374422ca3ed68826e5e"), rp_id="localhost", user_verification=UserVerificationRequirement.REQUIRED))

        @auth_bp.route('/webauthn_reg/<account_name>', methods=['GET'])
        def create_reg_options(account_name):
            return options_to_json(webauthn.generate_registration_options(
                challenge=bytes.fromhex("c99a420cd739ff56632d3262582df92c43d50bd64e045374422ca3ed68826e5e"),
                rp_id="localhost", rp_name=account_name, user_name=account_name)), 200

        api_bp.register_blueprint(auth_bp)