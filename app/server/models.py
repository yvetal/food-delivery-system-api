from pydantic import BaseModel, Field
from enum import Enum

class MenuItemCreationRequest(BaseModel):
    name: str = Field(...)
    price: int = Field(...)
    availability: bool = Field(...)

class MenuItem(BaseModel):
    name: str = Field(...)
    price: int = Field(...)
    availability: bool = Field(...)
    restaurant_id: str = Field(...)

class MenuItemQuerySchema(BaseModel):
    name: str | None = Field(default=None)
    price: str | None = Field(default=None)
    availability: bool | None = Field(default=True)
    restaurant_id: str | None = Field(default=None)

class OrderItemSchema(BaseModel):
    menu_item_id: str = Field(...)
    count: int = Field(...)

class PreparationStatus(Enum):
    PREPARING = 'PREPARING'
    PREPARED = 'PREPARED'

class DeliveryStatus(Enum):
    ASSIGNING = 'ASSIGNING'
    ASSIGNED = 'ASSIGNED'
    OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY'
    DELIVERED = 'DELIVERED'

class OrderCreationRequestSchema(BaseModel):
    order_items: list[OrderItemSchema] = Field(...)
    restaurant_id: str = Field(...)

class OrderSchema(BaseModel):
    preparation_status: PreparationStatus = Field(default=PreparationStatus.PREPARING)
    delivery_status: DeliveryStatus = Field(default = DeliveryStatus.ASSIGNING)
    order_item_ids: list[str] = Field(...)
    customer_username: str = Field(...)
    delivery_personnel_username: str = Field(default='')
    restaurant_id: str = Field(...)

class RestaurantSchema(BaseModel):
    name: str = Field(...)
    opening_hours: str = Field(default='')
    delivery_zone: str = Field(default='')
    cuisine: str = Field(default='')
    vegetarian: bool = Field(default=False)
    restaurant_owner_username: str = Field(...)

class RestaurantCreationRequestSchema(BaseModel):
    name: str = Field(...)
    restaurant_owner_username: str = Field(...)

class RestaurantUpdateRequestSchema(BaseModel):
    name: str | None = Field(default=None)
    opening_hours: str | None = Field(default=None)
    delivery_zone: str | None = Field(default=None)
    cuisine: str | None = Field(default=None)
    vegetarian: bool | None = Field(default=False)

class RestaurantQuerySchema(BaseModel):
    name: str | None = Field(default=None)
    delivery_zone: str | None = Field(default=None)
    cuisine: str | None = Field(default=None)
    vegetarian: bool | None = Field(default=False)

class UserDetails(BaseModel):
    pass

class DeliveryPersonnelDetails(UserDetails):
    pass

class CustomerDetails(UserDetails):
    delivery_address: str = Field(...)
    payment_upi_id: str = Field(...)

class RestaurantOwnerDetails(UserDetails):
    pass

class AdminDetails(UserDetails):
    pass

class UserRole(Enum):
    CUSTOMER = 'CUSTOMER'
    DELIVERY_PERSONNEL = 'DELIVERY_PERSONNEL'
    RESTAURANT_OWNER = 'RESTAURANT_OWNER'
    ADMIN = 'ADMIN'

class User(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    role: UserRole = Field(...)
    user_details_id: str = Field(...)

class UserInDB(BaseModel):
    username: str = Field(...)
    hashed_password: str = Field(...)
    role: UserRole = Field(...)
    user_details_id: str = Field(...)


class CustomerCreationRequestSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    customer_details: CustomerDetails = Field(...)

class RestaurantOwnerCreationRequestSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    restaurant_owner_details: RestaurantOwnerDetails = Field(...)

class DeliveryPersonnelCreationRequestSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    delivery_personnel_details: DeliveryPersonnelDetails = Field(...)

class AdminCreationRequestSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    admin_details: AdminDetails = Field(...)

class Token(BaseModel):
    access_token: str
    token_type: str


class LoginCredentials(BaseModel):
    username: str
    password: str