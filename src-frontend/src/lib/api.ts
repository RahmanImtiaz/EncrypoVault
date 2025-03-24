async function getAccountNames(): Promise<string[]> {
    const accounts = await fetch("/api/accounts/names")

    return (await accounts.json())
}

async function login(account_name: string, password: string, biometrics: string|null): Promise<Response> {
    return fetch("/api/auth/login", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            account_name,
            password,
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
    getOS,
    getWebauthnLoginOpts,
    getWebauthnRegOpts
}