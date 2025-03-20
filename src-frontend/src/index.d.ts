export interface WalletType {
  name: string;
  balance: number;
  address?: string;
  transactions?: Array<{
    date: string;
    type: 'send' | 'receive' | 'trade';
    amount: number;
    status: 'completed' | 'pending' | 'failed';
  }>;
}


interface PyWebView {
  api: {
    get_accounts(): Promise<string[]>
  }
}
declare global {
    interface Window { pywebview: PyWebView; }
}

window.pywebview = window.pywebview || {};