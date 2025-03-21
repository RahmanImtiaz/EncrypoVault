import {  PublicKeyCredentialRequestOptionsJSON } from "@simplewebauthn/browser";

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

interface Contact {
  name: string,
  address: string,
  crypto: string,
  description: string
}

enum AccountType {
  BEGINNER,
  ADVANCED,
  TESTER
}

interface Account {
  accountName: string,
  secretKey: string,
  contacts: Contact[],
  accountType: AccountType,
  encryptionKey: string
}
/*
data = {
            "accountName": self._accountName,
            "secretKey": self._secretKey,
            "contacts": self._contacts,
            "accountType": self._accountType.get_type_name(),
            "encryptionKey": encryption_key_str
        }
 */
interface PyWebView {
  api: {
    get_accounts(): Promise<string[]>
    get_loaded_account(): Account,
    create_account(account_name: string, account_password: string, account_type: string): Promise<string>
    authenticate_account(account_name: string, password: string, biometrics: Blob): Promise<Account>
    create_bitcoin_wallet(wallet_name: string): WalletType
    create_webauthn_auth_options():  Promise<string>
    create_webauthn_reg_options(): Promise<string>
    authenticate_account(account_name, password, biometrics): Promise<Account | null>
  }
}
declare global {
    interface Window { pywebview: PyWebView; }
}

window.pywebview = window.pywebview || {};