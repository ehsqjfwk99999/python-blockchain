import copy

from jsonpickle.pickler import encode

from block import Block
from blockchain import Blockchain
from blockchain_utils import BlockchainUtils
from message import Message
from node_api import NodeAPI
from socket_communication import SocketCommunication
from transaction import Transaction
from transaction_pool import TransactionPool
from wallet import Wallet


class Node:
    def __init__(self, ip: str, port: int, key: str = None) -> None:
        self.p2p = None
        self.ip = ip
        self.port = port
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()
        if key is not None:
            self.wallet.fromKey(key)

    def startP2P(self) -> None:
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication(self)

    def startAPI(self, apiPort: int) -> None:
        self.api = NodeAPI()
        self.api.injectNode(self)
        self.api.start(apiPort)

    def handleTransaction(self, transaction: Transaction) -> None:
        data = transaction.payload()
        signature = transaction.signature
        signerPublicKey = transaction.senderPublicKey
        signatureValid = Wallet.signatureValid(data, signature, signerPublicKey)
        transactionExists = self.transactionPool.transactionExists(transaction)
        transactionInBlock = self.blockchain.transactionExists(transaction)
        if not transactionExists and not transactionInBlock and signatureValid:
            self.transactionPool.addTransaction(transaction)
            message = Message(self.p2p.socketConnector, "TRANSACTION", transaction)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)
            forgerRequired = self.transactionPool.forgerRequired()
            if forgerRequired:
                self.forge()

    def handleBlock(self, block: Block):
        forger = block.forger
        blockHash = block.payload()
        signature = block.signature

        blockCountValid = self.blockchain.blockCountValid(block)
        lastBlockHashValid = self.blockchain.lastBlockHashValid(block)
        forgerValid = self.blockchain.forgerValid(block)
        transactionsValid = self.blockchain.transactionsValid(block.transactions)
        signatureValid = Wallet.signatureValid(blockHash, signature, forger)
        if not blockCountValid:
            self.requestChain()
        if lastBlockHashValid and forgerValid and transactionsValid and signatureValid:
            self.blockchain.addBlock(block)
            self.transactionPool.removeFromPool(block.transactions)
            message = Message(self.p2p.socketConnector, "BLOCK", block)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)

    def requestChain(self):
        message = Message(self.p2p.socketConnector, "BLOCKCHAINREQUEST", None)
        encodedMessage = BlockchainUtils.encode(message)
        self.p2p.broadcast(encodedMessage)

    def handleBlockchainRequest(self, requestingNode):
        message = Message(self.p2p.socketConnector, "BLOCKCHAIN", self.blockchain)
        encodedMessage = BlockchainUtils.encode(message)
        self.p2p.send(requestingNode, encodedMessage)

    def handleBlockchain(self, blockchain: Blockchain):
        localBlockchainCopy = copy.deepcopy(self.blockchain)
        localBlockCount = len(localBlockchainCopy.blocks)
        receivedChainBlockCount = len(blockchain.blocks)
        if localBlockCount <= receivedChainBlockCount:
            for blockNumber, block in enumerate(blockchain.blocks):
                if blockNumber >= localBlockCount:
                    localBlockchainCopy.addBlock(block)
                    self.transactionPool.removeFromPool(block.transactions)
            self.blockchain = localBlockchainCopy

    def forge(self):
        forger = self.blockchain.nextForger()
        if forger == self.wallet.publicKeyString():
            print("I am the next forger")
            block = self.blockchain.createBlock(
                self.transactionPool.transactions, self.wallet
            )
            self.transactionPool.removeFromPool(block.transactions)
            message = Message(self.p2p.socketConnector, "BLOCK", block)
            encodedMessage = BlockchainUtils.encode(message)
            self.p2p.broadcast(encodedMessage)
        else:
            print("I am not the next forger")
