from typing import List

from transaction import Transaction


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

    def removeFromPool(self, transactions: List[Transaction]) -> None:
        newPoolTransactions = []
        for poolTransaction in self.transactions:
            insert = True
            for transaction in transactions:
                if poolTransaction.equals(transaction):
                    insert = False
            if insert:
                newPoolTransactions.append(poolTransaction)
        self.transactions = newPoolTransactions

    def forgerRequired(self):
        return len(self.transactions) >= 1
