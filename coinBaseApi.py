def getApiKeys():
    import ApiKeys
    from coinbase.wallet.client import Client
    client = Client(ApiKeys.api_key, ApiKeys.api_secret)
    return client

def getBalances(client):
    wallets = client.get_accounts()["data"]
    totals = []
    totalBalance = 0
    namesOfCryptoCurrencies = []
    for nativeBalance in wallets:
        insideNativeBalance = nativeBalance["native_balance"]
        valueAmount = float(insideNativeBalance["amount"])
        totals.append(valueAmount)
        nameOfCurrency = str(insideNativeBalance["currency"])
    for balance in wallets:
        insideBalance = balance["balance"]
        nameCrypto = insideBalance["currency"]
        namesOfCryptoCurrencies.append(nameCrypto)
    for total in totals:
        totalBalance += total
    

    for i in range(0,len(totals)):
        print(namesOfCryptoCurrencies[i], "Wallet", totals[i],nameOfCurrency)
    
    print("\nYour Total Balance: ",round(totalBalance,3), nameOfCurrency)



def main():
    client = getApiKeys()
    getBalances(client)


main()

