from abc import ABC, abstractmethod


class DatabaseConnector(ABC):
    @abstractmethod
    def create(self, profile: dict):
        pass

    def read_user(self, user_id: str):
        pass

    def read_group(self, group_id: str):
        pass

    def update(self, user_id: str, update_dict: dict):
        pass

    def delete(self, user_id: str):
        pass
