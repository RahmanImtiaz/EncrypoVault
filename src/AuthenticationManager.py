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
    def get_instance() -> 'AuthenticationManager':
        """Get the singleton instance of AuthenticationManager"""
        if AuthenticationManager._AuthenticationManager is None:
            AuthenticationManager()
        return AuthenticationManager._AuthenticationManager
    
    def authenticate_account(self, account_name, password, biometrics):
        """Authenticate account using account name (string)"""
        print(f"authenticate_account received: account_name={account_name}, password_type={type(password)}, biometrics_type={type(biometrics)}")
        
        if not self.ensure_secure_boot():
            raise Exception("Secure boot is not enabled. Cannot authenticate account as biometrics cannot be trusted.")
        
        if AuditLog.get_instance().get_entries_in_range(datetime.now() - timedelta(minutes=10), datetime.now()).count() > 6:
            raise Exception("Too many failed attempts. Account locked.")
        
        print(f"Authenticating account {account_name}...")
        AuditLog.get_instance().add_entry(account_name, datetime.now(), "ATTEMPTING")

        # Ensure proper types before generating key
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        if not isinstance(biometrics, bytes):
            if isinstance(biometrics, str):
                biometrics = biometrics.encode('utf-8')
            elif biometrics is None:
                biometrics = b''
            else:
                biometrics = str(biometrics).encode('utf-8')
        
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
            if sys.platform != "darwin":
                print("Not macOS, returning empty bytes")
                return b''  # Return empty bytes if not macOS
                    
            from macos_touch_id import authenticate_with_touch_id
            print("Calling Touch ID authentication")
            biometric_data = authenticate_with_touch_id(reason="EncryptoVault Authentication")
            
            print(f"Touch ID returned: {type(biometric_data)}")
            
            # Ensure we always return bytes
            if biometric_data is None:
                print("Touch ID returned None, converting to empty bytes")
                return b''
            elif isinstance(biometric_data, str):
                print("Touch ID returned string, encoding to bytes")
                return biometric_data.encode('utf-8')
            elif isinstance(biometric_data, bool):
                print(f"Touch ID returned boolean: {biometric_data}")
                # If we got a boolean response instead of biometric data
                return b'touch_id_verified' if biometric_data else b''
            elif isinstance(biometric_data, bytes):
                print("Touch ID returned bytes, using directly")
                if biometric_data == b'PASSWORD_FALLBACK':
                    print("Touch ID unavailable, should use password fallback")
                    return b'PASSWORD_FALLBACK'
                return biometric_data
            else:
                print(f"Touch ID returned unknown type: {type(biometric_data)}")
                # For any other type, convert to string then bytes
                return str(biometric_data).encode('utf-8')
        
        except Exception as e:
            print(f"Error capturing biometrics: {str(e)}")
            raise

    def _generate_key(self, password, biometrics):
        """Generate a key using password and biometric data"""
        print(f"_generate_key received password type: {type(password)}")
        print(f"_generate_key received biometrics type: {type(biometrics)}")
        
        # Ensure password is bytes
        if not isinstance(password, bytes):
            print("Converting password to bytes")
            if isinstance(password, str):
                password = password.encode('utf-8')
            else:
                password = str(password).encode('utf-8')
        
        # Ensure biometrics is bytes
        if not isinstance(biometrics, bytes):
            print("Converting biometrics to bytes")
            if isinstance(biometrics, str):
                biometrics = biometrics.encode('utf-8')
            elif biometrics is None:
                biometrics = b''
            else:
                biometrics = str(biometrics).encode('utf-8')
        
        digest = hashes.Hash(hashes.SHA256())
        digest.update(password)
        digest.update(biometrics)
        out = digest.finalize()
        return out

    def ensure_secure_boot(self) -> bool:
        if sys.platform == 'win32':
            import winreg

            # noinspection SqlNoDataSourceInspection
            try:
                reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
                key = winreg.OpenKey(reg, r"SYSTEM\CurrentControlSet\Control\SecureBoot\State")

                val = winreg.QueryValueEx(key, "UEFISecureBootEnabled")
                return val[0] == 1
            except Exception as e:
                print(f"Error querying for uefi secure boot: {str(e)}")
            return False
        elif sys.platform == 'darwin':
            # for mac we can always assume secure boot
            return True
        elif sys.platform == 'linux':
            # for linux we can check the secure boot status, yeah we dont support linux but just for future if we end up with extra time
            return os.path.exists("/sys/firmware/efi") and os.path.exists("/proc/sys/kernel/secure_boot")
        else:
            return False