from pydantic import BaseModel
from typing import ClassVar
from PIL import Image

from src.connectors.database.experiences import SheetsGiftDatabaseConnector


class Gift(BaseModel):
    gift_id: str
    title: str
    description: str
    img: Image
    price: int
    price_unit: str
    amount_paid: int
    has_contributed: bool

    db_connector: ClassVar = SheetsGiftDatabaseConnector()

    @classmethod
    def read(cls):
        pass


class GiftContribution(BaseModel):
    gift_code: str
    name: str
    amount: int
