from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "12345678901"


    def test_pesel_too_long(self):
        acc = Account("Pawel", "Sobolewski", "12345678901234")
        assert acc.pesel == "Invalid"

    def test_pesel_too_short(self):
        acc = Account("Maksymilian", "Bielawski", "123456")
        assert acc.pesel == "Invalid"

    def test_pesel_is_none(self):
        acc = Account("Malwina", "Matysek", None)
        assert acc.pesel == "Invalid"


    def test_promo_is_valid(self):
        acc = Account("Katja", "Skowronska", "06212345678", "PROM_XYZ")
        assert acc.balance == 50

    def test_promo_too_long(self):
        acc = Account("Stanislaw", "Kossakowski", "06212345678", "PROM_XYZZ")
        assert acc.balance == 0

    def test_promo_too_short(self):
        acc = Account("Wiktor", "Sarosiek", "06212345678", "PROM_XY")
        assert acc.balance == 0

    def test_promo_not_valid(self):
        acc = Account("Laura", "Sakowicz", "06212345678", "PROZ_XYZ")
        assert acc.balance == 0

    def test_promo_too_old(self):
        acc = Account("Hubet", "Wienicki", "59012345678", "PROM_XYZ")
        assert acc.balance == 0

    def test_promo_1960(self):
        acc = Account("Malwina", "Matysek", "60012345678", "PROM_XYZ")
        assert acc.balance == 50


    def test_validate_promo_correct(self):
        acc = Account("Malwina", "Matysek", "06212345678", "PROM_XYZ")
        assert acc.validateBirthYear() is True

    def test_validate_promo_correct_after_september(self):
        acc = Account("Malwina", "Matysek", "06312345678", "PROM_XYZ")
        assert acc.validateBirthYear() is True

    def test_validate_promo_too_old(self):
        acc = Account("Malwina", "Matysek", "59012345678", "PROM_XYZ")
        assert acc.validateBirthYear() is False

    def test_validate_promo_too_old_after_september(self):
        acc = Account("Malwina", "Matysek", "59112345678", "PROM_XYZ")
        assert acc.validateBirthYear() is False