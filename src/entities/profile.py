from pydantic import BaseModel
from typing import Optional, ClassVar

from src.entities.plus_one_profile import PlusOneProfile
from src.connectors.database import SheetsDatabaseConnector


class InviteeProfile(BaseModel):
    user_id: str
    name: str
    attending: bool = False
    restrictions: Optional[str] = "Ninguna"
    can_bring_plus_one: Optional[bool] = False
    group_id: Optional[str] = None
    plus_one: Optional[PlusOneProfile] = None

    db_connector: ClassVar = SheetsDatabaseConnector()

    def write(self):
        self.db_connector.create(
            self.dict()
        )

    @classmethod
    def read(cls, user_id: str):
        profile_dict = cls.db_connector.read_user(user_id)
        return cls(**profile_dict)

    def update(self, changes_dict: dict):
        if self.plus_one:
            if "plus_one" in changes_dict:
                plus_one_changes = changes_dict.get("plus_one")
                if plus_one_changes:
                    self.db_connector.update(self.plus_one.user_id, plus_one_changes)
                else:
                    self.db_connector.delete(
                        user_id=self.plus_one.user_id
                    )
                changes_dict = {k: v for k, v in changes_dict.items() if k != "plus_one"}
        else:
            if "plus_one" in changes_dict:
                plus_one = changes_dict.get("plus_one")
                plus_one["user_id"] = f"{self.user_id}-1"
                plus_one["group_id"] = self.group_id
                self.db_connector.create(
                    plus_one
                )
        self.db_connector.update(self.user_id, changes_dict)
