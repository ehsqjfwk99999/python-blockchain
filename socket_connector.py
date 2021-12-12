class SocketConnector:
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port

    def equals(self, connector) -> bool:
        return self.ip == connector.ip and self.port == connector.port
