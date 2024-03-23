from abc import ABC, abstractmethod


class ExperienceImageStorageConnector(ABC):
    @abstractmethod
    def get_image_bytes(self, image_name: str):
        pass
