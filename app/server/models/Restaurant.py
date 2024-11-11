from pydantic import BaseModel, Field

from .MenuItem import MenuItemSchema
class RestaurantSchema(BaseModel):
    name: str = Field(...)
    menu_items: list[MenuItemSchema] = Field(...)
