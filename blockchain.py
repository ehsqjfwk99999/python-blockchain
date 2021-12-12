from typing import Any, List

from account_model import AccountModel
from block import Block
from blockchain_utils import BlockchainUtils
from transaction import Transaction


class Blockchain:
    def __init__(self) -> None:
        self.blocks: List[Block] = [Block.genesis()]
        self.accountModel: AccountModel = AccountModel()

    def addBlock(self, block: Block) -> None:
        self.executeTransactions(block.transactions)
        self.blocks.append(block)

    def toJson(self) -> Any:
        data = {}
        jsonBlocks = []
        for block in self.blocks:
            jsonBlocks.append(block.toJson())
        data["blocks"] = jsonBlocks
        return data

    def blockCountValid(self, block: Block) -> bool:
        if self.blocks[-1].blockCount == block.blockCount - 1:
            return True
        else:
            return False

    def lastBlockHashValid(self, block: Block) -> bool:
        latestBlockHash: str = BlockchainUtils.hash(
            self.blocks[-1].payload()
        ).hexdigest()
        if latestBlockHash == block.lastHash:
            return True
        else:
            return False

    def transactionCovered(self, transaction: Transaction) -> bool:
        if transaction.type == "EXCHANGE":
            return True
        senderBalance: int = self.accountModel.getBalance(transaction.senderPublicKey)
        if senderBalance >= transaction.amount:
            return True
        else:
            return False

    def getCoveredTransactionSet(
        self, transactions: List[Transaction]
    ) -> List[Transaction]:
        coveredTransactions: List[Transaction] = []
        for transaction in transactions:
            if self.transactionCovered(transaction):
                coveredTransactions.append(transaction)
            else:
                print("Transaction is not covered by sender")
        return coveredTransactions

    def executeTransaction(self, transaction: Transaction) -> None:
        sender: str = transaction.senderPublicKey
        receiver: str = transaction.receiverPublicKey
        amount: int = transaction.amount
        self.accountModel.updateBalance(sender, -amount)
        self.accountModel.updateBalance(receiver, amount)

    def executeTransactions(self, transactions: List[Transaction]) -> None:
        for transaction in transactions:
            self.executeTransaction(transaction)
