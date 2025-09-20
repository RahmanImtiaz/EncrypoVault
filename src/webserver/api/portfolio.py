from flask import Blueprint, jsonify, request
from AccountsFileManager import AccountsFileManager

class PortfolioRoutes:
    def __init__(self, app):
        self.app = app
        self.accounts_manager = AccountsFileManager()

        portfolio_bp = Blueprint('portfolio', __name__, url_prefix="/portfolio")

        @portfolio_bp.route('/balance', methods=['GET'])
        def get_portfolio_balance():
            try:
                account = AccountsFileManager.get_instance().get_loaded_account()
                if not account:
                    return jsonify({"error": "No account loaded"}), 401
                # Update balances if needed
                account.portfolio.update_all_balances()
                balance = account.portfolio.get_total_balance()
                return jsonify({"balance": balance})
            except Exception as e:
                print(f"Error getting portfolio balance: {str(e)}")
                return jsonify({"error": str(e)}), 500

        @portfolio_bp.route('/wallets', methods=['GET'])
        def get_portfolio_wallets():
            try:
                account = AccountsFileManager.get_instance().get_loaded_account()
                if not account:
                    return jsonify({"error": "No account loaded"}), 401
                account.portfolio.update_all_balances()
                wallets = account.portfolio.get_all_wallets()
                wallets_data = [
                    {
                        "name": wallet.name,
                        "balance": wallet.balance,
                        "address": wallet.address,
                        "coin_symbol": wallet.coin_symbol,
                        "holdings": wallet.holdings  # or format as needed
                    }
                    for wallet in wallets
                ]
                return jsonify({"wallets": wallets_data})
            except Exception as e:
                print(f"Error getting wallets: {str(e)}")
                return jsonify({"error": str(e)}), 500
            
        portfolio_bp.add_url_rule('/balance', view_func=get_portfolio_balance, methods=['GET'])
        portfolio_bp.add_url_rule('/wallets', view_func=get_portfolio_wallets, methods=['GET'])    

        
        