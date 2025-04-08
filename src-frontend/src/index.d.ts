type APIType = typeof import("./lib/api.ts").default

export interface Wallet {
  name: string;
  balance: number;
  address?: string;
  type: WalletType;
  transactions?: Array<{
    date: string;
    type: 'send' | 'receive' | 'trade';
    amount: number;
    status: 'completed' | 'pending' | 'failed';
  }>;
}

enum WalletType {
  BTC = "BTC"
}

interface Contact {
  name: string,
  address: string,
  crypto: string,
  description: string
}

enum AccountType {
  BEGINNER = "Beginner",
  ADVANCED = "Advanced",
  TESTER = "Tester"
}

interface Account {
  accountName: string,
  secretKey: string,
  contacts: Contact[],
  accountType: AccountType,
  encryptionKey: string
}

interface Transaction {
  timestamp: string;
  amount: number;
  hash: string;
  sender: string;
  receiver: string;
  name: string;
}

declare global {
    interface Window {
      pywebview: PyWebView,
      api: APIType;
    }
}

window.pywebview = window.pywebview || {};

window.api = API