from pytest_mock import MockerFixture
from src.PersonalAccount import PersonalAccount
from src.BusinessAccount import BusinessAccount
import pytest


class TestPersonalAccount:
    def test_personal_account_creation(self):
        acc: PersonalAccount = PersonalAccount("John", "Doe", "12345678901")
        assert acc.first_name == "John"
        assert acc.last_name == "Doe"
        assert acc.balance == 0
        assert acc.pesel == "12345678901"
        assert acc.history == []

    @pytest.mark.parametrize(
        "name, surname, pesel",
        [
            ("Pawel", "Sobolewski", "12345678901234"),
            ("Maksymilian", "Bielawski", "123456"),
            ("Malwina", "Matysek", None),
        ],
        ids=["pesel too long", "pesel too short", "pesel is None"],
    )
    def test_pesel(self, name: str, surname: str, pesel: str):
        acc: PersonalAccount = PersonalAccount(name, surname, pesel)
        assert acc.pesel == "Invalid"

    @pytest.mark.parametrize(
        "name, surname, pesel, promo_code, expected_balance",
        [
            ("Katja", "Skowronska", "06212345678", "PROM_XYZ", 50),
            ("Stanislaw", "Kossakowski", "06212345678", "PROM_XYZZ", 0),
            ("Wiktor", "Sarosiek", "06212345678", "PROM_XY", 0),
            ("Laura", "Sakowicz", "06212345678", "PROZ_XYZ", 0),
            ("Hubet", "Wienicki", "59012345678", "PROM_XYZ", 0),
            ("Renata", "Dobrowolska", "60012345678", "PROM_XYZ", 50),
        ],
        ids=[
            "promo is valid",
            "promo too long",
            "promo too short",
            "promo not valid",
            "promo too old",
            "promo 1960",
        ],
    )
    def test_promo(
        self,
        name: str,
        surname: str,
        pesel: str,
        promo_code: str,
        expected_balance: float,
    ):
        acc: PersonalAccount = PersonalAccount(name, surname, pesel, promo_code)
        assert acc.balance == expected_balance

    @pytest.mark.parametrize(
        "name, surname, pesel, promo_code, expected_result",
        [
            ("Hubert", "Baranowski", "06212345678", "PROM_XYZ", True),
            ("Mateusz", "Bartnik", "06312345678", "PROM_XYZ", True),
            ("Mateusz", "Orodzinski", "59012345678", "PROM_XYZ", False),
            ("Ewelina", "Maer", "59112345678", "PROM_XYZ", False),
        ],
        ids=[
            "validate promo correct",
            "validate promo correct after september",
            "validate promo too old",
            "validate promo too old after september",
        ],
    )
    def test_validate_promo_correct(
        self,
        name: str,
        surname: str,
        pesel: str,
        promo_code: str,
        expected_result: bool,
    ):
        acc: PersonalAccount = PersonalAccount(name, surname, pesel, promo_code)
        assert acc.validatePromotionBirthYear() is expected_result


class TestBusinessAccount:
    def test_business_account_creation(self, mocker: MockerFixture):
        mock = mocker.patch("requests.get")
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            "result": {"subject": {"statusValue": "Czynny"}}
        }
        acc: BusinessAccount = BusinessAccount("Drutex sp. z o.o.", "1234567890")
        assert acc.company_name == "Drutex sp. z o.o."
        assert acc.nip == "1234567890"
        assert acc.balance == 0
        assert acc.history == []

    @pytest.mark.parametrize(
        "company_name, nip",
        [
            ("Drutex sp. z o.o.", "12345678901234"),
            ("Drutex sp. z o.o.", "123456"),
            ("Drutex sp. z o.o.", None),
        ],
        ids=["nip too long", "nip too short", "nip is None"],
    )
    def test_nip_too_long(self, company_name: str, nip: str):
        acc: BusinessAccount = BusinessAccount(company_name, nip)
        assert acc.nip == "Invalid"

    def test_validate_nip_inactive(self, mocker: MockerFixture):
        mock = mocker.patch("requests.get")
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            "result": {"subject": {"statusValue": "Nieaktywny"}}
        }
        acc = BusinessAccount.__new__(BusinessAccount)
        assert not acc.validateNIP("1234567890")

    def test_validate_nip_error(self, mocker: MockerFixture):
        mock = mocker.patch("requests.get")
        mock.return_value.status_code = 500
        acc = BusinessAccount.__new__(BusinessAccount)
        assert not acc.validateNIP("1234567890")

    def test_business_account_invalid_nip_status(self, mocker: MockerFixture):
        mock = mocker.patch("requests.get")
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            "result": {"subject": {"statusValue": "Nieaktywny"}}
        }
        with pytest.raises(ValueError, match="Company not registered!!"):
            BusinessAccount("FakeCompany sp. z o.o.", "1234567890")

