import React, { useState } from 'react';
import './Login.css';
import { AccountType } from './index';
import { startRegistration } from '@simplewebauthn/browser';
import { PublicKeyCredentialCreationOptionsJSON } from '@simplewebauthn/typescript-types';
import { useToast } from './contexts/ToastContext';

interface RegisterProps {
  toggleForm: () => void;
}

export function Register({ toggleForm }: RegisterProps) {
  const [accountName, setAccountName] = useState("");
  const [accountType, setAccountType] = useState<AccountType>("Beginner" as AccountType);
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const { showToast } = useToast();
  const [showRecoveryPhrase, setShowRecoveryPhrase] = useState(false);
  const [recoveryPhrase, setRecoveryPhrase] = useState("");
  const [recoveryPhraseError, setRecoveryPhraseError] = useState("");

  const handleRecoveryPhraseChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    setRecoveryPhrase(value);
    
    const words = value.trim().split(/\s+/);
    if (words.length !== 12) {
      setRecoveryPhraseError("Recovery phrase must contain exactly 12 words");
    } else {
      setRecoveryPhraseError("");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!accountName.trim()) {
      setError("Account name is required");
      showToast("Account name is required", "error");
      return;
    }
    
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      showToast("Passwords do not match", "error");
      return;
    }

    if (showRecoveryPhrase) {
      const words = recoveryPhrase.trim().split(/\s+/);
      if (words.length !== 12) {
        setError("Recovery phrase must contain exactly 12 words");
        showToast("Recovery phrase must contain exactly 12 words", "error");
        return;
      }
    }

    try {
      // Check if the account already exists
      const accounts = await window.api.getAccountNames();
      if (accounts.includes(accountName)) {
          setError("Account already exists. Please choose a different account name.");
          showToast("Account already exists. Please choose a different account name.", "error");
          return;
      }

      // Get the platform
      const platform = await window.api.getOS();
      console.log("Platform detected:", platform);

      if (platform === "darwin") {
        // For macOS: Use Touch ID for registration
        console.log("Using Touch ID for macOS registration");
        
        // Make a registration request that will trigger Touch ID on the backend
        const response = await fetch('/api/auth/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            account_name: accountName,
            password: password,
            account_type: accountType,
            use_touch_id: true  // Signal to use Touch ID instead of WebAuthn
          }),
        });
        
        const data = await response.json();
        
        if (!response.ok) {
          throw new Error(data.error || 'Registration failed');
        }
        
        console.log("Account created successfully with Touch ID");
        showToast("Account created successfully with Touch ID", "success");
        
        // Redirect to login page after 2 seconds
        setTimeout(() => {
          toggleForm();
        }, 2000);
      } else {
        // For Windows and other platforms: Use WebAuthn
        console.log("Using WebAuthn for registration");
        const authData = await window.api.getWebauthnRegOpts(accountName) as unknown as PublicKeyCredentialCreationOptionsJSON;
        const biometrics = await startRegistration({optionsJSON: authData});
        console.log(biometrics);
        
        // Register the account with WebAuthn data
        const response = await window.api.register(
          accountName, 
          password, 
          accountType, 
          biometrics.response.clientDataJSON
        );
        
        console.log(response);
        console.log("Account created successfully with WebAuthn");
        showToast("Account created successfully with WebAuthn", "success");
        
        // Redirect to login page after 2 seconds
        setTimeout(() => {
          toggleForm();
        }, 2000);
      }
    } catch (err) {
      setError("Registration failed. Please try again.");
      showToast("Registration failed. Please try again.", "error");
      console.error(err);
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
            <form onSubmit={handleSubmit}>
                {showRecoveryPhrase && (
                  <div className="recovery-phrase-section">
                    <label htmlFor="recoveryPhrase" className="login-label">
                      Recovery Phrase (12 words)
                    </label>
                    <textarea
                      id="recoveryPhrase"
                      className="login-input recovery-phrase-input"
                      value={recoveryPhrase}
                      onChange={handleRecoveryPhraseChange}
                      required={showRecoveryPhrase} 
                      rows={3}
                    />
                    {recoveryPhraseError && (
                      <p className="error-message">{recoveryPhraseError}</p>
                    )}
                  </div>
                )}
              
              <label htmlFor="accountName" className="login-label">
                Account Name
              </label>
              <input
                type="text"
                id="accountName"
                className="login-input"
                value={accountName}
                onChange={(e) => setAccountName(e.target.value)}
                required
                aria-label="Account name input"
              />

                <label htmlFor="accountType" className="login-label">
                  Select Account Type
                </label>
                <select
                  id="accountType"
                  className="login-input"
                  value={accountType}
                  onChange={(e) => setAccountType(e.target.value as AccountType)}
                  required
                >
                  <option value="Beginner">Beginner</option>
                  <option value="Advanced">Advanced</option>
                  <option value="Tester">Tester</option>
                </select>

              <label
                htmlFor="password"
                className="login-label login-password-label"
              >
                Password
              </label>
              <input
                type="password"
                id="password"
                className="login-input login-password-input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                aria-label="Password input"
              />

              <label
                htmlFor="confirmPassword"
                className="login-label login-password-label"
              >
                Confirm Password
              </label>
              <input
                type="password"
                id="confirmPassword"
                className="login-input login-password-input"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                aria-label="Confirm Password input"
              />

              <div className="import-toggle">
                <label className="switch">
                  <input 
                    type="checkbox" 
                    checked={showRecoveryPhrase}
                    onChange={(e) => setShowRecoveryPhrase(e.target.checked)}
                  />
                  <span className="slider round"></span>
                </label>
                <span className="toggle-label">Import existing account</span>
              </div>

              {/* Only show error messages for validation errors, not success */}
              {error && !error.includes("success") && <p className="error-message">{error}</p>}

              <button type="submit" className="login-button">
                Register
              </button>
              <button 
                type="button"
                onClick={toggleForm} 
                className="toggle-button"
              >
                Already have an account?
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Register;