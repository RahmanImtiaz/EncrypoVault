import {AccountType} from "../index";

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



export default {
    getAccountNames,
    login,
    register,
    getOS,
    getWebauthnLoginOpts,
    getWebauthnRegOpts
}