import logging

logger = logging.getLogger(__name__)

from fastapi import APIRouter, HTTPException, Depends

from server.services.OrderService import order_service
from server.services.UserService import user_service
from server.hash import role_required
from server.models import OrderCreationRequestSchema

router = APIRouter()

@router.post(
    "/",
    responses={
        200: {"description": "Successful Response", "model": str},
    })
async def add_order(order: OrderCreationRequestSchema, current_user: dict = Depends(role_required("CUSTOMER"))):
    await order_service.add_order(order, current_user['username'])
    return 'Added'

@router.get("/")
async def get_orders(current_user: dict = Depends(role_required("DELIVERY_PERSONNEL"))):
    orders = await order_service.get_all()
    return orders

@router.post("/{id}/accept-for-delivery")
async def accept_orders(id, current_user: dict = Depends(role_required("DELIVERY_PERSONNEL"))):
    orders = await order_service.assign_delivery(id, current_user['username'])
    return orders
