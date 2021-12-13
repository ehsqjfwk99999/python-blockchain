import requests

from blockchain_utils import BlockchainUtils
from wallet import Wallet

if __name__ == "__main__":
    bob = Wallet()
    alice = Wallet()
    exchange = Wallet()

    transaction = exchange.createTransaction(alice.publicKeyString(), 10, "EXCHANGE")

    url = "http://localhost:5001/transaction"
    package = {"transaction": BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)
    print(request.text)
