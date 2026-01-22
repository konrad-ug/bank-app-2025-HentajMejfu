from pytest_mock import MockerFixture
from src.PersonalAccount import PersonalAccount
from src.BusinessAccount import BusinessAccount
import pytest


class TestLoans:

    @pytest.fixture()
    def p_acc(self):
        account = PersonalAccount('Maliwna', 'Matysek', '12345678901')
        return account

    @pytest.mark.parametrize("history, balance, amount, expected_result, expected_balance", [
        ([69, 420, 2137], 2626, 420, True, 3046),
        ([2137, -420, -1, 69, -20], 1765, 420, True, 2185),
        ([420, -50, -50], 320, 420, False, 320),
        ([20], 20, 420, False, 20),
        ([420, -20, -1, -20, -1], 378, 2137, False, 378)
    ],
    ids = [
        "three positives",
        "five transactions",
        "three transactions with two negatives",
        "not enough transactions",
        "multiple transactions with sum too low"
    ])
    def test_loan(self, p_acc: PersonalAccount, history: list[float], balance: float, amount: int, expected_result: bool, expected_balance: float):
        p_acc.history = history
        p_acc.balance = balance
        assert p_acc.submitForLoan(amount) is expected_result
        assert p_acc.balance == expected_balance


    @pytest.fixture()
    def b_acc(self, mocker: MockerFixture):
        mock = mocker.patch("requests.get")
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {
            "result": {"subject": {"statusValue": "Czynny"}}
        }
        account = BusinessAccount('Drutex s.p. z o.o.', '1234567890')
        return account

    @pytest.mark.parametrize("balance, history, amount, expected_result, expected_balance", [
        (280, [1775, -1775, 280], 140, True, 420),
        (420, [225, -1775], 420, False, 420),
        (2137, [420, -420, 2137], 213769, False, 2137)
    ],
    ids = [
        "loan granted",
        "not enough balance",
        "no ZUS history"
    ])
    def test_loan_business(self, b_acc: BusinessAccount, balance: float, history: list[float], amount: int, expected_result: bool, expected_balance: float):
        b_acc.balance = balance
        b_acc.history = history
        assert b_acc.submitForLoan(amount) is expected_result
        assert b_acc.balance == expected_balance