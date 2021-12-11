from typing import Any, List

from bcutils import BlockchainUtils
from block import Block


class Blockchain:
    def __init__(self) -> None:
        self.blocks: List[Block] = [Block.genesis()]

    def addBlock(self, block: Block) -> None:
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
