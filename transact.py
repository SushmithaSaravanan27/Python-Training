import accounts as acc
def deposit(account_no, amount):
    acc.accounts[account_no]["balance"] += amount
def withdraw(account_no, amount):
    acc.accounts[account_no]["balance"] -= amount
