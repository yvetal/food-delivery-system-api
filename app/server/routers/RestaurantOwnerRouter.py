from fastapi import APIRouter, HTTPException

from server.models import RestaurantOwnerCreationRequestSchema
from server.services.RestaurantOwnerService import restaurant_owner_service
from server.services.UserService import user_service

router = APIRouter()

@router.post(
    "/",
    responses={
        200: {"description": "Successful Response", "model": str},
    })
async def add_restaurant_owner(restaurant_owner: RestaurantOwnerCreationRequestSchema):
    if await user_service.user_exists(restaurant_owner.username):
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        ) 
    await restaurant_owner_service.add_restaurant_owner(restaurant_owner)
    return 'Added'