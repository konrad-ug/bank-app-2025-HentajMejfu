from modules.Account import Account

class PersonalAccount(Account):
    def __init__(self, first_name: str, last_name: str, pesel: str, promo_code: str = None):
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.pesel: str = pesel if (pesel is not None and len(pesel) == 11) else "Invalid"
        self.balance: float = (
            50
            if (
                promo_code is not None
                and len(promo_code) == 8
                and promo_code[:5] == "PROM_"
                and self.validatePromotionBirthYear()
            )
            else 0
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

    def submit_for_loan(self, amount: int):
        if len(self.history) >= 3 and False not in [i > 0 for i in self.history[:3]]:
            self.balance += amount
            return True
        elif len(self.history) >= 5 and sum(self.history[:5]) > amount:
            self.balance += amount
            return True
        else:
            return False