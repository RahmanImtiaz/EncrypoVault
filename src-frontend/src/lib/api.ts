async function getAccountNames(): Promise<string[]> {
    let accounts = await fetch("/api/get_accounts")

    return (await accounts.json())
}

export default {
    getAccountNames
}