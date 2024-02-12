from pydantic import BaseModel
from typing import Optional


class PlusOneProfile(BaseModel):
    user_id: str
    name: str
    attending: bool = False
    restrictions: Optional[str] = "Ninguna"
