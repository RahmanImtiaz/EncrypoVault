import React, { useState } from "react";
import "./Login.css";

interface RegisterProps {
  onRegister: () => void;
}

export function Register({ onRegister }: RegisterProps) {
  const [accountName, setAccountName] = useState("");
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
      // Here you would call your backend to register the account
      // const response = await window.pywebview.api.AccountsFileManager.save_account(...)
      onRegister();
    } catch (err) {
      setError("Registration failed. Please try again.");
      console.error(err);
    }
  };

  return (
    <div className="login-container">
      <div className="login-content">
        <div className="login-image-column">
          <img
            src="https://cdn.builder.io/api/v1/image/assets/a22ceb90578e417ca7fce76dfa9d5dc1/34e199f73a6b2c0e069b1697c3b8fd46052ddff71a9a62e0e2783f1bb23cb260?placeholderIfAbsent=true"
            alt="Register illustration"
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
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Register;