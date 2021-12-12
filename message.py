class Message:
    def __init__(self, senderConnector, messageType, data) -> None:
        self.senderConnector = senderConnector
        self.messageType = messageType
        self.data = data
