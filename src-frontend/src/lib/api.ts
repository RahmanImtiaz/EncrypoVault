async function getAccountNames(): Promise<string[]> {
    const accounts = await fetch("/api/accounts/names")

    return (await accounts.json())
}

export default {
    getAccountNames
}