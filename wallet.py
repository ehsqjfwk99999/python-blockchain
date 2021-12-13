from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from block import Block
from blockchain_utils import BlockchainUtils
from transaction import Transaction


class Wallet:
    def __init__(self):
        self.keyPair = RSA.generate(2048)

    def fromKey(self, file: str) -> None:
        key = ""
        with open(file, "r") as keyfile:
            key = RSA.importKey(keyfile.read())
        self.keyPair = key

    def sign(self, data):
        dataHash = BlockchainUtils.hash(data)
        signatureSchemeObject = PKCS1_v1_5.new(self.keyPair)
        signature = signatureSchemeObject.sign(dataHash)
        return signature.hex()

    @staticmethod
    def signatureValid(data, signature, publicKeyString):
        signature = bytes.fromhex(signature)
        dataHash = BlockchainUtils.hash(data)
        publicKey = RSA.importKey(publicKeyString)
        signatureSchemeObject = PKCS1_v1_5.new(publicKey)
        signatureValid = signatureSchemeObject.verify(dataHash, signature)
        return signatureValid

    def publicKeyString(self):
        publicKeyString = self.keyPair.publickey().exportKey("PEM").decode("utf-8")
        return publicKeyString

    def createTransaction(self, receiver, amount, transType):
        transaction = Transaction(self.publicKeyString(), receiver, amount, transType)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transaction

    def createBlock(self, transactions, lastHash, blockCount):
        print(f"createblock : {self.publicKeyString()}")
        print(f"createblock2 : {id(self)}")
        block = Block(transactions, lastHash, self.publicKeyString(), blockCount)
        signature = self.sign(block.payload())
        block.sign(signature)
        return block
