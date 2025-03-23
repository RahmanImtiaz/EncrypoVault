// Portfolio.tsx
import React from 'react';
import '../styles/Market.css';
import BasicDetails from '../components/BasicDetails';

const Market: React.FC = () => {
  return (
    <div>
      <h1>Market Page</h1>
      <BasicDetails cryptoId='bitcoin'/>
    </div>
  );
};

export default Market;