from datetime import date
from src.smtp.smtp import SMTPClient as smtp

class Account:
    account_type = 'base'

    def normalTransfer(self, amount: float) -> bool:
        if self.balance >= amount:
            self.balance -= amount
            self.bookTransaction(-amount)
            return True
        else:
            return False

    def expressTransfer(self, amount: float) -> bool:
        if self.balance >= amount:
            self.balance -= (amount + self.getExpressFee())
            self.bookTransaction(-amount, -self.getExpressFee())
            return True
        else:
            return False

    def receiveTransfer(self, amount: float) -> bool:
        self.balance += amount
        self.bookTransaction(amount)
        return True

    def getExpressFee(self) -> int:
        return 1

    def bookTransaction(self, amount: float, fee: int = None):
        self.history.append(amount)
        self.history.append(fee) if fee is not None else None

    def send_history_via_email(self, email_adress: str) -> bool:
        today = str(date.today())

        if self.account_type == 'personal':
            return smtp.send(f'Account Transfer History {today}', f'Personal Account History: {self.history}', email_adress)
        elif self.account_type == 'business':
            return smtp.send(f'Account Transfer History {today}', f'Business Account History: {self.history}', email_adress)
        return False