import React, { useState, useEffect } from "react";
import {PublicKeyCredentialRequestOptionsJSON, startAuthentication} from '@simplewebauthn/browser';


import "./Login.css";

interface LoginProps {
  onLogin: () => void;
}

export function Login({ onLogin }: LoginProps) {

  const [selectedAccount, setSelectedAccount] = useState("demo_account");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [isPasswordVerified, _setIsPasswordVerified] = useState(false);
  const [useFallbackAuth, _setUseFallbackAuth] = useState(false);
  const [accounts, setAccounts] = useState<string[]>([])
  const [platform, setPlatform] = useState<string | null>(null);
  const [_isBiometricsSupported, setIsBiometricsSupported] = useState<boolean | null>(null);

  // Check biometric support when component mounts
  useEffect(() => {
    const checkBiometricSupport = async () => {
      try {
        const supported = await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();
        setIsBiometricsSupported(supported);
      } catch (err) {
        console.error('Error checking biometric support:', err);
        setIsBiometricsSupported(false);
      }
    };

    function detectPlatform() {
      // If pywebview is already available, use it immediately
      if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.get_platform()
          .then(platformInfo => {
            console.log("Platform detected:", platformInfo);
            setPlatform(platformInfo);
          })
          .catch(err => {
            console.error("Error detecting platform:", err);
            // Fallback detection using navigator.platform
            if (navigator.platform.indexOf('Mac') !== -1) {
              setPlatform('macos');
            } else if (navigator.platform.indexOf('Win') !== -1) {
              setPlatform('windows');
            } else {
              setPlatform('other');
            }
          });
      } else {
        // Otherwise wait for the pywebviewready event
        const readyHandler = async () => {
          try {
            if (window.pywebview && window.pywebview.api) {
              const platformInfo = await window.pywebview.api.get_platform();
              console.log("Platform detected after ready event:", platformInfo);
              setPlatform(platformInfo);
            }
          } catch (err) {
            console.error("Error detecting platform after ready event:", err);
            // Fallback detection
            if (navigator.platform.indexOf('Mac') !== -1) {
              setPlatform('macos');
            } else if (navigator.platform.indexOf('Win') !== -1) {
              setPlatform('windows');
            } else {
              setPlatform('other');
            }
          }
        };
  
        window.addEventListener("pywebviewready", readyHandler);
        return () => {
          window.removeEventListener("pywebviewready", readyHandler);
        };
      }
    }

    function fetchAccounts() {
      window.api.getAccountNames()
          .then(fetchedAccounts => {
            console.log("Accounts fetched:", fetchedAccounts);
            setAccounts(fetchedAccounts);
            // Set the selected account to the first account in the list if available
            if (fetchedAccounts && fetchedAccounts.length > 0) {
              setSelectedAccount(fetchedAccounts[0]);
            }
          })
          .catch(err => {
            console.error("Error fetching accounts:", err);
          });

    }

    checkBiometricSupport();
    fetchAccounts()
    detectPlatform();
  }, []);

  const handleBiometricAuth = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true);
    setError("");
    const platform = await window.api.getOS()
    try {
      if (platform === 'darwin') {
        // For macOS: Use Touch ID through the backend
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            account_name: selectedAccount,
            password: password
            // No biometrics for macOS - Touch ID is handled on backend
          }),
        });
        
        const data = await response.json();
        
        if (!response.ok) {
          throw new Error(data.error || 'Authentication failed');
        }
        
        onLogin();
      } else {
        // This will trigger the system's biometric prompt (fingerprint, Face ID, etc.)
        const authData: PublicKeyCredentialRequestOptionsJSON = await window.api.getWebauthnLoginOpts() as unknown as PublicKeyCredentialRequestOptionsJSON
        //const authData2 = {"challenge": "yZpCDNc5_1ZjLTJiWC35LEPVC9ZOBFN0Qiyj7WiCbl4", "timeout": 60000, "rpId": "localhost", "allowCredentials": [], "userVerification": "preferred"}
        console.log("Before")
        console.log(`authdata:`)
        console.log(authData)
        const webauthnResponse = await startAuthentication({optionsJSON: authData, useBrowserAutofill: false})
        console.log("After")
        await window.api.login(selectedAccount, password, webauthnResponse.response.authenticatorData)
        onLogin();
      }
      //onLogin();  //this is the code that should be deleted after, and the top bit needs to be uncommented.
    } catch (err) {
      console.error('Biometric auth error:', err);
      setError("You closed the OS login prompt!");
    } finally {
      setLoading(false);
    }
  };


  // const _handlePasswordSubmit = async (e: React.FormEvent) => {
  //   e.preventDefault();
  //   setLoading(true);
  //   setError("");
  //
  //   try {
  //     // Here you would verify with your backend
  //     //new changes from here. Remove the comments in the next three lines and remove everything else, make sure there is no space before }
  //     //const DEMO_PASSWORD = "demo123";
  //     //if (selectedAccount === "demo_account" && password !== DEMO_PASSWORD) {
  //     //  throw new Error("Invalid password for demo account (use: demo123)");
  //     // //}
  //     // const account = await window.pywebview.api.authenticate_account(selectedAccount, password);
  //     // console.log('Account verified:', account);
  //     //
  //     // if (account) {
  //     //   setIsPasswordVerified(true);
  //     //   onLogin();
  //     // }
  //     // else {
  //     //   throw new Error("Invalid credentials");
  //     // }
  //     //setIsPasswordVerified(true);
  //     //setLoading(false);
  //
  //      // First verify the account/password combination
  //
  //      const account = await window.pywebview.api.authenticate_account(selectedAccount, password, null);
  //      console.log('Credentials verified:', account);
  //
  //      if (account) {
  //        // Set password as verified but don't log in yet - this will show biometric screen
  //        _setIsPasswordVerified(true);
  //      } else {
  //        throw new Error("Invalid credentials");
  //      }
  //     //onLogin();
  //   } catch (err) {
  //     setError(err instanceof Error ? err.message : "Password verification failed");
  //     setLoading(false);
  //   }
  // };

  const handleDesktopAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      // Here you would verify with your backend using desktop password
      const DEMO_DESKTOP_PASSWORD = "desktop123";
      if (password !== DEMO_DESKTOP_PASSWORD) {
        throw new Error("Invalid desktop password (use: desktop123)");
      }

      onLogin();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Desktop authentication failed");
    } finally {
      setLoading(false);
    }
  };



  // Render biometric authentication screen
  const renderBiometricScreen = () => (
    <div className="biometric-auth-container">
      <h2 className="biometric-title">
        {platform === 'macos' ? 'Touch ID Authentication' : 'Fingerprint Authentication'}
      </h2>
      <div className="fingerprint-icon">
        <svg viewBox="0 0 24 24" width="64" height="64">
          <path fill="currentColor" d="M17.81 4.47c-.08 0-.16-.02-.23-.06C15.66 3.42 14 3 12.01 3c-1.98 0-3.86.47-5.57 1.41-.24.13-.54.04-.68-.2-.13-.24-.04-.54.2-.68C7.82 2.52 9.86 2 12.01 2c2.13 0 3.99.47 6.03 1.52.25.13.34.43.21.67-.09.18-.26.28-.44.28zM3.5 9.72c-.1 0-.2-.03-.29-.09-.23-.16-.28-.47-.12-.7.99-1.4 2.25-2.5 3.75-3.27C9.98 4.04 14 4.03 17.15 5.65c1.5.77 2.76 1.86 3.75 3.25.16.22.11.54-.12.7-.23.16-.54.11-.7-.12-.9-1.26-2.04-2.25-3.39-2.94-2.87-1.47-6.54-1.47-9.4.01-1.36.7-2.5 1.7-3.4 2.96-.08.14-.23.21-.39.21zm6.25 12.07c-.13 0-.26-.05-.35-.15-.87-.87-1.34-1.43-2.01-2.64-.69-1.23-1.05-2.73-1.05-4.34 0-2.97 2.54-5.39 5.66-5.39s5.66 2.42 5.66 5.39c0 .28-.22.5-.5.5s-.5-.22-.5-.5c0-2.42-2.09-4.39-4.66-4.39-2.57 0-4.66 1.97-4.66 4.39 0 1.44.32 2.77.93 3.85.64 1.15 1.08 1.64 1.85 2.42.19.2.19.51 0 .71-.11.1-.24.15-.37.15zm7.17-1.85c-1.19 0-2.24-.3-3.1-.89-1.49-1.01-2.38-2.65-2.38-4.39 0-.28.22-.5.5-.5s.5.22.5.5c0 1.41.72 2.74 1.94 3.56.71.48 1.54.71 2.54.71.24 0 .64-.03 1.04-.1.27-.05.53.13.58.41.05.27-.13.53-.41.58-.57.11-1.07.12-1.21.12zM14.91 22c-.04 0-.09-.01-.13-.02-1.59-.44-2.63-1.03-3.72-2.1-1.4-1.39-2.17-3.24-2.17-5.22 0-1.62 1.38-2.94 3.08-2.94 1.7 0 3.08 1.32 3.08 2.94 0 1.07.93 1.94 2.08 1.94s2.08-.87 2.08-1.94c0-3.77-3.25-6.83-7.25-6.83-2.84 0-5.44 1.58-6.61 4.03-.39.81-.59 1.76-.59 2.8 0 .78.07 2.01.67 3.61.1.26-.03.55-.29.64-.26.1-.55-.04-.64-.29-.49-1.31-.73-2.61-.73-3.96 0-1.2.23-2.29.68-3.24 1.33-2.79 4.28-4.6 7.51-4.6 4.55 0 8.25 3.51 8.25 7.83 0 1.62-1.38 2.94-3.08 2.94s-3.08-1.32-3.08-2.94c0-1.07-.93-1.94-2.08-1.94s-2.08.87-2.08 1.94c0 1.71.66 3.31 1.87 4.51.95.94 1.86 1.46 3.27 1.85.27.07.42.35.35.61-.05.23-.26.38-.47.38z"/>
        </svg>
      </div>
      <p className="biometric-text">
        {platform === 'macos' 
          ? 'Please verify your identity using Touch ID' 
          : 'Please verify your identity using your fingerprint'}
      </p>
      <button 
        onClick={handleBiometricAuth} 
        className="login-button"
        disabled={loading}
      >
        {loading 
          ? "Verifying..." 
          : platform === 'macos' ? "Use Touch ID" : "Scan Fingerprint"}
      </button>
      {error && <p className="error-message">{error}</p>}
    </div>
  );

  return (
    <div className="login-container">
      <div className="login-content">
        <div className="login-image-column">
          <img
            src="https://cdn.builder.io/api/v1/image/assets/a22ceb90578e417ca7fce76dfa9d5dc1/34e199f73a6b2c0e069b1697c3b8fd46052ddff71a9a62e0e2783f1bb23cb260?placeholderIfAbsent=true"
            alt="Login illustration"
            className="login-image"
          />
        </div>
        <div className="login-form-column">
          <div className="login-form-wrapper">
            <div className="login-header">
              <img
                src="https://cdn.builder.io/api/v1/image/assets/a22ceb90578e417ca7fce76dfa9d5dc1/190a36156f40ffdccaf66b74c972f828e1f174d8890275b3e5b712debc635378?placeholderIfAbsent=true"
                alt="Crypto logo"
                className="login-logo"
              />
              <div>EncryptoVault</div>
            </div>
            
            {!isPasswordVerified ? (
              // Step 1: Password Authentication
              <form onSubmit={handleBiometricAuth}>
                <label htmlFor="account" className="login-label">
                  Select Account
                </label>
                <select
                  id="account"
                  className="login-input"
                  value={selectedAccount}
                  onChange={(e) => setSelectedAccount(e.target.value)}
                  required
                >
                  {accounts.length > 0 && accounts.map(account => (
                      <option value={account}>{account}</option>
                  ))}
                  {accounts.length === 0 && (
                      <option value={"No accounts available!"}>No accounts available!</option>
                  )}
                </select>

                <label htmlFor="password" className="login-label">
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  className="login-input"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />

                {error && <p className="error-message">{error}</p>}

                <button 
                  type="submit" 
                  className="login-button"
                  disabled={loading}
                >
                  {loading ? "Verifying..." : "Continue"}
                </button>
              </form>
            ) : useFallbackAuth ? (
              // Desktop Password Fallback
              <form onSubmit={handleDesktopAuth}>
                <h2 className="biometric-title">Desktop Authentication</h2>
                <p className="biometric-text">
                  Please enter your desktop password to continue
                </p>
                <label htmlFor="desktopPassword" className="login-label">
                  Desktop Password
                </label>
                <input
                  type="password"
                  id="desktopPassword"
                  className="login-input"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                {error && <p className="error-message">{error}</p>}
                <button 
                  type="submit" 
                  className="login-button"
                  disabled={loading}
                >
                  {loading ? "Verifying..." : "Authenticate"}
                </button>
              </form>
            ) : (
              // Step 2: Biometric Authentication
              renderBiometricScreen()
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
