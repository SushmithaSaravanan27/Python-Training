accounts = {}
def createAccount(account_no, name, balance):
    accounts[account_no] = {"name": name, "balance": balance}
def getBalance(account_no):
    return accounts[account_no]["balance"]
