#!/usr/bin/env python3

import sys
import time
from Foundation import NSRunLoop, NSDate

def authenticate_with_touch_id(reason="Authentication required"):
    """
    Displays macOS authentication dialog with password fallback
    Returns True if authenticated, False if failed/canceled
    """
    if sys.platform != "darwin":
        print("Error: This feature requires macOS")
        return False

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
            return False

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
            
        return auth_result[0] if auth_result[0] is not None else False

    except ImportError:
        print("Missing required framework: pip install pyobjc")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False