import pprint

from account_model import AccountModel
from bcutils import BlockchainUtils
from block import Block
from blockchain import Blockchain
from node import Node
from txnpool import TransactionPool
from wallet import Wallet

if __name__ == "__main__":

    node = Node()
    print(node.blockchain)
    print(node.wallet)
    print(node.transactionPool)
