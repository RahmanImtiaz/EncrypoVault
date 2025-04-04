import { useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { QRCodeComponent } from '../components/generateQR';
import '../styles/WalletInfo.css';

interface Holding {
  amount: number;
  name: string;
  symbol: string;
  value: number;
}

interface Wallet {
  name: string;
  balance: number;
  address: string;
  coin_symbol: string;
  holdings: {
    [key: string]: Holding;
  };
}

const WalletInfo = () => {
  const location = useLocation();
  const wallet = location.state?.wallet as Wallet;
  const [showQR, setShowQR] = useState(false);

  useEffect(() => {
    console.log('WalletInfo received:', wallet);
  }, [wallet]);

  if (!wallet) {
    return <div className="wallet-info-container">No wallet selected</div>;
  }

  if (showQR) {
    return (
      <div className="qr-modal-overlay">
        <div className="qr-modal-content">
          <div className="modal-header">
            <h2>{wallet.name}</h2>
          </div>
          <QRCodeComponent
            value={wallet.address}
            size={256}
            level="Q"
            bgColor="#FFFFFF"
            fgColor="#000000"
          />
          <p className="address-text"> Wallet Address: {wallet.address}</p>
            <button 
              className="close-button"
              onClick={() => setShowQR(false)}
            >
              ×
            </button>
        </div>
      </div>
    );
  }

  return (
    <div className='info-container'>
      <div className='wallet-name'>
        <h2>{wallet.name} Details</h2>
      </div>

      <div className='wallet-details'>
        <div className='wallet-balance'>
          <h3 className='big'>Balance: {wallet.balance} {wallet.coin_symbol}</h3>
        </div>
        <div className='wallet-address'>
          <h3>Address: {wallet.address}</h3>
        </div>
        <div className='wallet-coin-symbol'>
          <h4 className='smaller'>Coin Symbol: {wallet.coin_symbol}</h4>
        </div>
        <div className='wallet-holdings'>
          <h3>Holdings:</h3>
          {Object.keys(wallet.holdings).length > 0 ? (
            <ul className="holdings-list">
              {Object.entries(wallet.holdings).map(([key, holding]) => (
                <li key={key}>
                  {holding.name}: {holding.amount} ({holding.symbol}) - £{holding.value.toFixed(2)}
                </li>
              ))}
            </ul>
          ) : (
            <p>No holdings available</p>
          )}
        </div>

        <div className="buttons">
          <button className="wallet-button" onClick={() => setShowQR(true)}>Receive {wallet.coin_symbol}</button>
          <button className="wallet-button">Send {wallet.coin_symbol}</button>
          <button className="wallet-button">Buy {wallet.coin_symbol}</button>
          <button className="wallet-button">Sell {wallet.coin_symbol}</button>
        </div>

      </div>
    </div>
  );
};

export default WalletInfo;