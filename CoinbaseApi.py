def get_api_keys():
    import ApiKeys
    from coinbase.wallet.client import Client
    client = Client(ApiKeys.api_key, ApiKeys.api_secret)
    return client


def get_wallets_api(client):
    wallets = client.get_accounts()["data"]
    return wallets


def get_preferred_currency(wallets):
    for nativeBalance in wallets:
        insideNativeBalance = nativeBalance["native_balance"]
        nameOfCurrency = str(insideNativeBalance["currency"])
        return nameOfCurrency


def get_total_balance(wallets):
    totals = []
    totalBalance = 0
    for nativeBalance in wallets:
        insideNativeBalance = nativeBalance["native_balance"]
        valueAmount = float(insideNativeBalance["amount"])
        totals.append(valueAmount)
    for total in totals:
        totalBalance += total
    return totalBalance


def get_balances(wallets,x):
    totals = []
    namesOfCryptoCurrencies = []
    for nativeBalance in wallets:
        insideNativeBalance = nativeBalance["native_balance"]
        valueAmount = float(insideNativeBalance["amount"])
        totals.append(valueAmount)
    for balance in wallets:
        insideBalance = balance["balance"]
        nameCrypto = insideBalance["currency"]
        namesOfCryptoCurrencies.append(nameCrypto)
    
    print(namesOfCryptoCurrencies[x], "Wallet", totals[x],get_preferred_currency(wallets))
    

def get_number_of_wallets(wallets):
    idsWallets = []
    for id in wallets:
        walletId = id["id"]
        idsWallets.append(walletId)
    return len(idsWallets)
    
def get_transaction_value(client,wallets,x,y):
    idsWallets = []
    paymentValues = []
    for id in wallets:
        walletId = id["id"]
        idsWallets.append(walletId)
    
    transactions = client.get_transactions(idsWallets[x])["data"]
    for transaction in transactions:
        insideNativeAmount = transaction["native_amount"]
        paymentValue = float(insideNativeAmount["amount"])
        #fees counting 
        if paymentValue < 10.99:
            paymentValue-=0.99
        elif 11 > paymentValue < 25.99:
            paymentValue-=1.49
        elif 26 > paymentValue < 51.99:
            paymentValue-=1.99
        elif 52 > paymentValue < 77.99:
            paymentValue-=2.99
        else:
            fee = float((paymentValue*3.84)/100)
            paymentValue -= fee
        paymentValues.append(round(paymentValue,2))
    return paymentValues[y]


def get_number_of_transaction(client,wallets,x):
    idsWallets = []
    namesOfCryptoCurrencies = []
    for id in wallets:
        walletId = id["id"]
        idsWallets.append(walletId)
        
    transactions = client.get_transactions(idsWallets[x])["data"]
    for transaction in transactions:
        insideAmount = transaction["amount"]
        cryptoName = insideAmount["currency"]
        namesOfCryptoCurrencies.append(cryptoName)
    
    return namesOfCryptoCurrencies


def get_name_from_transaction(client,wallets,x,y):
    Lista = get_number_of_transaction(client,wallets,x)
    return Lista[y]


def get_sum_of_transaction(client,wallets):
    suma = 0

    try:
        for i in range (0,get_number_of_wallets(get_wallets_api(client))):
            for x in range(0,len(get_number_of_transaction(client,wallets,i))):
                suma += get_transaction_value(client,wallets,i,x)
    except:
        print()
    return round(suma,3)


def compare_balance_to_sum_of_transaction(client,wallets):
    LossPercentage = ((get_total_balance(wallets)/get_sum_of_transaction(client,wallets))*100)-100
    ProfitPercentage = ((get_total_balance(wallets)/get_sum_of_transaction(client,wallets))*100)-100
    
    if get_total_balance(wallets)>=get_sum_of_transaction(client,wallets):
        print("Your profit is: ",round(get_total_balance(wallets)-get_sum_of_transaction(client,wallets),2),get_preferred_currency(wallets),"   (",round(ProfitPercentage,2),"% )")
    else:
        print("Your loss is: ",round(get_sum_of_transaction(client,wallets)-get_total_balance(wallets),2),get_preferred_currency(wallets),"   (",round(LossPercentage,2),"% )")

def display(client,wallets):
    q = " "
    
    try:
        for i in range (0,get_number_of_wallets(get_wallets_api(client))):
            get_balances(wallets,i)
            for x in range(0,len(get_number_of_transaction(client,wallets,i))):
                print(8*q,"(Transaction #",x+1,") Bought", get_name_from_transaction(client,wallets,i,x) ,"for:",get_transaction_value(client,wallets,i,x),get_preferred_currency(wallets))
    except:
        print(8*q,"Downloaded data failed")

    print("\n")
    print("Your Total Balance: ",round(get_total_balance(wallets),3), get_preferred_currency(wallets))
    print("Your Total Transactions Value:  ",round(get_sum_of_transaction(client,wallets),3),get_preferred_currency(wallets))
    compare_balance_to_sum_of_transaction(client,wallets)


def main():
    client = get_api_keys()
    display(client,get_wallets_api(client))
    
main()

