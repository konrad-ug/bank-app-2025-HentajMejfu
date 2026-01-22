from src.PersonalAccount import PersonalAccount
from src.BusinessAccount import BusinessAccount
import pytest


class TestPersonalTransfers:
    @pytest.fixture()
    def pacc(self):
        account = PersonalAccount("Paweł", "Malinowski", "12345678901", "PROM_420")
        return account

    @pytest.mark.parametrize("balance, amount, expected_result, expected_balance, expected_history", [
        (100, 50, True, 50, [-50]),
        (30, 50, False, 30, [])
    ],
    ids = [
        "enough balance",
        "not enough balance"
    ])
    def test_normal_transfer(self, pacc: PersonalAccount, balance: float, amount: float, expected_result: bool, expected_balance: float, expected_history: list[float]):
        pacc.balance = balance
        assert pacc.normalTransfer(amount) is expected_result
        assert pacc.balance == expected_balance
        assert pacc.history == expected_history


    @pytest.mark.parametrize("balance, amount, expected_result, expected_balance, expected_history", [
        (50, 50, True, -1, [-50, -1]),
        (30, 50, False, 30, [])
    ],
    ids = [
        "enough balance",
        "not enough balance"
    ])
    def test_express_transfer(self, pacc: PersonalAccount, balance: float, amount: float, expected_result: bool, expected_balance: float, expected_history: list[float]):
        pacc.balance = balance
        assert pacc.expressTransfer(amount) is expected_result
        assert pacc.balance == expected_balance
        assert pacc.history == expected_history


    def test_receive_transfer(self):
        acc: PersonalAccount = PersonalAccount("Pawel", "Sobolewski", "12345678901", "PROM_4200")
        assert acc.receiveTransfer(69)
        assert acc.balance == 69
        assert acc.history == [69]


class TestBusinessTransfers:
    @pytest.fixture()
    def bacc(self):
        account = BusinessAccount("Drutex sp. z o.o.", "1234567890")
        return account

    @pytest.mark.parametrize("balance, amount, expected_result, expected_balance, expected_history", [
        (100, 20, True, 80, [-20]),
        (10, 20, False, 10, [])
    ],
    ids = [
        "enough balance",
        "not enough balance"
    ])
    def test_normal_transfer(self, bacc: BusinessAccount, balance: float, amount: float, expected_result: bool, expected_balance: float, expected_history: list[float]):
        bacc.balance = balance
        assert bacc.normalTransfer(amount) is expected_result
        assert bacc.balance == expected_balance
        assert bacc.history == expected_history


    @pytest.mark.parametrize("balance, amount, expected_result, expected_balance, expected_history", [
        (50, 50, True, -5, [-50, -5]),
        (30, 50, False, 30, [])
    ],
    ids = [
        "enough balance including fee",
        "not enough balance due to fee",
    ])
    def test_express_transfer(self, bacc: BusinessAccount, balance: float, amount: float, expected_result: bool, expected_balance: float, expected_history: list[float]):
        bacc.balance = balance
        assert bacc.expressTransfer(amount) is expected_result
        assert bacc.balance == expected_balance
        assert bacc.history == expected_history


    def test_receive_transfer(self):
        acc: BusinessAccount = BusinessAccount("Drutex sp. z o.o.", "1234567890")
        assert acc.receiveTransfer(69)
        assert acc.balance == 69
        assert acc.history == [69]