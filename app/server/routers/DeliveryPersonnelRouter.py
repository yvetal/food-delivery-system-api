from fastapi import APIRouter, HTTPException, Depends

from server.models import DeliveryPersonnelCreationRequestSchema
from server.services.DeliveryPersonnelService import delivery_personnel_service
from server.services.OrderService import order_service

from server.hash import role_required
from server.services.UserService import user_service


router = APIRouter()

@router.post(
    "/",
    responses={
        200: {"description": "Successful Response", "model": str},
    })
async def add_delivery_personnel(delivery_personnel: DeliveryPersonnelCreationRequestSchema):
    if await user_service.user_exists(delivery_personnel.username):
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        ) 
    await delivery_personnel_service.add_delivery_personnel(delivery_personnel)
    return {
        "message": "User registered successfully"
    }

@router.get("/orders")
async def get_orders_for_delivery_personnel(current_user: dict = Depends(role_required("DELIVERY_PERSONNEL"))):
    orders = await order_service.get_orders_for_delivery_personnel_by_username(current_user['username'])
    return orders