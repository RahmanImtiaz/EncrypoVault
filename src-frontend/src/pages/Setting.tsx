import React, { useState, useEffect } from 'react';
import '../styles/Setting.css';
import { useToast } from '../contexts/ToastContext';

const Setting: React.FC = () => {
  const [accountType, setAccountType] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [message, setMessage] = useState<string>("");
  const [feedbackMessage, setFeedbackMessage] = useState<string>("");
  // Form states for feedback
  const [feedback, setFeedback] = useState<string>("");
  const [rating, setRating] = useState<string>("5");
  const [email, setEmail] = useState<string>("");
  const [isSubmittingFeedback, setIsSubmittingFeedback] = useState<boolean>(false);
  const { showToast } = useToast();
  
  const savedTheme = localStorage.getItem('theme');

  useEffect(() => {
    if (savedTheme === 'light')
      document.body.classList.add('light-mode');
    else 
      document.body.classList.remove('light-mode');
  }, [savedTheme]);

  
  const handleThemeToggle = () : void => {
    const currentTheme = localStorage.getItem('theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', newTheme);
  }
  
  // Fetch current account type on mount
  useEffect(() => {
    const fetchAccountInfo = async () => {
      try {
        const response = await fetch('/api/accounts/current');
        const accountData = await response.json();
        
        if (accountData && accountData.accountType) {
          setAccountType(accountData.accountType);
        }
      } catch (error) {
        console.error("Failed to fetch account info:", error);
        showToast("Failed to fetch account info", "error");
      }
    };
    
    fetchAccountInfo();
  }, [showToast]);
  
  const handleSwitchAccountType = async () => {
    try {
      setIsLoading(true);
      setMessage("");
      
      const response = await fetch('/api/accounts/current/switch-type', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      const result = await response.json();
      
      if (response.ok) {
        setAccountType(result.accountType);
        setMessage(result.message);
        showToast(`Account type switched to ${result.accountType}`, "success");
      } else {
        setMessage(result.error || "Failed to switch account type");
        showToast(result.error || "Failed to switch account type", "error");
      }
    } catch (error) {
      console.error("Error switching account type:", error);
      setMessage("An error occurred while switching account type");
      showToast("An error occurred while switching account type", "error");
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleSubmitFeedback = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmittingFeedback(true);
    
    try {
      // Google Form ID and field IDs - replace with your actual Google Form details
      const GOOGLE_FORM_ID = '1FAIpQLSfxyY2wfsM53lvaWmQVqP4NrSrUGQDHVL6rpuJ_2-3xKanvwg';
      const FEEDBACK_FIELD_ID = 'entry.1381303830';
      const RATING_FIELD_ID = 'entry.676251229';
      const EMAIL_FIELD_ID = 'entry.1708504892';
      
      // Create the form data for submission
      const formData = new URLSearchParams({
        [FEEDBACK_FIELD_ID]: feedback,
        [RATING_FIELD_ID]: rating,
        [EMAIL_FIELD_ID]: email,
      });
      
      // Submit to Google Form
      await fetch(`https://docs.google.com/forms/d/e/${GOOGLE_FORM_ID}/formResponse`, {
        method: 'POST',
        mode: 'no-cors', // This is important for CORS issues
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
      });
      
      // Since we use no-cors, we can't actually check response status
      // So we'll just assume success
      setFeedbackMessage("Thank you for your feedback!");
      showToast("Thank you for your feedback!", "success");
      setFeedback("");
      setRating("5");
      setEmail("");
      
      // Reset message after 3 seconds
      setTimeout(() => {
        setFeedbackMessage("");
      }, 3000);
    } catch (error) {
      console.error('Failed to submit feedback:', error);
      setFeedbackMessage("Error submitting feedback. Please try again.");
      showToast("Error submitting feedback. Please try again.", "error");
    } finally {
      setIsSubmittingFeedback(false);
    }
  };
  
  // Determine button text based on current account type
  const getButtonText = () => {
    if (accountType === "Beginner") {
      return "Switch to Advanced";
    } else if (accountType === "Advanced") {
      return "Switch to Beginner";
    } else {
      return "Account Type Not Available";
    }
  };

  return (
    <div className="settings-container">
      <h1 className="settings-title">Settings</h1>
      
      <div className="settings-section">
        <h2>Account Type</h2>
        <p className="current-type">Current account type: <span>{accountType}</span></p>
        
        <div className="account-type-info">
          {accountType === "Beginner" ? (
            <p>Beginner mode provides simplified crypto management with basic features. Switch to Advanced mode to access additional analytics, candlestick charts, and advanced transactions.</p>
          ) : accountType === "Advanced" ? (
            <p>Advanced mode gives you full access to all features including advanced analytics, candlestick charts, and unlimited transactions. Switch to Beginner mode for a simpler interface.</p>
          ) : (
            <p>Tester accounts are for development and testing purposes only.</p>
          )}
        </div>
        <div className='settings-buttons'>
          <button 
            className="switch-type-button"
            onClick={handleSwitchAccountType}
            disabled={isLoading || accountType === "Tester"}
          >
            {isLoading ? "Switching..." : getButtonText()}
          </button>

          <button className = "theme-toggle-button"
          onClick={handleThemeToggle}>
            Toggle {savedTheme} Mode
          </button>
        </div>
        
        {message && <p className="settings-message">{message}</p>}
      </div>
      
      {accountType === "Tester" && (
        <div className="settings-section">
          <h2>Send Feedback</h2>
          <p className="feedback-intro">We'd love to hear your thoughts on EncryptoVault!</p>
          
          {feedbackMessage ? (
        <div className="feedback-success">
          {feedbackMessage}
        </div>
          ) : (
        <form onSubmit={handleSubmitFeedback} className="feedback-form">
          <div className="form-group">
            <label htmlFor="feedback">Your Feedback</label>
            <textarea 
          id="feedback" 
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          placeholder="Share your experience using EncryptoVault..."
          required
          rows={4}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="rating">Rate your experience (1-5)</label>
            <select 
          id="rating"
          value={rating}
          onChange={(e) => setRating(e.target.value)}
            >
          <option value="5">5 - Excellent</option>
          <option value="4">4 - Good</option>
          <option value="3">3 - Average</option>
          <option value="2">2 - Below Average</option>
          <option value="1">1 - Poor</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="email">Your Email (optional)</label>
            <input 
          type="email" 
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="email@example.com"
            />
            <p className="email-note">
          We'll only use this to follow up on your feedback if needed.
            </p>
          </div>
          
          <button 
            type="submit" 
            className="submit-feedback-btn"
            disabled={isSubmittingFeedback || !feedback}
          >
            {isSubmittingFeedback ? 'Sending...' : 'Submit Feedback'}
          </button>
        </form>
          )}
        </div>
      )}
    </div>
  );
};

export default Setting;