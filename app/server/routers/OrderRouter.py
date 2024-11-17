import logging

logger = logging.getLogger(__name__)

from fastapi import APIRouter, HTTPException, Depends
from server.services.RestaurantService import restaurant_service
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
    inserted_id = await order_service.add_order(order, current_user['username'])
    return inserted_id

@router.get("/")
async def get_orders(current_user: dict = Depends(role_required("DELIVERY_PERSONNEL"))):
    orders = await order_service.get_all()
    return orders

@router.get("/{id}")
async def get_orders(id, current_user: dict = Depends(role_required("CUSTOMER"))):
    order = await order_service.get_by_id(id)
    return order

@router.post("/{id}/mark-accepted-for-delivery")
async def accept_orders(id, current_user: dict = Depends(role_required("DELIVERY_PERSONNEL"))):
    orders = await order_service.assign_delivery(id, current_user['username'])
    return orders

@router.post("/{id}/mark-prepared")
async def accept_orders(id, current_user: dict = Depends(role_required("RESTAURANT_OWNER"))):
    owned_restaurants = await restaurant_service.get_restaurants_by_owner(current_user['username'])
    logger.info(owned_restaurants)
    owned_restaurant_ids = [restaurant['_id'] for restaurant in owned_restaurants]

    order = await order_service.get_by_id(id)
    restaurant_id_from_order = order['restaurant_id']
    if restaurant_id_from_order in owned_restaurant_ids:
        orders = await order_service.mark_prepared(id)
        return orders
    else:
        raise HTTPException(
            status_code=409,
            detail="Restaurant Owner does not match Restaurant"
        ) 
    
@router.post("/{id}/mark-out-for-delivery")
async def accept_orders(id, current_user: dict = Depends(role_required("DELIVERY_PERSONNEL"))):
    orders = await order_service.mark_out_for_delivery(id)
    return orders

@router.post("/{id}/mark-delivered")
async def accept_orders(id, current_user: dict = Depends(role_required("DELIVERY_PERSONNEL"))):
    orders = await order_service.mark_delivered(id)
    return orders
