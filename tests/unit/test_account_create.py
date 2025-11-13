from src.PersonalAccount import PersonalAccount
from src.BusinessAccount import BusinessAccount


class TestPersonalAccount:
    def test_personal_account_creation(self):
        acc: PersonalAccount = PersonalAccount("John", "Doe", "12345678901")
        assert acc.first_name == "John"
        assert acc.last_name == "Doe"
        assert acc.balance == 0
        assert acc.pesel == "12345678901"
        assert acc.history == []


    def test_pesel_too_long(self):
        acc: PersonalAccount = PersonalAccount("Pawel", "Sobolewski", "12345678901234")
        assert acc.pesel == "Invalid"

    def test_pesel_too_short(self):
        acc: PersonalAccount = PersonalAccount("Maksymilian", "Bielawski", "123456")
        assert acc.pesel == "Invalid"

    def test_pesel_is_none(self):
        acc: PersonalAccount = PersonalAccount("Malwina", "Matysek", None)
        assert acc.pesel == "Invalid"


    def test_promo_is_valid(self):
        acc: PersonalAccount = PersonalAccount("Katja", "Skowronska", "06212345678", "PROM_XYZ")
        assert acc.balance == 50

    def test_promo_too_long(self):
        acc: PersonalAccount = PersonalAccount("Stanislaw", "Kossakowski", "06212345678", "PROM_XYZZ")
        assert acc.balance == 0

    def test_promo_too_short(self):
        acc: PersonalAccount = PersonalAccount("Wiktor", "Sarosiek", "06212345678", "PROM_XY")
        assert acc.balance == 0

    def test_promo_not_valid(self):
        acc: PersonalAccount = PersonalAccount("Laura", "Sakowicz", "06212345678", "PROZ_XYZ")
        assert acc.balance == 0

    def test_promo_too_old(self):
        acc: PersonalAccount = PersonalAccount("Hubet", "Wienicki", "59012345678", "PROM_XYZ")
        assert acc.balance == 0

    def test_promo_1960(self):
        acc: PersonalAccount = PersonalAccount("Renata", "Dobrowolska", "60012345678", "PROM_XYZ")
        assert acc.balance == 50


    def test_validate_promo_correct(self):
        acc: PersonalAccount = PersonalAccount("Hubert", "Baranowski", "06212345678", "PROM_XYZ")
        assert acc.validatePromotionBirthYear() is True

    def test_validate_promo_correct_after_september(self):
        acc: PersonalAccount = PersonalAccount("Mateusz", "Bartnik", "06312345678", "PROM_XYZ")
        assert acc.validatePromotionBirthYear() is True

    def test_validate_promo_too_old(self):
        acc: PersonalAccount = PersonalAccount("Mateusz", "Orodzinski", "59012345678", "PROM_XYZ")
        assert acc.validatePromotionBirthYear() is False

    def test_validate_promo_too_old_after_september(self):
        acc: PersonalAccount = PersonalAccount("Ewelina", "Maer", "59112345678", "PROM_XYZ")
        assert acc.validatePromotionBirthYear() is False


class TestBusinessAccount:
    def test_business_account_creation(self):
        acc: BusinessAccount = BusinessAccount("Drutex sp. z o.o.", "1234567890")
        assert acc.company_name == "Drutex sp. z o.o."
        assert acc.nip == "1234567890"
        assert acc.balance == 0
        assert acc.history == []


    def test_nip_too_long(self):
        acc: BusinessAccount = BusinessAccount("Drutex sp. z o.o.", "12345678901234")
        assert acc.nip == "Invalid"

    def test_nip_too_short(self):
        acc: BusinessAccount = BusinessAccount("Drutex sp. z o.o.", "123456")
        assert acc.nip == "Invalid"

    def test_nip_is_none(self):
        acc: BusinessAccount = BusinessAccount("Drutex sp. z o.o.", None)
        assert acc.nip == "Invalid"