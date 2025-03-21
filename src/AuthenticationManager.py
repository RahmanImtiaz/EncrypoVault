import sys
import os
from AuditLog import AuditLog
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes
from AccountsFileManager import AccountsFileManager
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
    
    def authenticate_account(self, account_name, password, biometrics):
        """Authenticate account using account name (string)"""
        if not self.ensure_secure_boot():
            raise Exception("Secure boot is not enabled. Cannot authenticate account as biometrics cannot be trusted.")
        if AuditLog.get_instance().get_entries_in_range(datetime.now() - timedelta(minutes=10), datetime.now()).count() > 6:
            raise Exception("Too many failed attempts. Account locked.")
        print(f"Authenticating account {account_name}...")
        AuditLog.get_instance().add_entry(account_name, datetime.now(), "ATTEMPTING")

        key = self._generate_key(password, biometrics)
        account = AccountsFileManager.get_instance().load_account(key, account_name)
        if account is None:
            AuditLog.get_instance().add_entry(account_name, datetime.now(), "FAILED")
            raise Exception("Invalid credentials (or account does not exist)")
        else:
            AuditLog.get_instance().add_entry(account_name, datetime.now(), "SUCCESS")
        return account

    def prompt_for_password(self):
        """Prompt for authentication password"""
        try:
            # For testing purposes, use test_password if available
            if hasattr(self, 'test_password'):
                if isinstance(self.test_password, str):
                    return self.test_password.encode('utf-8')
                elif isinstance(self.test_password, bytes):
                    return self.test_password
                else:
                    raise TypeError("test_password must be str or bytes")
                    
            # In a real implementation, show secure password dialog
            import getpass
            password = getpass.getpass("Enter password: ")
            return password.encode('utf-8')
        except Exception as e:
            print(f"Error prompting for password: {str(e)}")
            raise

    def prompt_for_biometrics(self):
        """Prompt for biometric authentication"""
        try:
            # For testing purposes, use test_biometrics if available
            if hasattr(self, 'test_biometrics'):
                return self.test_biometrics
                
            # In real implementation, this would interface with WebAuthn/biometric hardware
            # For testing, use a default value
            print("Simulating biometric scan...")
            return b"test_biometric_data"
        except Exception as e:
            print(f"Error capturing biometrics: {str(e)}")
            raise

    def _generate_key(self, password, biometrics):
        """Generate a key using password and biometric data"""
        digest = hashes.Hash(hashes.SHA256())
        digest.update(password)
        digest.update(biometrics)
        out = digest.finalize()
        return out

    def ensure_secure_boot(self):
        if sys.platform == 'win32':
            import wmi
            w = wmi.WMI()

            # noinspection SqlNoDataSourceInspection
            result = w.query("SELECT SecureBootEnabled FROM Win32_BIOS")

            return len(result) > 0 and result[0].SecureBootEnabled
        elif sys.platform == 'darwin':
            # for mac we can always assume secure boot
            return True
        elif sys.platform == 'linux':
            # for linux we can check the secure boot status, yeah we dont support linux but just for future if we end up with extra time
            return os.path.exists("/sys/firmware/efi") and os.path.exists("/proc/sys/kernel/secure_boot")
        else:
            return False