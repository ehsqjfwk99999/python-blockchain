from flask import Flask, jsonify
from flask_classful import FlaskView, request, route

from blockchain_utils import BlockchainUtils

node = None


class NodeAPI(FlaskView):
    def __init__(self) -> None:
        self.app = Flask(__name__)

    def start(self, apiPort: int) -> None:
        NodeAPI.register(self.app, route_base="/")
        self.app.run(host="localhost", port=apiPort)

    def injectNode(self, injectedNode) -> None:
        global node
        node = injectedNode

    @route("/info", methods=["GET"])
    def info(self):
        return "Info", 200

    @route("/blockchain", methods=["GET"])
    def blockchain(self):
        return node.blockchain.toJson(), 200

    @route("/transactionPool", methods=["GET"])
    def transactionPool(self):
        transactions = {}
        for ctr, transaction in enumerate(node.transactionPool.transactions):
            transactions[ctr] = transaction.toJson()
        return jsonify(transactions), 200

    @route("/transaction", methods=["POST"])
    def transaction(self):
        values = request.get_json()
        if not "transaction" in values:
            return "Missing transaction value", 400
        transaction = BlockchainUtils.decode(values["transaction"])
        node.handleTransaction(transaction)
        response = {"message": "received transaction"}
        return jsonify(response), 201
