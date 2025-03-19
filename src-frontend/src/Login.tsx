import React, { useState } from "react";
import { startAuthentication } from '@simplewebauthn/browser';
import "./Login.css";

interface LoginProps {
  onLogin: () => void;
}

export function Login({ onLogin }: LoginProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState("");
  const [isPasswordVerified, setIsPasswordVerified] = useState(false);

  const validateEmail = (email: string) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
  };

  const handlePasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateEmail(email)) {
      setError("Invalid email format");
      return;
    }
    
    // Verify password first
    try {
      // Here you would typically verify the password with your backend
      // For demo purposes, we're just setting it to true
      setIsPasswordVerified(true);
      setError("");
    } catch (err) {
      setError("Password verification failed");
    }
  };

  const handleBiometricAuth = async () => {
    try {
      // For demonstration purposes, we'll simulate a successful authentication
      // In a real application, this would communicate with your backend
      const isSupported = await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();
      
      if (!isSupported) {
        setError("Your device doesn't support biometric authentication");
        return;
      }

      // Simulate authentication delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Simulate successful authentication
      onLogin();
      
    } catch (err) {
      setError("Biometric authentication failed. Please try again.");
      console.error(err);
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
              <form onSubmit={handlePasswordSubmit}>
                <label htmlFor="email" className="login-label">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  className="login-input"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  aria-label="Email input"
                />

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

                <div className="login-options">
                  <div className="login-remember">
                    <input
                      type="checkbox"
                      id="remember"
                      className="login-checkbox"
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                      aria-label="Remember me checkbox"
                    />
                    <label htmlFor="remember">Save Email and Password</label>
                  </div>
                  <div>
                    <span className="login-signup">Don't have an account?</span>
                  </div>
                </div>

                {error && <p className="error-message">{error}</p>}

                <button type="submit" className="login-button">
                  Continue
                </button>
              </form>
            ) : (
              <div className="biometric-auth-container">
                <h2 className="biometric-title">Biometric Authentication</h2>
                <p className="biometric-text">
                  Please verify your identity using biometrics
                </p>
                <button onClick={handleBiometricAuth} className="login-button">
                  Start Biometric Authentication
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
