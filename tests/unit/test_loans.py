from src.PersonalAccount import PersonalAccount
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
        assert p_acc.submit_for_loan(amount) is expected_result
        assert p_acc.balance == expected_balance