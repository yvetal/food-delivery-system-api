from pydantic import BaseModel, Field

class MenuItemSchema(BaseModel):
    name: str = Field(...)