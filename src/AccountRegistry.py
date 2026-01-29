from src.PersonalAccount import PersonalAccount

class AccountRegistry:

    def __init__(self):
        self.accounts: list[PersonalAccount] = []

    def addAccount(self, account: PersonalAccount):
        self.accounts.append(account)

    def search(self, pesel: str):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None

    def getAllAccounts(self):
        return self.accounts

    def getNumberOfAccounts(self):
        return len(self.accounts)

    def removeAccount(self, pesel: str):
        account = self.search(pesel)
        if account:
            self.accounts.remove(account)
            return True
        return False