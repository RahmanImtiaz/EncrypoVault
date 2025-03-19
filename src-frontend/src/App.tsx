import React, { useState } from 'react';
import './App.css';
import Login from './Login';
import Register from './Register';
import Portfolio from './Portfolio';
import './Portfolio.css';

function App() {
  const [isLogin, setIsLogin] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [balance, setBalance] = useState(1000);
  const [wallets, setWallets] = useState([
    {
      name: 'Bitcoin',
      balance: 0.5,
      address: '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
      transactions: [
        {
          date: '2024-01-15',
          type: 'receive',
          amount: 0.1,
          status: 'completed'
        },
        {
          date: '2024-01-14',
          type: 'send',
          amount: 0.05,
          status: 'completed'
        }
      ]
    },
    {
      name: 'Ethereum',
      balance: 2,
      address: '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
      transactions: [
        {
          date: '2024-01-16',
          type: 'trade',
          amount: 0.5,
          status: 'pending'
        }
      ]
    },
    {
      name: 'Solana',
      balance: 15,
      address: 'DRpbCBMxVnDpQpC9b3HGDp3wNe3zXabDrhvB2BCqBsRF',
      transactions: []
    }
  ]);

  const toggleForm = () => {
    setIsLogin(!isLogin);
  };

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleRegister = () => {
    setIsLogin(true);
  };

  return (
    <div className="App">
      {!isAuthenticated ? (
        isLogin ? (
          <Login onLogin={handleLogin} />
        ) : (
          <Register onRegister={handleRegister} />
        )
      ) : (
        <Portfolio balance={balance} wallets={wallets} />
      )}
      {!isAuthenticated && (
        <button onClick={toggleForm} className="toggle-button">
          {isLogin ? "Don't have an account? Register" : "Already have an account? Login"}
        </button>
      )}
    </div>
  );
}

export default App;