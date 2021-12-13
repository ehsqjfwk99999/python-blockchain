from typing import Any, List

from account_model import AccountModel
from block import Block
from blockchain_utils import BlockchainUtils
from proof_of_stake import ProofOfStake
from transaction import Transaction
from wallet import Wallet


class Blockchain:
    def __init__(self) -> None:
        self.blocks: List[Block] = [Block.genesis()]
        self.accountModel: AccountModel = AccountModel()
        self.pos = ProofOfStake()

    def addBlock(self, block: Block) -> None:
        self.executeTransactions(block.transactions)
        if self.blocks[-1].blockCount < block.blockCount:
            self.blocks.append(block)
        # self.blocks.append(block)

    def toJson(self) -> Any:
        data = {}
        jsonBlocks = []
        for block in self.blocks:
            jsonBlocks.append(block.toJson())
        data["blocks"] = jsonBlocks
        return data

    def blockCountValid(self, block: Block) -> bool:
        if self.blocks[-1].blockCount >= block.blockCount - 1:
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
        if transaction.type == "STAKE":
            sender: str = transaction.senderPublicKey
            receiver: str = transaction.receiverPublicKey
            if sender == receiver:
                amount: int = transaction.amount
                self.pos.update(sender, amount)
                self.accountModel.updateBalance(sender, -amount)
        else:
            sender: str = transaction.senderPublicKey
            receiver: str = transaction.receiverPublicKey
            amount: int = transaction.amount
            self.accountModel.updateBalance(sender, -amount)
            self.accountModel.updateBalance(receiver, amount)

    def executeTransactions(self, transactions: List[Transaction]) -> None:
        for transaction in transactions:
            self.executeTransaction(transaction)

    def nextForger(self):
        lastBlockHash = BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest()
        nextForger = self.pos.forger(lastBlockHash)
        return nextForger

    def createBlock(
        self, transactionFromPool: List[Transaction], forgerWallet: Wallet
    ) -> Block:
        coveredTransactions = self.getCoveredTransactionSet(transactionFromPool)
        self.executeTransactions(coveredTransactions)
        newBlock = forgerWallet.createBlock(
            coveredTransactions,
            BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest(),
            len(self.blocks),
        )
        self.blocks.append(newBlock)
        return newBlock

    def transactionExists(self, transaction: Transaction):
        for block in self.blocks:
            for blockTransaction in block.transactions:
                if transaction.equals(blockTransaction):
                    return True
        return False

    def forgerValid(self, block: Block):
        forgerPublicKey = self.pos.forger(block.lastHash)
        proposedBlockForger = block.forger
        if forgerPublicKey == proposedBlockForger:
            return True
        else:
            return False

    def transactionsValid(self, transactions: List[Transaction]):
        coveredTransactions = self.getCoveredTransactionSet(transactions)
        return len(coveredTransactions) == len(transactions)
