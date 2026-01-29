import requests
import pytest


class TestPerf:
    url = "http://127.0.0.1:5000/api/accounts"
    account_details = {"name": "Dariusz", "surname": "Dudek", "pesel": "12345678901"}
    iteration_count = 100
    timeout = 0.5

    @pytest.fixture(autouse=True, scope="function")
    def clear_accounts(self):
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            accounts = response.json()
            for account in accounts:
                pesel = account["pesel"]
                requests.delete(f"{self.url}/{pesel}", timeout=self.timeout)
        except Exception as e:
            print(f"Warning: could not clear accounts: {e}")

    def test_create_delete_perf(self):
        for _ in range(self.iteration_count):
            create_response = requests.post(self.url, json=self.account_details, timeout=self.timeout)
            assert create_response.status_code == 201
            assert create_response.json()["message"] == "Account created"

            del_response = requests.delete(f"{self.url}/{self.account_details['pesel']}", timeout=self.timeout)
            assert del_response.status_code == 200
            assert del_response.json()["message"] == "Account deleted"

    def test_create_delete_perf_group(self):
        pesels = [f"12345678{i:03d}" for i in range(1000)]
        for pesel in pesels:
            body = {**self.account_details, "pesel": pesel}
            create_res = requests.post(self.url, json=body, timeout=self.timeout)
            assert create_res.status_code == 201
            assert create_res.json()["message"] == "Account created"

        for pesel in pesels:
            del_res = requests.delete(f"{self.url}/{pesel}", timeout=self.timeout)
            assert del_res.status_code == 200
            assert del_res.json()["message"] == "Account deleted"

    def test_transfer_perf(self):
        create_response = requests.post(self.url, json=self.account_details, timeout=self.timeout)
        assert create_response.status_code == 201
        assert create_response.json()["message"] == "Account created"

        for _ in range(self.iteration_count):
            transfer_response = requests.post(
                f"{self.url}/{self.account_details['pesel']}/transfer",
                json={"type": "incoming", "amount": 100},
                timeout=5,
            )
            assert transfer_response.status_code == 200
            assert transfer_response.json()["message"] == "Accepted for processing"

        account_response = requests.get(f"{self.url}/{self.account_details['pesel']}", timeout=self.timeout)
        account_data = account_response.json()
        assert "balance" in account_data
        expected_balance = 100 * self.iteration_count
        assert account_data["balance"] == expected_balance, f"Expected {expected_balance}, got {account_data['balance']}"

        del_response = requests.delete(f"{self.url}/{self.account_details['pesel']}", timeout=self.timeout)
        assert del_response.status_code == 200
        assert del_response.json()["message"] == "Account deleted"
