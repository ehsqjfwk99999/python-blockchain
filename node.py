from blockchain import Blockchain
from node_api import NodeAPI
from socket_communication import SocketCommunication
from txnpool import TransactionPool
from wallet import Wallet


class Node:
    def __init__(self, ip: str, port: int) -> None:
        self.p2p = None
        self.ip = ip
        self.port = port
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication()

    def startAPI(self, apiPort: int):
        self.api = NodeAPI()
        self.api.injectNode(self)
        self.api.start(apiPort)
