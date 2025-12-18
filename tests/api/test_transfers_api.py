import pytest
import requests

class TestTransfersApi:
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

    @pytest.mark.parametrize("path, body, code", [
        (f"/{ACC_DETAILS['pesel']}/transfer", {"amount": 200, "type": "incoming"}, 200),
        ("/09876543210/transfer", {"amount": 200, "type": "incoming"}, 404),
        (f"/{ACC_DETAILS['pesel']}/transfer", {"xd": "XD"}, 400),
        (f"/{ACC_DETAILS['pesel']}/transfer", {"amount": 200, "type": "sigma"}, 400),
        (f"/{ACC_DETAILS['pesel']}/transfer", {"amount": "xd", "type": "incoming"}, 400)
    ],
    ids = [
        "valid transfer",
        "non_existing_account",
        "invalid_body",
        "invalid_type",
        "invalid_amount"
    ])
    def test_incoming_transfer(self, path: str, body: dict, code: int):
        r = requests.post(self.url(path), json=body)
        assert r.status_code == code

    @pytest.mark.parametrize("path, body, code", [
        (f"/{ACC_DETAILS['pesel']}/transfer", {"amount": 200, "type": "outgoing"}, 200),
        ("/09876543210/transfer", {"amount": 200, "type": "outgoing"}, 404),
        (f"/{ACC_DETAILS['pesel']}/transfer", {"xd": "XD"}, 400),
        (f"/{ACC_DETAILS['pesel']}/transfer", {"amount": 200, "type": "sigma"}, 400),
        (f"/{ACC_DETAILS['pesel']}/transfer", {"amount": "xd", "type": "outgoing"}, 400),
        (f"/{ACC_DETAILS['pesel']}/transfer", {"amount": 2137, "type": "outgoing"}, 422)
    ],
    ids = [
        "valid transfer",
        "non_existing_account",
        "invalid_body",
        "invalid_type",
        "invalid_amount",
        "insufficient_funds"
    ])
    def test_normal_transfer(self, path: str, body: dict, code: int):
        requests.post(self.url(f"/{self.ACC_DETAILS['pesel']}/transfer"), json={"amount": 420, "type": "incoming"})
        r = requests.post(self.url(path), json=body)
        assert r.status_code == code

    @pytest.mark.parametrize("path, body, code", [
        (f"/{ACC_DETAILS['pesel']}/transfer", {"amount": 200, "type": "express"}, 200),
        ("/09876543210/transfer", {"amount": 200, "type": "express"}, 404),
        (f"/{ACC_DETAILS['pesel']}/transfer", {"xd": "XD"}, 400),
        (f"/{ACC_DETAILS['pesel']}/transfer", {"amount": 200, "type": "xd"}, 400),
        (f"/{ACC_DETAILS['pesel']}/transfer", {"amount": "xd", "type": "express"}, 400),
        (f"/{ACC_DETAILS['pesel']}/transfer", {"amount": 2137, "type": "express"}, 422)
    ],
    ids = [
        "valid transfer",
        "non_existing_account",
        "invalid_body",
        "invalid_type",
        "invalid_amount",
        "insufficient_funds"
    ])
    def test_express_transfer(self, path: str, body: dict, code: int):
        requests.post(self.url(f"/{self.ACC_DETAILS['pesel']}/transfer"), json={"amount": 420, "type": "incoming"})
        r = requests.post(self.url(path), json=body)
        assert r.status_code == code