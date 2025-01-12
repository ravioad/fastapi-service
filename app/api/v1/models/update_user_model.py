from typing import Optional
from pydantic import BaseModel, Field

class UpdateUserModel(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = Field(None, min_length=3, max_length=50)
