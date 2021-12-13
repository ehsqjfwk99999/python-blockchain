from typing import List

from socket_connector import SocketConnector


class Message:
    def __init__(
        self, senderConnector: SocketConnector, messageType: str, data
    ) -> None:
        self.senderConnector = senderConnector
        self.messageType = messageType
        self.data: List[SocketConnector] = data
