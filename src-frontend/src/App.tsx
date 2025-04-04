import {useEffect, useState} from 'react';
import './App.css';
import Login from './Login';
import Register from './Register';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Contacts from './pages/Contacts';
import Market from './pages/Market';
import Wallets from './pages/Wallets';
import Setting from './pages/Setting';
import Portfolio from './pages/Portfolio';
import './styles/Portfolio.css';
import BuyCrypto from './pages/BuyCrypto';
import SellCrypto from './pages/SellCrypto';
import SendCrypto from './pages/SendCrypto';
import ReceiveCrypto from './pages/ReceiveCrypto';
import WalletInfo  from './pages/WalletInfo';
import { ToastProvider } from './contexts/ToastContext';

export function App() {
  const [isLogin, setIsLogin] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [lastClicked, setLastClicked] = useState<string | null>(null);

  const handleClick = () => {
    const currentTime = new Date().toISOString();
    setLastClicked(currentTime);
  }

  useEffect(() => {
    if (!isAuthenticated) return;

    const checkInActivity = setInterval(() => {
      if (lastClicked){
        const currentTime = new Date();
        const lastClick = new Date(lastClicked);

        // CHANGE THE TIME HERE !!!!!!!!!!!!!!!!!!!!!!
        if (currentTime.getTime() - lastClick.getTime() > 1000 * 60 * 10){
          handleLogout();
        }
      }
    }, 1000 * 10); // Check every 10 seconds
    
    return () => clearInterval(checkInActivity);
  }, [lastClicked, isAuthenticated]);


  useEffect(() => {
    document.addEventListener('click', handleClick);
    return () => {
      document.removeEventListener('click', handleClick);
    }
  }, []);

  const toggleForm = () => {
    setIsLogin(!isLogin);
  };

  const handleLogin = () => {
    setIsAuthenticated(true);
  };
  
  const handleLogout = async () => {
    try {
      // Call the API logout endpoint to clear backend session
      await window.api.logout();
      
      // Reset the frontend state
      setIsAuthenticated(false);
    } catch (error) {
      console.error("Error logging out:", error);
      // Even if there's an error, log the user out of the frontend
      setIsAuthenticated(false);
    }
  };

  return (
    <ToastProvider>
      <Router>
        <div className="app">
          {!isAuthenticated ? (
            isLogin ? (
              <Login onLogin={handleLogin} toggleForm={toggleForm} />
            ) : (
              <Register toggleForm={toggleForm} />
            )
          ) : (
            <>
              {/* Navbar (header) is always here once authenticated */}
              <Navbar onLogout={handleLogout} />
              {/* Routes for different pages */}
              <Routes>
                {/*Routes for navigation*/}
                <Route path="/" element={<Portfolio />} />
                <Route path="/portfolio" element={<Portfolio />} />
                <Route path="/wallets" element={<Wallets />} />
                <Route path="/contacts" element={<Contacts />} />
                <Route path="/market" element={<Market />} />
                <Route path="/settings" element={<Setting />} />

              {/* Routes for crypto transaction actions */}
              <Route path="/buy" element={<BuyCrypto />} />
              <Route path="/sell" element={<SellCrypto />} />
              <Route path="/send" element={<SendCrypto />} />
              <Route path="/receive" element={<ReceiveCrypto />} />

              {/* Route for WalletInfo */}
              <Route path="/walletInfo" element={<WalletInfo />} />

            </Routes>
          </>
        )}
      </div>
    </Router>
    </ToastProvider>
  );
}

export default App;