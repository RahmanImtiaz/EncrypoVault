import sys
import time

def authenticate_with_touch_id(reason="Authenticate to access EncryptoVault"):
    """
    Shows a native macOS Touch ID prompt and returns True if successful.
    
    Args:
        reason (str): The reason displayed to the user in the Touch ID prompt
        
    Returns:
        bool: True if authentication succeeded, False otherwise
    """
    if sys.platform != "darwin":
        print("Touch ID is only available on macOS")
        return False
        
    try:
        from LocalAuthentication import LAContext, LAPolicyDeviceOwnerAuthenticationWithBiometrics
        
        # Create authentication context
        context = LAContext.new()
        
        # Check if Touch ID is available
        can_evaluate, error = context.canEvaluatePolicy_error_(
            LAPolicyDeviceOwnerAuthenticationWithBiometrics, 
            None
        )
        
        if not can_evaluate:
            print(f"Touch ID not available: {error}")
            return False
        
        # Using a list to store result from callback
        result = [False]
        
        def callback(success, error):
            """Callback when Touch ID verification completes"""
            result[0] = success
            if error:
                print(f"Touch ID error: {error}")
        
        # Request Touch ID authentication
        context.evaluatePolicy_localizedReason_reply_(
            LAPolicyDeviceOwnerAuthenticationWithBiometrics,
            reason,
            callback
        )
        
        # Wait for Touch ID result (with timeout)
        timeout = 10  # seconds
        interval = 0.1
        elapsed = 0
        while elapsed < timeout and not result[0]:
            time.sleep(interval)
            elapsed += interval
        
        return result[0]
    except Exception as e:
        print(f"Error using Touch ID: {str(e)}")
        return False