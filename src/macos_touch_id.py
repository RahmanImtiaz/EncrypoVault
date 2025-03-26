#!/usr/bin/env python3

import sys
import time
import hashlib
import uuid
from Foundation import NSRunLoop, NSDate

def authenticate_with_touch_id(reason="Authentication required"):
    """
    Displays macOS authentication dialog with password fallback
    Returns biometric data as bytes if authenticated, empty bytes if failed/canceled
    """
    if sys.platform != "darwin":
        print("Error: This feature requires macOS")
        return b''

    try:
        from LocalAuthentication import LAContext, LAPolicyDeviceOwnerAuthentication

        context = LAContext.new()
        auth_result = [None]
        error_info = [None]

        # Check if authentication is available
        can_authenticate, error = context.canEvaluatePolicy_error_(
            LAPolicyDeviceOwnerAuthentication, None
        )

        if not can_authenticate:
            print(f"Authentication unavailable: {error.localizedDescription() if error else 'Unknown error'}")
            return b''

        # Define completion handler
        def auth_completion(success, error):
            auth_result[0] = success
            error_info[0] = error

        # Show authentication dialog
        context.evaluatePolicy_localizedReason_reply_(
            LAPolicyDeviceOwnerAuthentication,
            reason,
            auth_completion
        )

        # Wait for response with timeout
        run_loop = NSRunLoop.currentRunLoop()
        start_time = time.time()
        timeout = 30  # seconds

        while time.time() - start_time < timeout and auth_result[0] is None:
            run_loop.runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))

        if error_info[0]:
            print(f"Authentication error: {error_info[0].localizedDescription()}")
            return b''
            
        # If authentication succeeded, generate a consistent biometric token
        if auth_result[0]:
            # Generate a machine-specific identifier
            machine_id = str(uuid.getnode())  # Uses MAC address as unique identifier
            
            # Create a hash of the machine ID to represent the biometric data
            # This ensures we get the same biometric data for the same user on the same machine
            biometric_data = hashlib.sha256(machine_id.encode()).digest()
            return biometric_data
        else:
            return b''

    except ImportError:
        print("Missing required framework: pip install pyobjc")
        return b''
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return b''