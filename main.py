from txnpool import TransactionPool
from wallet import Wallet

if __name__ == "__main__":

    sender = "sender"
    receiver = "receiver"
    amount = 1
    transType = "TRANSFER"

    wallet = Wallet()
    f_wallet = Wallet()
    pool = TransactionPool()

    transaction = wallet.createTransaction(receiver, amount, transType)

    if not pool.transactionExists(transaction):
        pool.addTransaction(transaction)
    if not pool.transactionExists(transaction):
        pool.addTransaction(transaction)

    print(pool.transactions)