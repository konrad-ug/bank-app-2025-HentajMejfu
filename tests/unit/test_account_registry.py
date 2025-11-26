from src.AccountRegistry import AccountRegistry as ar
from src.PersonalAccount import PersonalAccount as pa
import pytest

class TestAccountRegistry:

    @pytest.fixture()
    def registry(self):
        registry = ar()
        return registry

    @pytest.fixture()
    def pAccounts(self):
        accounts = [
            pa('Malwina', 'Matysek', '80010112345'),
            pa('Maksymilian', 'Bielawski', '02222954321', 'PROM_202'),
            pa('Bartosz', 'Dziezyc', '99030367890', 'Xdddd')
        ]
        return accounts

    def test_add_personal_account(self, registry: ar, pAccounts: list[pa]):
        for account in pAccounts:
            registry.addAccount(account)

        assert len(registry.accounts) == 3
        assert registry.accounts == pAccounts

    @pytest.mark.parametrize("search_pesel, expected_account", [
        ('80010112345', 0),
        ('02222954321', 1),
        ('99999999999', None)
    ],
    ids = [
        "existing account 1",
        "existing account 2",
        "non-existing account"
    ])
    def test_search_with_pesel(self, registry: ar, pAccounts: list[pa], search_pesel: str, expected_account: pa):
        registry.accounts = pAccounts.copy()

        assert registry.search(search_pesel) == pAccounts[expected_account] if expected_account is not None else registry.search(search_pesel) is None

    def test_return_all_accounts(self, registry: ar, pAccounts: list[pa]):
        registry.accounts = pAccounts.copy()

        assert registry.getAllAccounts() == pAccounts

    def test_return_number_of_accounts(self, registry: ar, pAccounts: list[pa]):
        registry.accounts = pAccounts.copy()

        assert registry.getNumberOfAccounts() == 3