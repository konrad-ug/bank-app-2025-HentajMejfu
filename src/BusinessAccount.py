import os
from dotenv import load_dotenv
from datetime import datetime
import requests
from src.modules.Account import Account

load_dotenv()
BANK_APP_MF_URL: str = os.getenv("BANK_APP_MF_URL")

class BusinessAccount(Account):
    def __init__(self, company_name: str, nip: str):
        self.account_type: str = 'business'
        self.company_name: str = company_name

        if nip is not None and len(nip) == 10:
            if self.validateNIP(nip):
                self.nip: str = nip
            else:
                raise ValueError("Company not registered!!")

        else:
            self.nip: str = "Invalid"

        self.balance: float = 0
        self.history: list[float] = []

    def getExpressFee(self):
        return 5

    def submitForLoan(self, amount: int):
        if self.balance >= amount * 2 and -1775 in self.history:
            self.balance += amount
            return True
        else:
            return False

    def validateNIP(self, nip: str):
        date: str = datetime.today().strftime("%Y-%m-%d")
        print(f"Sending requests to {BANK_APP_MF_URL}")
        response = requests.get(f"{BANK_APP_MF_URL}/{nip}?date={date}")
        print(f"Repsonse status code: {response.json()}")
        if response.status_code != 200:
            return False
        data = response.json() or {}
        result = data.get("result") or {}
        subject = result.get("subject") or {}
        status = subject.get("statusValue")
        return status == "Czynny"