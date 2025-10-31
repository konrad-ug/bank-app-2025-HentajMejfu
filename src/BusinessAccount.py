from modules.Account import Account

class BusinessAccount(Account):
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip if (nip is not None and len(nip) == 10) else "Invalid"
        self.balance = 0
        self.history = []

    def getExpressFee(self):
        return 5