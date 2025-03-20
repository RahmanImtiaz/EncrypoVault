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
    create_account(account_name: string, account_password: string, account_type: string): Promise<string>
    authenticate_account(account_name: string, password: string): Promise<any>
  }
}
declare global {
    interface Window { pywebview: PyWebView; }
}

window.pywebview = window.pywebview || {};