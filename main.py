import pprint
import sys

from account_model import AccountModel
from block import Block
from blockchain import Blockchain
from blockchain_utils import BlockchainUtils
from node import Node
from txnpool import TransactionPool
from wallet import Wallet

if __name__ == "__main__":

    ip = sys.argv[1]
    port = int(sys.argv[2])

    node = Node(ip, port)
    node.startP2P()

    if port == 10002:
        node.p2p.connect_with_node("localhost", 10001)
