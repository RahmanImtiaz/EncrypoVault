import React, {useState} from "react";
import "./Login.css";
import {PublicKeyCredentialCreationOptionsJSON, startRegistration} from "@simplewebauthn/browser";
import type { AccountType } from "./index";

interface RegisterProps {
  toggleForm: () => void; // Add toggleForm prop
}

export function Register({ toggleForm }: RegisterProps) {
  const [accountName, setAccountName] = useState("");
  const [accountType, setAccountType] = useState<AccountType>("Beginner" as AccountType);
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!accountName.trim()) {
      setError("Account name is required");
      return;
    }
    
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      // Check if the account already exists
      const accounts = await window.api.getAccountNames();
      if (accounts.includes(accountName)) {
          setError("Account already exists. Please choose a different account name.");
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
        setError("Account created successfully");
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
        setError("Account created successfully");
      }
      // onRegister(); // Uncomment if you want to automatically log in after registration
    } catch (err) {
      setError("Registration failed. Please try again.");
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

              {error && <p className="error-message">{error}</p>}

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