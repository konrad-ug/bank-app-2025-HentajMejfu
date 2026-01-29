import pytest
from src.PersonalAccount import PersonalAccount
from src.MongoAccountsRepository import MongoAccountRepository
from pytest_mock import MockFixture


class TestMongoAccountRegistry:
    account1 = PersonalAccount("Alice", "Smith", "12345678901")
    account2 = PersonalAccount("Bob", "Johnson", "10987654321")

    @pytest.fixture(autouse=True)
    def mongo_repo(self):
        self.account1.receiveTransfer(100)

    def test_save_and_load_accounts(self, mocker):
        mock_collection = mocker.Mock()
        mock_collection.find.return_value = [
            self.account1.toDict(),
            self.account2.toDict(),
        ]
        mongo_repo = MongoAccountRepository(collection=mock_collection)
        mongo_repo.save_all([self.account1, self.account2])

        loaded_accounts = mongo_repo.load_all()

        assert len(loaded_accounts) == 2
        assert any(
            acc.pesel == "12345678901" and acc.first_name == "Alice"
            for acc in loaded_accounts
        )
        assert any(
            acc.pesel == "10987654321" and acc.first_name == "Bob"
            for acc in loaded_accounts
        )