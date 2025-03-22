// Portfolio.tsx
import React from 'react';
import '../styles/Wallets.css';

const Wallets: React.FC = () => {
  return (
    <div className="walletContainter">
      <div className="walletHeading">
        <h1>Wallet</h1>
        <button>+ new</button>
      </div>
      <div className="walletList">
          <div>Wallet1</div>
          <div>Wallet2</div>
          <div>Wallet3</div>
      </div>
    </div>
  );
};

export default Wallets;