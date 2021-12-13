import threading
import time
from typing import List

from blockchain_utils import BlockchainUtils
from message import Message
from socket_connector import SocketConnector


class PeerDiscoveryHandler:
    def __init__(self, node) -> None:
        self.socketCommunication = node

    def start(self) -> None:
        statusThread = threading.Thread(target=self.status)
        statusThread.start()
        discoveryThread = threading.Thread(target=self.discovery)
        discoveryThread.start()

    def status(self) -> None:
        while True:
            print("Current Connections")
            for peer in self.socketCommunication.peers:
                print(f"{peer.ip} : {peer.port}")
            time.sleep(10)

    def discovery(self) -> None:
        while True:
            handshakeMessage = self.handshakeMessage()
            self.socketCommunication.broadcast(handshakeMessage)
            time.sleep(10)

    def handshake(self, connect_node) -> None:
        handshakeMessage = self.handshakeMessage()
        self.socketCommunication.send(connect_node, handshakeMessage)

    def handshakeMessage(self):
        ownConnector = self.socketCommunication.socketConnector
        ownPeers = self.socketCommunication.peers
        data: List[SocketConnector] = ownPeers
        messageType: str = "DISCOVERY"
        message = Message(ownConnector, messageType, data)
        encodedMessage = BlockchainUtils.encode(message)
        return encodedMessage

    def handleMessage(self, message: Message) -> None:
        peersSocketConnector: SocketConnector = message.senderConnector
        peersPeerList: List[SocketConnector] = message.data
        newPeer: bool = True
        for peer in self.socketCommunication.peers:
            if peer.equals(peersSocketConnector):
                newPeer = False
        if newPeer == True:
            self.socketCommunication.peers.append(peersSocketConnector)

        for peersPeer in peersPeerList:
            peerKnown = False
            for peer in self.socketCommunication.peers:
                if peer.equals(peersPeer):
                    peerKnown = True
            if not peerKnown and not peersPeer.equals(
                self.socketCommunication.socketConnector
            ):
                self.socketCommunication.connect_with_node(peersPeer.ip, peersPeer.port)
