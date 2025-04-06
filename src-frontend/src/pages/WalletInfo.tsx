import { useLocation } from 'react-router-dom';
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from 'react';
import { QRCodeComponent } from '../components/generateQR';
import fetchPrice from '../components/fetchPrice';
import '../styles/WalletInfo.css';
import { getWalletBalance } from '../components/helpers/FakeTransactionRecords';

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

interface Transaction {
  txid: string;
  time: string;
  direction: 'in' | 'out';
  amount: string;
  status: 'confirmed' | 'pending';
}

interface TransactionOutput {
  value: string | number;
  address: string;
  public_hash?: string;
  public_key?: string;
  lock_script?: string;
  spent?: boolean;
  output_n?: number;
  script_type?: string;
  witver?: number;
  encoding?: string;
  spending_txid?: string;
  spending_index_n?: number;
  strict?: boolean;
  change?: boolean;
  witness_type?: string;
  network?: string;
}

const WalletInfo = () => {
  const location = useLocation();
  const wallet = location.state?.wallet as Wallet;
  const [showQR, setShowQR] = useState(false);
  const [showTxModal, setShowTxModal] = useState(false);
  const [selectedTx, setSelectedTx] = useState<Transaction | null>(null);
  const navigate = useNavigate();
  const {priceData} = fetchPrice(); 
  const savedTheme = localStorage.getItem('theme');

  useEffect(() => {
    if (savedTheme === 'light')
      document.body.classList.add('light-mode');
    else 
      document.body.classList.remove('light-mode');
  }, [savedTheme]);

  // Mock transaction data
  const transactions = useState<Transaction[]>([
    {
      txid: '4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b',
      time: '2023-05-15 14:22:10',
      direction: 'in',
      amount: '0.005',
      status: 'confirmed'
    },
    {
      txid: '3ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a',
      time: '2023-05-14 09:45:22',
      direction: 'out',
      amount: '0.002',
      status: 'confirmed'
    },
  ])[0]; 

  // Mock transaction details
  const txDetails = useState<{
    inputs: TransactionOutput[];
    outputs: TransactionOutput[];
  }>({
    inputs: [
      {
        value: 500000,
        address: '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
        script_type: 'p2pkh',
        spent: true
      }
    ],
    outputs: [
      {
        value: 200000,
        address: '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2',
        script_type: 'p2pkh',
        spent: false
      },
      {
        value: 300000,
        address: wallet?.address || '',
        script_type: 'p2pkh',
        change: true
      }
    ]
  })[0]; 

  useEffect(() => {
    console.log('WalletInfo received:', wallet);
  }, [wallet]);

  const handleTxClick = (tx: Transaction) => {
    setSelectedTx(tx);
    setShowTxModal(true);
  };

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
        <button className="previous-page" onClick={() => navigate(-1)}>←</button>
        <h2>{wallet.name} Details</h2>
      </div>

      <div className='wallet-details'>
        <div className="wallet-balance">
          <h3 className='big'>Balance:
            {(() => {
            const priceKey = wallet.coin_symbol === "BTC" ? "BTC-GBP" : "ETH-GBP";
            const price = priceData?.[priceKey];
            
            if (price !== undefined) {
              return `£${(wallet.balance * Number(price)).toFixed(2)}`;
            } else {
              return `£${wallet.balance.toFixed(2)}`;
            }
            })()}
          </h3>
        </div>
        <div className='wallet-coin-symbol'>
          <h4 className='smaller'>Coin Symbol: {wallet.coin_symbol}</h4>
        </div>
        <div className='wallet-holdings'>
          <h3>Holdings:</h3>
            <p className="balance-display"><p>{getWalletBalance(wallet)} {wallet?.coin_symbol}</p></p>
        </div>
        <div className="buttons">
          <button className="wallet-button" onClick={() => navigate("/buy", { state: { wallet }})}>Buy {wallet.coin_symbol}</button>
          <button className="wallet-button" onClick={() => navigate("/sell", { state: { wallet }})}>Sell {wallet.coin_symbol}</button>
          <button className="wallet-button" onClick={() => navigate("/send",{ state: { wallet }} )}>Send {wallet.coin_symbol}</button>
          <button className="wallet-button" onClick={() => setShowQR(true)}>Receive {wallet.coin_symbol}</button>
        </div>
        <div className='wallet-address'>
          <h3>Address: {wallet.address}</h3>
        </div>
      </div>

      {/* Transaction History Section */}
      <div className="transaction-history">
        <h3>Transaction History</h3>
        {transactions.length === 0 ? (
          <p className="no-transactions">No transactions yet</p>
        ) : (
          <div className="transactions-list">
            {transactions.map((tx) => (
              <div 
                key={tx.txid} 
                className={`transaction-item ${tx.direction} ${tx.status}`}
                onClick={() => handleTxClick(tx)}
              >
                <div className="tx-direction">
                  {tx.direction === 'in' ? '⬇️' : '⬆️'}
                </div>
                <div className="tx-details">
                  <div className="tx-amount">
                    {tx.direction === 'in' ? '+' : '-'}{tx.amount} {wallet.coin_symbol}
                  </div>
                  <div className="tx-time">{tx.time}</div>
                </div>
                <div className="tx-status">{tx.status}</div>
                <div className="tx-id">{tx.txid.substring(0, 12)}...</div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Transaction Details Modal */}
      {showTxModal && selectedTx && (
        <div className="tx-modal-overlay" onClick={() => setShowTxModal(false)}>
          <div className="tx-modal-content" onClick={(e) => e.stopPropagation()}>
            <button 
              className="close-button"
              onClick={() => setShowTxModal(false)}
            >
              ×
            </button>
            
            <h3>Transaction Details</h3>
            <div className="tx-summary">
              <p><strong>TXID:</strong> {selectedTx.txid}</p>
              <p><strong>Time:</strong> {selectedTx.time}</p>
              <p><strong>Amount:</strong> {selectedTx.amount} {wallet.coin_symbol}</p>
              <p><strong>Status:</strong> {selectedTx.status}</p>
              <p><strong>Direction:</strong> {selectedTx.direction === 'in' ? 'Received' : 'Sent'}</p>
            </div>

            <div className="tx-io-container">
              <div className="tx-inputs">
                <h4>Inputs</h4>
                {txDetails.inputs.map((input, index) => (
                  <div key={index} className="tx-io-item">
                    <p><strong>Value:</strong> {input.value} satoshis</p>
                    <p><strong>Address:</strong> {input.address}</p>
                    {input.script_type && <p><strong>Script Type:</strong> {input.script_type}</p>}
                    {input.spent && <p><strong>Spent:</strong> Yes</p>}
                  </div>
                ))}
              </div>

              <div className="tx-outputs">
                <h4>Outputs</h4>
                {txDetails.outputs.map((output, index) => (
                  <div key={index} className="tx-io-item">
                    <p><strong>Value:</strong> {output.value} satoshis</p>
                    <p><strong>Address:</strong> {output.address}</p>
                    {output.script_type && <p><strong>Script Type:</strong> {output.script_type}</p>}
                    {output.change && <p><strong>Change:</strong> Yes</p>}
                    {output.spent === false && <p><strong>Spent:</strong> No</p>}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default WalletInfo;