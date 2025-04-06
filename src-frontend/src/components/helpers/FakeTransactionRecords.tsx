type TransactionType = 'buy' | 'sell';

interface TransactionRecord {
  walletName: string;
  coinSymbol: string;
  amount: number;
  type: TransactionType;
  timestamp: number;
}

export const saveTransaction = (record: Omit<TransactionRecord, 'timestamp'>) => {
  const transactions = getTransactions();
  const newRecord = {
    ...record,
    timestamp: Date.now()
  };
  localStorage.setItem('cryptoTransactions', JSON.stringify([...transactions, newRecord]));
};

export const getTransactions = (): TransactionRecord[] => {
  const data = localStorage.getItem('cryptoTransactions');
  return data ? JSON.parse(data) : [];
};

export const getWalletBalance = (wallet: { name: string; coin_symbol: string; balance: number }): number => {
  const transactions = getTransactions();
  const walletTransactions = transactions.filter(
    t => t.walletName === wallet.name && t.coinSymbol === wallet.coin_symbol
  );
  
  const netAmount = walletTransactions.reduce((sum, t) => {
    return t.type === 'buy' ? sum + t.amount : sum - t.amount;
  }, 0);

  return wallet.balance + netAmount;
};