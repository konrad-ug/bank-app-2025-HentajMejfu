class Account:
    def normalTransfer(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.bookTransaction('Normal Transfer', amount)
            return True
        else:
            return False

    def expressTransfer(self, amount):
        if self.balance >= amount:
            self.balance -= (amount + self.getExpressFee())
            self.bookTransaction('Express Transfer', amount, self.getExpressFee())
            return True
        else:
            return False

    def receiveTransfer(self, amount):
        self.balance += amount
        self.bookTransaction('Transfer Received', amount)
        return True

    def getExpressFee(self):
        return 1

    def bookTransaction(self, op, amount, fee = None):
        self.history.append({
            "operation": op,
            "amount": amount,
            "fee": fee
        })