from flask import Blueprint, jsonify, request
from AccountsFileManager import AccountsFileManager

class ContactRoutes:
    def __init__(self, api_bp: Blueprint):
        contacts_bp = Blueprint('contacts', __name__, url_prefix="/contacts")

        @contacts_bp.route('/list', methods=['GET'])
        def list_contacts():
            """Get all contacts for the current account"""
            # Get current account
            account_manager = AccountsFileManager.get_instance()
            current_account = account_manager.get_loaded_account()

            if not current_account:
                return jsonify({"error": "No account is currently logged in"}), 401

            # Get contacts
            try:
                contacts = current_account.get_contacts() or {}
                contact_list = [{"name": name, "address": address} for name, address in contacts.items()]
                return jsonify({"contacts": contact_list}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @contacts_bp.route('/add', methods=['POST'])
        def add_contact():
            """Add a contact to the current account"""
            # Get current account
            account_manager = AccountsFileManager.get_instance()
            current_account = account_manager.get_loaded_account()

            if not current_account:
                return jsonify({"error": "No account is currently logged in"}), 401

            # Get request data
            data = request.json
            if not data or 'name' not in data or 'address' not in data:
                return jsonify({"error": "Missing name or address"}), 400

            # Add contact
            try:
                current_account.add_contact(data['name'], data['address'])
                account_manager.save_account(current_account)
                return jsonify({"success": True, "message": "Contact added successfully"}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        api_bp.register_blueprint(contacts_bp)
