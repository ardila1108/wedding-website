from pydantic import BaseModel
from typing import ClassVar
import io
from PIL import Image

from src.connectors.database.experiences import SheetsGiftDatabaseConnector
from src.connectors.storage.experiences import GoogleDriveImageStorageConnector


class Gift(BaseModel):
    gift_id: str
    title: str
    description: str
    img: bytes
    price: int
    price_unit: str
    amount_paid: int
    contributors: list[str]

    db_connector: ClassVar = SheetsGiftDatabaseConnector()
    storage_connector: ClassVar = GoogleDriveImageStorageConnector()

    @classmethod
    def read(cls, gift_id):
        gift_dict = cls.db_connector.read_gift(gift_id)
        gift_dict["img"] = cls.storage_connector.get_image_bytes(gift_id)
        contributions = cls.db_connector.read_contributions(gift_id)
        gift_dict["amount_paid"] = sum([int(cont["amount"]) for cont in contributions])
        gift_dict["contributors"] = [cont["user_id"] for cont in contributions]
        return cls(**gift_dict)

    def get_image(self):
        return Image.open(io.BytesIO(self.img))


class GiftContribution(BaseModel):
    gift_id: str
    user_id: str
    amount: int

    db_connector: ClassVar = SheetsGiftDatabaseConnector()

    def write(self):
        self.db_connector.add_contribution(
            self.dict()
        )
