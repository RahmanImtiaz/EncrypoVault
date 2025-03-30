import '../styles/ReceiveCrypto.css';
//import { useState } from 'react';
import { useNavigate } from "react-router-dom";

const ReceiveCrypto = () => {
  const navigate = useNavigate();
  //const[scanned, setScanned]=useState(false);
  

  return (
    <div className="receive-container">
      <label htmlFor="" className="main-label">Receive Crypto</label>
      <div className="qr-scan-box">
        <p>Replace this with QR code scanning implementation when done</p>
      </div>
      {/*<p className="scan-message">{scanned?"success" : "Awaiting QR code"}</p>*/}
      <p className="scan-message">Awaiting QR code</p>
      <button type="button" className="receive-goBack" onClick={() => navigate(-1)}>Cancel</button>
    </div>
  );
};

export default ReceiveCrypto;