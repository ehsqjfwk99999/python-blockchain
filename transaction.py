import uuid
import time
import copy


class Transaction:
    def __init__(self, senderPublicKey, receiverPublicKey, amount, transType):
        self.senderPublicKey = senderPublicKey
        self.receiverPublicKey = receiverPublicKey
        self.amount = amount
        self.type = transType
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = ""

    def toJson(self):
        return self.__dict__

    def sign(self, signature):
        self.signature = signature

    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation["signature"] = ""
        return jsonRepresentation

    def equals(self, transaction):
        if self.id == transaction.id:
            return True
        else:
            return False