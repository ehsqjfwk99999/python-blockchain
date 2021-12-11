from transaction import Transaction

from typing import List


class TransactionPool:
    def __init__(self) -> None:
        self.transactions: List[Transaction] = []

    def addTransaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def transactionExists(self, transaction: Transaction) -> bool:
        for poolTransaction in self.transactions:
            if poolTransaction.equals(transaction):
                return True
        return False
