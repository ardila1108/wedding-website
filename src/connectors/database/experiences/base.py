from abc import ABC, abstractmethod


class ExperienceDatabaseConnector(ABC):
    @abstractmethod
    def add_contribution(self, gift_contribution: dict):
        pass

    @abstractmethod
    def read_contributions(self, gift_id: str):
        pass

    @abstractmethod
    def read_gift(self, gift_id: str):
        pass
