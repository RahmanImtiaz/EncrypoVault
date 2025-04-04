import {useState} from 'react';
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
import { ToastProvider } from './contexts/ToastContext';

export function App() {
  const [isLogin, setIsLogin] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const toggleForm = () => {
    setIsLogin(!isLogin);
  };

  const handleLogin = () => {
    setIsAuthenticated(true);
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
              <Navbar />
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
              </Routes>
            </>
          )}
        </div>
      </Router>
    </ToastProvider>
  );
}

export default App;