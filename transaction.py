import copy
import time
import uuid


class Transaction:
    def __init__(
        self, senderPublicKey: str, receiverPublicKey: str, amount: int, transType
    ) -> None:
        self.senderPublicKey = senderPublicKey
        self.receiverPublicKey = receiverPublicKey
        self.amount = amount
        self.type = transType
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = ""

    def toJson(self):
        return self.__dict__

    def sign(self, signature) -> None:
        self.signature = signature

    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation["signature"] = ""
        return jsonRepresentation

    def equals(self, transaction) -> bool:
        if self.id == transaction.id:
            return True
        else:
            return False
