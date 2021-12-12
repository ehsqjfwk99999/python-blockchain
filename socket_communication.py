from p2pnetwork.node import Node


class SocketCommunication(Node):
    def __init__(self, ip: str, port: int) -> None:
        super(SocketCommunication, self).__init__(ip, port, None)

    def startSocketCommunication(self) -> None:
        self.start()

    def inbound_node_connected(self, connected_node) -> None:
        print("inbound connection")
        self.send_to_node(connected_node, "Hi I am the node you connected to")

    def outbound_node_connected(self, connected_node) -> None:
        print("outbound connection")
        self.send_to_node(
            connected_node, "Hi I am the node who initialized the connection"
        )

    def node_message(self, connected_node, message) -> None:
        print(message)
