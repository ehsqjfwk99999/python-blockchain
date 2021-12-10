from txnpool import TransactionPool
from wallet import Wallet
from block import Block
import pprint

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

    block = wallet.createBlock(pool.transactions, "lastHash", 1)

    signatureValid = wallet.signatureValid(
        block.payload(), block.signature, f_wallet.publicKeyString()
    )
    print(signatureValid)
