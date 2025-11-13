from modules.Account import Account

class BusinessAccount(Account):
    def __init__(self, company_name: str, nip: str):
        self.company_name: str = company_name
        self.nip: str = nip if (nip is not None and len(nip) == 10) else "Invalid"
        self.balance: float = 0
        self.history: list[float] = []

    def getExpressFee(self):
        return 5