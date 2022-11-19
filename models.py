from typing import Optional
import uuid;
from pydantic import BaseModel, Field


class ListModel(BaseModel):
    id:str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str
    description: str
class ListUpdateModel(BaseModel):
    title: Optional[str]
    description: Optional[str]