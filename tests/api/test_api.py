import pytest
import requests

class TestAPI:
    BASE_URL = "http://127.0.0.1:5000/api/accounts"
    ACC_DETAILS = {"name": "Jan", "surname": "Kowalski", "pesel": "01234567890"}

    def url(self, path=""):
        return f"{self.BASE_URL}{path}"

    @pytest.fixture(autouse=True)
    def setup(self):
        r = requests.post(self.url(), json=self.ACC_DETAILS)
        assert r.status_code == 201
        yield
        for acc in requests.get(self.url()).json():
            r = requests.delete(self.url(f"/{acc['pesel']}"))
            assert r.status_code == 200

    def test_get_personal_account(self):
        r = requests.get(self.url())
        assert r.status_code == 200
        accounts = r.json()
        assert len(accounts) == 1
        assert accounts[0]["pesel"] == self.ACC_DETAILS["pesel"]

    def test_get_account_count(self):
        r = requests.get(self.url("/count"))
        assert r.status_code == 200
        assert r.json()["count"] == 1

    def test_get_account_by_pesel(self):
        r = requests.get(self.url(f"/{self.ACC_DETAILS['pesel']}"))
        assert r.status_code == 200
        assert r.json()["pesel"] == self.ACC_DETAILS["pesel"]

    def test_get_account_by_pesel_not_found(self):
        r = requests.get(self.url("/nonexistent"))
        assert r.status_code == 404
        assert r.json()["error"] == "Account not found"

    def test_update_account(self):
        new_data = {"name": "Janusz", "surname": "Nowak"}
        r = requests.patch(self.url(f"/{self.ACC_DETAILS['pesel']}"), json=new_data)
        assert r.status_code == 200
        r = requests.get(self.url(f"/{self.ACC_DETAILS['pesel']}"))
        account = r.json()
        assert account["name"] == new_data["name"]
        assert account["surname"] == new_data["surname"]

    def test_update_account_not_found(self):
        r = requests.patch(self.url("/nonexistent"), json={"name": "X"})
        assert r.status_code == 404

    def test_update_account_invalid(self):
        r = requests.patch(self.url(f"/{self.ACC_DETAILS['pesel']}"), json={})
        assert r.status_code == 400

    def test_delete_account(self):
        r = requests.delete(self.url(f"/{self.ACC_DETAILS['pesel']}"))
        assert r.status_code == 200

    def test_delete_account_not_found(self):
        r = requests.delete(self.url("/nonexistent"))
        assert r.status_code == 404

    def test_create_account_invalid_json(self):
        r = requests.post(self.url(), data="notjson")
        assert r.status_code == 400
