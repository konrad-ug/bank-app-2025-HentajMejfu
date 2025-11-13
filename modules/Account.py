class Account:
    def normalTransfer(self, amount: float):
        if self.balance >= amount:
            self.balance -= amount
            self.bookTransaction(-amount)
            return True
        else:
            return False

    def expressTransfer(self, amount: float):
        if self.balance >= amount:
            self.balance -= (amount + self.getExpressFee())
            self.bookTransaction(-amount, -self.getExpressFee())
            return True
        else:
            return False

    def receiveTransfer(self, amount: float):
        self.balance += amount
        self.bookTransaction(amount)
        return True

    def getExpressFee(self):
        return 1

    def bookTransaction(self, amount: float, fee: int = None):
        self.history.append(amount)
        self.history.append(fee) if fee is not None else None