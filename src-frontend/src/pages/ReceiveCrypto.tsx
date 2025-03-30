import '../styles/ReceiveCrypto.css';

import { useNavigate } from "react-router-dom";

const ReceiveCrypto = () => {
  const navigate = useNavigate();

  return (
    <div>
      <h1>Receive Crypto</h1>
      <button onClick={() => navigate(-1)}>Back</button>
    </div>
  );
};

export default ReceiveCrypto;