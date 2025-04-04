import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/navbar.css';

interface NavbarProps {
  onLogout: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ onLogout }) => {
    return (
      <nav className="navbar">
        <ul className="navList">
          <li className="navItem">
            <Link to="/" className="navLink">
              <div className="navButton">
                <img src="/icons8-home-48-white.png" alt="home"/>
                <span className="navLabel">Home</span>
              </div>
            </Link>
          </li>
          <li className="navItem">
            <Link to="/wallets" className="navLink">
              <div className="navButton">
                <img src="/icons8-wallet-48-white.png" alt="wallets"/>
                <span className="navLabel">Wallets</span>
              </div>
            </Link>
          </li>
          <li className="navItem">
            <Link to="/contacts" className="navLink">
              <div className="navButton">
                <img src="/icons8-contacts-48-white.png" alt="contacts"/>
                <span className="navLabel">Contacts</span>
              </div>
            </Link>
          </li>
          <li className="navItem">
            <Link to="/market" className="navLink">
              <div className="navButton">
                <img src="/graph-white-48.png" alt="market"/>
                <span className="navLabel">Market</span>
              </div>
            </Link>
          </li>
          <li className="navItem">
            <Link to="/settings" className="navLink">
              <div className="navButton">
                <img src="/icons8-settings-48-white.png" alt="settings"/>
                <span className="navLabel">Settings</span>
              </div>
            </Link>
          </li>
          {/* Logout Button */}
          <li className="navItem">
            <button onClick={onLogout} className="navLink logoutButton">
              <div className="navButton">
                <img src="/icons8-logout-50.png" alt="logout" className="logoutIcon"/>
                <span className="navLabel">Logout</span>
              </div>
            </button>
          </li>
        </ul>
      </nav>
    );
  };

export default Navbar;