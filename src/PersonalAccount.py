from src.modules.Account import Account

class PersonalAccount(Account):
    def __init__(self, first_name: str, last_name: str, pesel: str, promo_code: str = None):
        self.account_type: str = 'personal'
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.pesel: str = pesel if (pesel is not None and len(pesel) == 11) else "Invalid"
        self.balance: float = (
            50.0
            if (
                promo_code is not None
                and len(promo_code) == 8
                and promo_code[:5] == "PROM_"
                and self.validatePromotionBirthYear()
            )
            else 0.0
        )
        self.history: list[float] = []

    def validatePromotionBirthYear(self):
        pesel: str = self.pesel
        if pesel[2] in ["0", "1"] and int(pesel[:2]) >= 60:
            return True
        elif pesel[2] in ["2", "3"]:
            return True
        else:
            return False

    def submitForLoan(self, amount: int):
        if len(self.history) >= 3 and False not in [i > 0 for i in self.history[:3]]:
            self.balance += amount
            return True
        elif len(self.history) >= 5 and sum(self.history[:5]) > amount:
            self.balance += amount
            return True
        else:
            return False

    def toDict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "pesel": self.pesel,
            "balance": self.balance,
            "history": self.history,
        }

    @classmethod
    def fromDict(cls, data):
        account = cls(data.get("first_name"), data.get("last_name"), data.get("pesel"))
        account.balance = data.get("balance", account.balance)
        account.history = data.get("history", [])
        return account