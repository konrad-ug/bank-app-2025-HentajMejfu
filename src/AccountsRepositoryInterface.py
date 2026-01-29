from abc import ABC, abstractmethod


class AccounstRepository(ABC):

    @abstractmethod
    def save_all(self, accounts: list):
        pass

    def load_all(self) -> list:
        pass