import requests

from blockchain_utils import BlockchainUtils
from wallet import Wallet


def postTransaction(sender, receiver, amount, transType):
    transaction = sender.createTransaction(
        receiver.publicKeyString(), amount, transType
    )
    url = "http://localhost:5001/transaction"
    package = {"transaction": BlockchainUtils.encode(transaction)}
    requests.post(url, json=package)


if __name__ == "__main__":
    bob = Wallet()
    alice = Wallet()
    alice.fromKey("./keys/stakerPrivateKey.pem")
    exchange = Wallet()

    postTransaction(exchange, alice, 100, "EXCHANGE")
    postTransaction(exchange, bob, 100, "EXCHANGE")
    postTransaction(exchange, bob, 100, "EXCHANGE")

    postTransaction(alice, alice, 25, "STAKE")
    postTransaction(alice, bob, 1, "TRANSFER")
    postTransaction(alice, bob, 1, "TRANSFER")
    postTransaction(alice, bob, 1, "TRANSFER")
