from src.PersonalAccount import PersonalAccount


class TestLoans:
    def test_loan_approved_last_three(self):
        acc: PersonalAccount = PersonalAccount('Maliwna', 'Matysek', '12345678901')
        acc.receiveTransfer(69)
        acc.receiveTransfer(420)
        acc.receiveTransfer(2137)
        assert acc.submit_for_loan(420) is True
        assert acc.balance == 3046

    def test_loan_approved_last_five(self):
        acc: PersonalAccount = PersonalAccount('Maliwna', 'Matysek', '12345678901')
        acc.receiveTransfer(2137)
        acc.expressTransfer(420)
        acc.receiveTransfer(69)
        acc.normalTransfer(20)
        assert acc.submit_for_loan(420) is True
        assert acc.balance == 2185

    def test_loan_rejected_too_few_transactions(self):
        acc: PersonalAccount = PersonalAccount('Maliwna', 'Matysek', '12345678901')
        acc.receiveTransfer(20)
        assert acc.submit_for_loan(420) is False
        assert acc.balance == 20

    def test_loan_rejected_last_five(self):
        acc: PersonalAccount = PersonalAccount('Maliwna', 'Matysek', '12345678901')
        acc.receiveTransfer(420)
        acc.expressTransfer(20)
        acc.expressTransfer(20)
        assert acc.submit_for_loan(2137) is False
        assert acc.balance == 378