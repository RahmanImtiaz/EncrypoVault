import {AccountType} from "../index";
import {io, Socket} from "socket.io-client"

async function getAccountNames(): Promise<string[]> {
    const accounts = await fetch("/api/accounts/names")

    return (await accounts.json())
}

async function login(accountName: string, password: string, biometrics: string|null): Promise<Response> {
    return fetch("/api/auth/login", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            account_name: accountName,
            password,
            biometrics
        })
    })
}

async function register(accountName: string, password: string, accountType: AccountType, biometrics: string): Promise<Response> {
    return fetch("/api/auth/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            account_name: accountName,
            password,
            account_type: accountType,
            biometrics
        })
    })
}

async function getOS() : Promise<string> {
    const res = await fetch("/api/utils/os")
    return (await res.json()).os
}

async function getWebauthnLoginOpts(): Promise<JSON> {
    return await (await fetch("/api/auth/webauthn_auth")).json()
}

async function getWebauthnRegOpts(accountName: string): Promise<JSON> {
    return await (await fetch(`/api/auth/webauthn_reg/${accountName}`)).json()
}

async function getPortfolioBalance() {
    try {
        const response = await fetch("/api/portfolio/balance");
        const data = await response.json();
        
        // Handle different possible response formats
        if (data.balance !== undefined) {
            return data.balance; // If response has {balance: value}
        } else if (typeof data === 'number') {
            return data; // If response is just a number
        } else {
            console.error('Unexpected balance format:', data);
            return 0;
        }
    } catch (error) {
        console.error('Error fetching portfolio balance:', error);
        return 0;
    }
}

let cryptoSocket: Socket|null = null
async function getCryptoSocket() {
    if(!cryptoSocket) {
        try {
            return await new Promise((res, rej) => {
                const connAttempt = io("http://localhost:9209/api/crypto/ws")
                connAttempt.once("connect", () => {cryptoSocket = connAttempt; res(cryptoSocket)})
                connAttempt.once("error", (e: Error) => rej(e) )
                connAttempt.on("server_error", (e) => console.log(e))
            })
        } catch (e) {
            console.error("Failed to connect to crypto socket!")
            console.error(e)
        }
    }
    return cryptoSocket
    //return io("http://localhost:9209/api/crypto/ws")
}


async function createWallet(walletName: string): Promise<Response> {
    return fetch("/api/crypto/wallets", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            walletName: walletName,
            walletType: "BTC"
        })
    });
}

async function getWallets() {
    try {
      const response = await fetch("/api/crypto/wallets/details");
      const data = await response.json();
      
      return (data.data || []).map((wallet: any) => ({
          name: wallet.name,
          address: wallet.address || "",
          balance: wallet.balance || 0,
          coin_symbol: wallet.type || 'BTC',
          holdings: wallet.holdings || {}
      }));
    } catch (error) {
      console.error('Error fetching wallets:', error);
      return [];
    }
}

async function sendCrypto(walletName: string, amount: number, destinationAddress: string) {
    try {
        await fetch("/api/crypto/wallets/send_crypto", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                walletName,
                amount,
                destinationAddress
            })
        })
    } catch (e) {
        console.error(`Error trying to send crypto: ${e}`)
    }
}

async function addContact(name: string, address: string): Promise<Response> {
    return fetch("/api/contacts/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name,
            address
        })
    });
}

async function getContacts(): Promise<{name: string, address: string}[]> {
    const response = await fetch("/api/contacts/list");
    const data = await response.json();
    return data.contacts || [];
}

export default {
    getAccountNames,
    login,
    register,
    getOS,
    getWebauthnLoginOpts,
    getWebauthnRegOpts,
    getPortfolioBalance,
    getCryptoSocket,
    addContact,
    getContacts,
    createWallet,
    getWallets,
    sendCrypto
}