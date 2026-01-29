import pytest
import requests


class TestSaveLoadApi:
    url = "http://127.0.0.1:5000"
    account_details = {"name": "james", "surname": "hetfield", "pesel": "89092909825"}
    transfer_data = {"amount": 100, "type": "incoming"}

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        response = requests.post(f"{self.url}/api/accounts", json=self.account_details)
        requests.post(
            f"{self.url}/api/accounts/{self.account_details['pesel']}/transfer",
            json=self.transfer_data,
        )
        assert response.status_code == 201
        yield
        response = requests.get(f"{self.url}/api/accounts")
        accounts = response.json()
        for account in accounts:
            pesel = account["pesel"]
            requests.delete(f"{self.url}/api/accounts/{pesel}")

    def test_save_and_load_accounts(self):
        response = requests.post(f"{self.url}/api/accounts/save")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Accounts saved to MongoDB"

        response = requests.get(f"{self.url}/api/accounts")
        accounts = response.json()
        for account in accounts:
            pesel = account["pesel"]
            requests.delete(f"{self.url}/api/accounts/{pesel}")

        response = requests.post(f"{self.url}/api/accounts/load")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Accounts loaded from MongoDB"