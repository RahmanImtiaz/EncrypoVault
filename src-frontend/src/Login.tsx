import React, { useState } from "react";
import { startAuthentication } from '@simplewebauthn/browser';
import "./Login.css";

interface LoginProps {
  onLogin: () => void;
}

export function Login({ onLogin }: LoginProps) {
  const [selectedAccount, setSelectedAccount] = useState("demo_account");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [isPasswordVerified, setIsPasswordVerified] = useState(false);

  const handlePasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    // Demo account verification
    const DEMO_PASSWORD = "demo123";
    if (selectedAccount === "demo_account" && password !== DEMO_PASSWORD) {
      setError("Invalid password for demo account (use: demo123)");
      setLoading(false);
      return;
    }

    // Password verified, move to biometric step
    setIsPasswordVerified(true);
    setLoading(false);
  };

  const handleBiometricAuth = async () => {
    setLoading(true);
    setError("");

    try {
      // Check if device supports biometric auth
      const supported = await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();
      
      if (!supported) {
        throw new Error("Your device doesn't support biometric authentication");
      }

      // Create authentication challenge
      const authData = {
        challenge: Uint8Array.from("DEMO_CHALLENGE", c => c.charCodeAt(0)),
        timeout: 60000,
        rpId: window.location.hostname || "localhost",
        allowCredentials: [{
          id: Uint8Array.from("DEMO_CREDENTIAL", c => c.charCodeAt(0)),
          type: 'public-key' as const,
          transports: ['internal'] as const
        }],
        userVerification: 'required' as const
      };

      // Start biometric authentication
      await startAuthentication(authData);
      onLogin();
      
    } catch (err) {
      setError("Biometric authentication failed. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

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
              <form onSubmit={handlePasswordSubmit}>
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
                  <option value="demo_account">Demo Account</option>
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
            ) : (
              // Step 2: Biometric Authentication
              <div className="biometric-auth-container">
                <h2 className="biometric-title">Biometric Authentication</h2>
                <p className="biometric-text">
                  Please verify your identity using biometrics
                </p>
                <button 
                  onClick={handleBiometricAuth} 
                  className="login-button"
                  disabled={loading}
                >
                  {loading ? "Verifying..." : "Start Biometric Authentication"}
                </button>
                {error && <p className="error-message">{error}</p>}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
