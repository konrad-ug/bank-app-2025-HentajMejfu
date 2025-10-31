from modules.Account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if (pesel is not None and len(pesel) == 11) else "Invalid"
        self.balance = (
            50
            if (
                promo_code is not None
                and len(promo_code) == 8
                and promo_code[:5] == "PROM_"
                and self.validatePromotionBirthYear()
            )
            else 0
        )
        self.history = []

    def validatePromotionBirthYear(self):
        if self.pesel is not None:
            pesel = self.pesel
            if pesel[2] in ["0", "1"] and int(pesel[:2]) >= 60:
                return True
            elif pesel[2] in ["2", "3"]:
                return True
            else:
                return False
        else:
            return False