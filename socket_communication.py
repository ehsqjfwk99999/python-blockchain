import json
from typing import List

from p2pnetwork.node import Node

from blockchain_utils import BlockchainUtils
from message import Message
from peer_discovery_handler import PeerDiscoveryHandler
from socket_connector import SocketConnector


class SocketCommunication(Node):
    def __init__(self, ip: str, port: int) -> None:
        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers: List[SocketConnector] = []
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)
        self.socketConnector = SocketConnector(ip, port)

    def connectToFirstNode(self) -> None:
        if self.socketConnector.port != 10001:
            self.connect_with_node("localhost", 10001)

    def startSocketCommunication(self, node) -> None:
        self.node = node
        self.start()
        self.peerDiscoveryHandler.start()
        self.connectToFirstNode()

    def inbound_node_connected(self, connected_node) -> None:
        self.peerDiscoveryHandler.handshake(connected_node)

    def outbound_node_connected(self, connected_node) -> None:
        self.peerDiscoveryHandler.handshake(connected_node)

    def node_message(self, connected_node, message: Message) -> None:
        message = BlockchainUtils.decode(json.dumps(message))
        if message.messageType == "DISCOVERY":
            self.peerDiscoveryHandler.handleMessage(message)
        elif message.messageType == "TRANSACTION":
            transaction = message.data
            self.node.handleTransaction(transaction)

    def send(self, receiver, message):
        self.send_to_node(receiver, message)

    def broadcast(self, message):
        self.send_to_nodes(message)
