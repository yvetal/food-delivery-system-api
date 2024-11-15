from pydantic import BaseModel, Field
from enum import Enum

class MenuItem(BaseModel):
    name: str = Field(...)
    price: int = Field(...)
    availability: bool = Field(...)

class OrderItem(BaseModel):
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

class OrderCondensed(BaseModel):
    preparation_status: PreparationStatus = Field(default=PreparationStatus.PREPARING)
    delivery_status: DeliveryStatus = Field(default = DeliveryStatus.ASSIGNING)
    order_item_ids: list[str] = Field(...)
    restaurant_id: str = Field(...)
    customer_id: str = Field(...)
    delivery_personnel_id: str = Field(default='')

class RestaurantCondensed(BaseModel):
    name: str = Field(...)
    opening_hours: str = Field(...)
    delivery_zone: str = Field(...)
    cuisine: str = Field(...)
    vegetarian: bool = Field(...)
    menu_item_ids: list[str] = Field(...)
    order_ids: list[str] = Field(...)
    restaurant_owner_id: str = Field(...)


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
    DELIVERY_PERSONNEL = 'DELIVERYPERSONNEL'
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