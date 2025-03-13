import os
class AuthenticationManager:
    """Singleton class for authentication of accounts"""
    _AuthenticationManager = None

    def __new__(cls):
        if cls._AuthenticationManager is None:
            cls._AuthenticationManager = super(AuthenticationManager, cls).__new__(cls)
            cls._AuthenticationManager.__initialized = False
        return cls._AuthenticationManager
    
    def __init__(self):
        if getattr(self, '_initialized', False):
            return
        
        self._initialized = True

    @staticmethod
    def get_instance():
        """Get the singleton instance of AuthenticationManager"""
        if AuthenticationManager._AuthenticationManager is None:
            AuthenticationManager()
        return AuthenticationManager._AuthenticationManager
    
    def authenticate_account(self, account_name):
        """Authenticate account using account name (string)"""
        pass

    def _generate_key(self):
        """Generate a key using password and biometric data"""
        # For testing purposes, we'll generate a random key
        # In a real implementation, this would combine password + biometric
        return os.urandom(32)  # 32 bytes for AES-256