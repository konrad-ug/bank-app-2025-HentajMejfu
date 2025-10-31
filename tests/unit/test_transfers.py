from src.PersonalAccount import PersonalAccount
from src.BusinessAccount import BusinessAccount


class TestPersonalTransfers:
    def test_normal_transfer_enough(self):
        acc = PersonalAccount("Ewa", "Karp", "12345678901", "PROM_420")
        assert acc.normalTransfer(20) is True
        assert acc.history[0] == { "operation": "Normal Transfer", "amount": 20, "fee": None }

    def test_normal_transfer_not_enough(self):
        acc = PersonalAccount("Pawel", "Malinowski", "12345678901", "PROM_4200")
        assert acc.normalTransfer(20) is False


    def test_express_transfer_enough(self):
        acc = PersonalAccount("Tomasz", "Buczkowicz", "12345678901", "PROM_420")
        assert acc.expressTransfer(50) is True
        assert acc.balance == -1
        assert acc.history[0] == { "operation": "Express Transfer", "amount": 50, "fee": 1 }

    def test_express_transfer_not_enough(self):
        acc = PersonalAccount("Maciej", "Niedzwiedz", "12345678901", "PROM_420")
        assert acc.expressTransfer(51) is False

    def test_express_transfer_not_enough_2(self):
        acc = PersonalAccount("Pawel", "Sobolewski", "12345678901", "PROM_4200")
        assert acc.expressTransfer(50) is False

    def test_receive_transfer(self):
        acc = PersonalAccount("Pawel", "Sobolewski", "12345678901", "PROM_4200")
        assert acc.receiveTransfer(69)
        assert acc.balance == 69
        assert acc.history[0] == { "operation": "Transfer Received", "amount": 69, "fee": None }


class TestBusinessTransfers:
    def test_normal_transfer_enough(self):
        acc = BusinessAccount("Drutex sp. z o.o.", "1234567890")
        acc.balance = 20
        assert acc.normalTransfer(20) is True
        assert acc.history[0] == { "operation": "Normal Transfer", "amount": 20, "fee": None }

    def test_normal_transfer_not_enough(self):
        acc = BusinessAccount("Drutex sp. z o.o.", "1234567890")
        assert acc.normalTransfer(20) is False


    def test_express_transfer_enough(self):
        acc = BusinessAccount("Drutex sp. z o.o.", "1234567890")
        acc.balance = 50
        assert acc.expressTransfer(50) is True
        assert acc.balance == -5
        assert acc.history[0] == { "operation": "Express Transfer", "amount": 50, "fee": 5 }

    def test_express_transfer_not_enough(self):
        acc = BusinessAccount("Drutex sp. z o.o.", "1234567890")
        acc.balance = 50
        assert acc.expressTransfer(51) is False

    def test_express_transfer_not_enough_2(self):
        acc = BusinessAccount("Drutex sp. z o.o.", "1234567890")
        assert acc.expressTransfer(50) is False

    def test_receive_transfer(self):
        acc = PersonalAccount("Pawel", "Sobolewski", "12345678901", "PROM_4200")
        assert acc.receiveTransfer(69)
        assert acc.balance == 69
        assert acc.history[0] == { "operation": "Transfer Received", "amount": 69, "fee": None }