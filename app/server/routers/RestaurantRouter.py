from fastapi import APIRouter, HTTPException

from server.models import RestaurantCreationRequestSchema
from server.services.RestaurantService import restaurant_service
from server.services.UserService import user_service

router = APIRouter()

@router.post(
    "/",
    responses={
        200: {"description": "Successful Response", "model": str},
    })
async def add_restaurant(restaurant: RestaurantCreationRequestSchema):
    await restaurant_service.add_restaurant(restaurant)
    return 'Added'