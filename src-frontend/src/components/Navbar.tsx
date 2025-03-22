import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/navbar.css';

const Navbar: React.FC = () => {
    return (
      <nav className="navbar">
        <ul className="navList">
          <li className="navItem">
            <Link to="/" className="navLink">
              <div className="navButton">
                <img src="/icons8-home-48-white.png" alt="home"/>
              </div>
            </Link>
          </li>
          <li className="navItem">
            <Link to="/wallets" className="navLink">
              <div className="navButton">
                <img src="/icons8-wallet-48-white.png" alt="wallets"/>
              </div>
            </Link>
          </li>
          <li className="navItem">
            <Link to="/contacts" className="navLink">
              <div className="navButton">
                <img src="/icons8-contacts-48-white.png" alt="contacts"/>
              </div>
            </Link>
          </li>
          <li className="navItem">
            <Link to="/market" className="navLink">
              <div className="navButton">
                <img src="/graph-white-48.png" alt="market"/>
              </div>
            </Link>
          </li>
          <li className="navItem">
            <Link to="/settings" className="navLink">
              <div className="navButton">
                <img src="/icons8-settings-48-white.png" alt="settings"/>
              </div>
            </Link>
          </li>
        </ul>
      </nav>
    );
  };


export default Navbar;