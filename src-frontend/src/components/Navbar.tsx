import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/navbar.css';

const Navbar: React.FC = () => {
    return (
      <nav className="navbar">
        <ul className="navList">
          <li className="navItem">
            <Link to="/" className="navLink">
              Portfolio
            </Link>
          </li>
          <li className="navItem">
            <Link to="/wallets" className="navLink">
              Wallets
            </Link>
          </li>
          <li className="navItem">
            <Link to="/contacts" className="navLink">
              Contacts
            </Link>
          </li>
          <li className="navItem">
            <Link to="/market" className="navLink">
              Market
            </Link>
          </li>
          <li className="navItem">
            <Link to="/settings" className="navLink">
              Settings
            </Link>
          </li>
        </ul>
      </nav>
    );
  };


export default Navbar;