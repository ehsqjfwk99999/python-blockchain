from blockchain import Blockchain
from txnpool import TransactionPool
from wallet import Wallet


class Node:
    def __init__(self) -> None:
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()
