from pydantic import BaseModel


class Gift(BaseModel):
    gift_id: str
    title: str
    description: str
    img_path: str
    price: int
    price_unit: str
    paid: int
    contributors: list[str]


class GiftContribution(BaseModel):
    gift_code: str
    name: str
    amount: int
