from transaction import Transaction

import time
import copy
from typing import List


class Block:
    def __init__(
        self, transactions: List[Transaction], lastHash: str, forger, blockCount: int
    ) -> None:
        self.transactions = transactions
        self.lastHash = lastHash
        self.forger = forger
        self.blockCount = blockCount
        self.timestamp = time.time()
        self.signature = ""

    @staticmethod
    def genesis():
        genesisBlock: Block = Block([], "genesisHash", "genesis", 0)
        genesisBlock.timestamp = 0
        return genesisBlock

    def toJson(self):
        data = {}
        data["lastHash"] = self.lastHash
        data["forger"] = self.forger
        data["blockCount"] = self.blockCount
        data["timestamp"] = self.timestamp
        data["signature"] = self.signature
        jsonTransactions = []
        for transaction in self.transactions:
            jsonTransactions.append(transaction.toJson())
        data["transactions"] = jsonTransactions
        return data

    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation["signature"] = ""
        return jsonRepresentation

    def sign(self, signature) -> None:
        self.signature = signature
