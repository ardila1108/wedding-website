from abc import ABC, abstractmethod


class ExperienceDatabaseConnector(ABC):
    @abstractmethod
    def add_contribution(self, gift_contribution: dict):
        pass

    def read_gift(self, gift_id: str):
        pass
