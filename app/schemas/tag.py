from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TagCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=50)


class TagReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_at: datetime
    updated_at: datetime
