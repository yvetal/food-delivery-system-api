from fastapi import APIRouter, HTTPException, Depends

from server.models import RestaurantCreationRequestSchema
from server.services.RestaurantService import restaurant_service
from server.services.UserService import user_service
from server.hash import role_required

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
