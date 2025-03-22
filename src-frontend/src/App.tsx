import {useEffect, useState} from 'react';
import './App.css';
import Login from './Login';
import Register from './Register';
import {WalletType} from "./index";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Contacts from './pages/Contacts';
import Market from './pages/Market';
import Wallets from './pages/Wallets';
import Setting from './pages/Setting';
import Portfolio from './pages/Portfolio';
import './styles/Portfolio.css';

export function App() {
  const [isLogin, setIsLogin] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [balance, _setBalance] = useState(1000);
  const [wallets, setWallets] = useState<WalletType[]>([]);

  useEffect(() => {
    let dummyWallets: WalletType[] = [{
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
    }]

    setWallets(dummyWallets)
  }, []);
  // useEffect(() => {
  //   const checkForAccounts = async () => {
  //     try {
  //       const accounts = await window.pywebview.api.AccountsFileManager.get_accounts();
  //       if (!accounts || accounts.length === 0) {
  //         setIsLogin(false); // Switch to registration if no accounts exist
  //       }
  //     } catch (err) {
  //       console.error('Error checking accounts:', err);
  //       setIsLogin(false); // Switch to registration on error
  //     }
  //   };
  //
  //   checkForAccounts();
  // }, []);

  const toggleForm = () => {
    setIsLogin(!isLogin);
  };

  const handleLogin = () => {
    setIsAuthenticated(true);
  };



  return (
    <Router>
    <div className="app">
      {!isAuthenticated ? (
        isLogin ? (
          <Login onLogin={handleLogin} />
        ) : (
          <Register />
        )
      ) : (
        <>
          {/* Navbar (header) is always here once authenticated */}
          <Navbar />
          {/* Routes for different pages */}
          <Routes>
            <Route
              path="/"
              element={<Portfolio balance={balance} wallets={wallets} />}
            />
            <Route path="/portfolio" element={<Portfolio balance={balance} wallets={wallets} />}/>
            <Route path="/wallets" element={<Wallets />} />
            <Route path="/contacts" element={<Contacts />} />
            <Route path="/market" element={<Market />} />
            <Route path="/settings" element={<Setting />} />
          </Routes>
        </>
      )}

      {/* Show the login/register toggle button only when the user is not authenticated */}
      {!isAuthenticated && (
        <button onClick={toggleForm} className="toggle-button">
          {isLogin ? 'Need to Register?' : 'Already have an account?'}
        </button>
      )}
    </div>
  </Router>
  );
}

export default App;