class Account:
    def normalTransfer(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.bookTransaction(-amount)
            return True
        else:
            return False

    def expressTransfer(self, amount):
        if self.balance >= amount:
            self.balance -= (amount + self.getExpressFee())
            self.bookTransaction(-amount, -self.getExpressFee())
            return True
        else:
            return False

    def receiveTransfer(self, amount):
        self.balance += amount
        self.bookTransaction(amount)
        return True

    def getExpressFee(self):
        return 1

    def bookTransaction(self, amount, fee = None):
        self.history.append(amount)
        self.history.append(fee) if fee is not None else None