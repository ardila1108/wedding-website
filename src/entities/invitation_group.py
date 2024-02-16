from pydantic import BaseModel
from typing import ClassVar

from src.connectors.database import NotionDatabaseConnector


class InvitationGroup(BaseModel):
    name: str
    invitee_list: list

    db_connector: ClassVar = NotionDatabaseConnector()

    @classmethod
    def read(cls, group_id: str):
        group_dict = cls.db_connector.read_group(group_id)
        return cls(**group_dict)
