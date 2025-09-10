import accounts 
import transactions
accounts.createAccount(101,"amal",1000)
transactions.deposit(101,500)
transactions.withdraw(101,200)
print("balance:",accounts.getBalance(101))
