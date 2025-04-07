import React, { useState, useEffect } from "react";
import { PublicKeyCredentialRequestOptionsJSON, startAuthentication } from '@simplewebauthn/browser';
import "./Login.css";
import { useToast } from './contexts/ToastContext';

interface LoginProps {
  onLogin: () => void;
  toggleForm: () => void;
}

export function Login({ onLogin, toggleForm }: LoginProps) {
  const [selectedAccount, setSelectedAccount] = useState("demo_account");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [accounts, setAccounts] = useState<string[]>([]);
  const [failedAttempts, setFailedAttempts] = useState(0); 
  const [isButtonDisabled, setIsButtonDisabled] = useState(false);
  console.log(failedAttempts);
  if (!localStorage.getItem("theme")) {
    localStorage.setItem("theme", "dark");
  }
  const { showToast } = useToast();

  // Check biometric support when component mounts
  useEffect(() => {
    const checkBiometricSupport = async () => {
      try {
        const supported = await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();
        console.log('Biometric support:', supported);
      } catch (err) {
        console.error('Error checking biometric support:', err);
      }
    };

    function fetchAccounts() {
      window.api.getAccountNames()
          .then(fetchedAccounts => {
            console.log("Accounts fetched:", fetchedAccounts);
            setAccounts(fetchedAccounts);
            if (fetchedAccounts && fetchedAccounts.length > 0) {
              setSelectedAccount(fetchedAccounts[0]);
            }
          })
          .catch(err => {
            console.error("Error fetching accounts:", err);
          });
    }

    checkBiometricSupport();
    fetchAccounts();
  }, []);

  const handleBiometricAuth = async (e: React.FormEvent) => {
    e.preventDefault()

    if (isButtonDisabled) return;

    setLoading(true);
    const platform = await window.api.getOS()
    try {
      if (platform === 'darwin') {
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            account_name: selectedAccount,
            password: password
          }),
        });
        
        const data = await response.json();
        
        if (!response.ok) {
          if (data.error === 'TOUCHID_UNAVAILABLE') {
            showToast("Touch ID is unavailable. Please use your password to log in.", 'error');
          } else {
            throw new Error(data.error || 'Authentication failed');
          }
        } else {
          showToast('Login successful!', 'success');
          onLogin();
        }
      } else {
        const authData: PublicKeyCredentialRequestOptionsJSON = await window.api.getWebauthnLoginOpts() as unknown as PublicKeyCredentialRequestOptionsJSON
        const webauthnResponse = await startAuthentication({optionsJSON: authData, useBrowserAutofill: false})
        const res = await window.api.login(selectedAccount, password, webauthnResponse.response.authenticatorData)

        if(res.status === 200) {
          showToast('Login successful!', 'success');
          onLogin();
        } else {
          setLoading(false)
          showToast('Invalid Password or biometrics!', 'error');
        }
      }
    } catch (err) {
      console.error('Biometric auth error:', err);
      setFailedAttempts(prev => {
        const attempts = prev +1
        if (attempts >=3){
          setIsButtonDisabled(true)
          showToast('Too many failed attempts! Please try again in 5 minutes.', 'error');

            setTimeout(() => {
            setIsButtonDisabled(false);
            setFailedAttempts(0);
            showToast('You can try again!');
            }, 300000); // 5 minutes
        }
        return attempts
      });

      showToast('You closed the OS login prompt! or Incorrect Login Error', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-content">
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
                    <option key={account} value={account}>{account}</option>
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

              <button 
                type="submit" 
                className="login-button"
                disabled={loading || isButtonDisabled}
              >
                {loading ? "Verifying..." : "Continue"}
              </button>
              <button 
                type="button"
                onClick={toggleForm} 
                className="toggle-button"
                disabled={loading || isButtonDisabled}
              >
                Need to Register?
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
