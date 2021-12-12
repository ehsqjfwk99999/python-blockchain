from typing import Dict, List


class AccountModel:
    def __init__(self) -> None:
        self.accounts: List[str] = []
        self.balances: Dict[str, int] = {}

    def addAccount(self, publicKeyString: str) -> None:
        if not publicKeyString in self.accounts:
            self.accounts.append(publicKeyString)
            self.balances[publicKeyString] = 0

    def getBalance(self, publicKeyString: str) -> int:
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        return self.balances[publicKeyString]

    def updateBalance(self, publicKeyString: str, amount: int) -> None:
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        self.balances[publicKeyString] += amount
