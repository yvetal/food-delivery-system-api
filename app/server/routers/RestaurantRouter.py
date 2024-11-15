import logging

logger = logging.getLogger(__name__)

from fastapi import APIRouter, HTTPException, Depends

from server.services.RestaurantService import restaurant_service
from server.services.UserService import user_service
from server.hash import role_required
from server.models import RestaurantCreationRequestSchema, RestaurantSchema, RestaurantUpdateRequestSchema, MenuItemCreationRequest

router = APIRouter()

@router.post(
    "/",
    responses={
        200: {"description": "Successful Response", "model": str},
    })
async def add_restaurant(restaurant: RestaurantCreationRequestSchema):
    await restaurant_service.add_restaurant(restaurant)
    return 'Added'

@router.get("/")
async def get_restaurants(current_user: dict = Depends(role_required("CUSTOMER"))):
    restaurants = await restaurant_service.get_all()
    return restaurants


@router.put("/{id}/")
async def get_restaurants(id: str, restaurant_update_details: RestaurantUpdateRequestSchema, current_user: dict = Depends(role_required("RESTAURANT_OWNER"))):
    restaurant: RestaurantSchema = await restaurant_service.get_by_id(id)
    if restaurant['restaurant_owner_username'] == current_user['username']:
        await restaurant_service.update_restaurant(id, restaurant_update_details)
    else:
        raise HTTPException(
            status_code=409,
            detail="Restaurant Owner does not match Restaurant"
        ) 

@router.put("/{id}/menu-items")
async def add_menu_item(id: str, menu_item: MenuItemCreationRequest, current_user: dict = Depends(role_required("RESTAURANT_OWNER"))):
    restaurant: RestaurantSchema = await restaurant_service.get_by_id(id)
    if restaurant['restaurant_owner_username'] == current_user['username']:
        await restaurant_service.add_menu_item(id, menu_item)
    else:
        raise HTTPException(
            status_code=409,
            detail="Restaurant Owner does not match Restaurant"
        ) 

@router.get("/{id}/menu-items")
async def get_menu_items_for_restaurant(id: str, current_user: dict = Depends(role_required("CUSTOMER"))):
    menu_items = await restaurant_service.get_menu_items(id)
    return menu_items
